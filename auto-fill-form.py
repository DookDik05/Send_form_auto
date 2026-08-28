import asyncio, httpx, random, re, uuid, csv

FORM_ID = "1FAIpQLSeFltPTHhM4uNfOSh0vDuAWL5M-TFzD8KQiuLKF8J3G9jSnlw"
VIEW_URL = f"https://docs.google.com/forms/d/e/{FORM_ID}/viewform"
POST_URL = f"https://docs.google.com/forms/d/e/{FORM_ID}/formResponse"

NUM_RESPONSES = 1000           # จำนวนที่ต้องการส่ง
CONCURRENCY = 10               # งานพร้อมกัน (ลอง 5–10)
RETRIES = 2                   # รีทรายเมื่อพลาด/429

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]

# ---------- ช้อยส์ + น้ำหนัก (คงจากที่ตั้งไว้) ----------
def choice_w(opts, w): return random.choices(opts, weights=w, k=1)[0]

nationality_choices = ["คนไทย (Thai)", "ต่างชาติ (Foreigner)"]; nationality_w = [0.9, 0.1]
gender_choices = ["ชาย (Male)", "หญิง (Female)", "อื่นๆ (Other)"]; gender_w = [0.48, 0.48, 0.04]
age_choices = [
    "ต่ำกว่า 18 (Less than 18 years old)", "18-25 ปี (Between 18 - 25 years old)",
    "26-35 ปี (Between 26 - 35 years old)", "36-45 ปี (Between 36 - 45 years old)",
    "46-60 ปี (Between 46 - 60 years old)", "มากกว่า 60 ปี (More than 60 years old)",
]; age_w = [0.05, 0.25, 0.30, 0.20, 0.15, 0.05]
where_from_choices = ["ในเขตจังหวัดอุดรธานี (Udon Thani Area)", "มาจากจังหวัดอื่น (Other Provinces)", "มาจากต่างประเทศ (Abroad)"]; where_from_w = [0.6, 0.35, 0.05]
tourism_type_choices = ["พักค้างในอุดรธานี (Visiting and stay at Udon Thani)", "พักค้างใกล้เคียง (Visiting and stay at nearby province)", "ไม่พักค้าง (Non-overnight tourism)"]; tourism_type_w = [0.55, 0.15, 0.30]
duration_choices = ["1 - 2 วัน (1 - 2 Days)", "3 - 5 วัน (3 - 5 Days)", "มากกว่า 5 วัน (More than 5 Days)"]; duration_w = [0.65, 0.30, 0.05]
budget_choices = ["0 - 2,000 (THB)", "2,001 - 5,000 (THB)", "5,001 - 7,000 (THB)", "7,001 - 10,000 (THB)", "มากกว่า 10,000 บาทขึ้นไป (More than 10,000 THB)"]; budget_w = [0.25, 0.35, 0.20, 0.12, 0.08]
spend_event_choices = ["0 - 200 บาท (THB)", "201-500 บาท (THB)", "500-700 บาท (THB)", "701-1,000 บาท (THB)", "มากกว่า 1,000 บาท (More than 1,000 THB)"]; spend_event_w = [0.25, 0.40, 0.18, 0.12, 0.05]
source_choices = ["สื่อออนไลน์ Online media", "ป้ายประชาสัมพันธ์ Information board", "อื่นๆ etc."]; source_w = [0.75, 0.20, 0.05]

data_keys = {
    "nationality": "entry.1086328584", "gender": "entry.721007974",
    "age": "entry.540972076", "where_from": "entry.2115264552",
    "tourism_type": "entry.533360791", "duration": "entry.1365390770",
    "budget": "entry.667640791", "spend_event": "entry.875290967",
    "source": "entry.421713523",
    "press_conf": "entry.1792294564", "location": "entry.914468717",
    "concert": "entry.1854286772", "ceremony": "entry.1608147273",
    "activities": "entry.397101435", "parking": "entry.1010756211",
    "food": "entry.1494541273", "bathroom": "entry.1987127571",
}

FIVE_LABEL = "5 = มากที่สุด(Highly Satisfied)"

def make_payload(fbzx: str) -> dict:
    payload = {
        data_keys["nationality"]: choice_w(nationality_choices, nationality_w),
        data_keys["gender"]: choice_w(gender_choices, gender_w),
        data_keys["age"]: choice_w(age_choices, age_w),
        data_keys["where_from"]: choice_w(where_from_choices, where_from_w),
        data_keys["tourism_type"]: choice_w(tourism_type_choices, tourism_type_w),
        data_keys["duration"]: choice_w(duration_choices, duration_w),
        data_keys["budget"]: choice_w(budget_choices, budget_w),
        data_keys["spend_event"]: choice_w(spend_event_choices, spend_event_w),
        data_keys["source"]: choice_w(source_choices, source_w),
        data_keys["press_conf"]: FIVE_LABEL, data_keys["location"]: FIVE_LABEL,
        data_keys["concert"]: FIVE_LABEL, data_keys["ceremony"]: FIVE_LABEL,
        data_keys["activities"]: FIVE_LABEL, data_keys["parking"]: FIVE_LABEL,
        data_keys["food"]: FIVE_LABEL, data_keys["bathroom"]: FIVE_LABEL,
        "fvv": "1", "draftResponse": "[]", "pageHistory": "0,1", "fbzx": fbzx,
    }
    return payload

async def get_fbzx(client: httpx.AsyncClient, headers: dict) -> str:
    r = await client.get(VIEW_URL, headers=headers)
    r.raise_for_status()
    m = re.search(r'name="fbzx"\s+value="([^"]+)"', r.text)
    if not m:
        raise RuntimeError("ไม่พบ fbzx token")
    return m.group(1)

async def submit_once(client: httpx.AsyncClient, sem: asyncio.Semaphore, idx: int):
    # จำกัด concurrency
    async with sem:
        ua = random.choice(USER_AGENTS)
        headers = {
            "User-Agent": ua,
            "Referer": VIEW_URL,
            "Accept-Encoding": "gzip, deflate, br",
        }
        # jitter เล็ก ๆ ให้ดูเป็นธรรมชาติ
        await asyncio.sleep(random.uniform(0.02, 0.20))
        # retry เบา ๆ หากพลาด (429/เน็ตตก)
        for attempt in range(RETRIES + 1):
            try:
                fbzx = await get_fbzx(client, headers)
                payload = make_payload(fbzx)
                r = await client.post(POST_URL, data=payload, headers=headers, follow_redirects=False, timeout=20.0)
                if r.status_code in (200, 302):
                    print(f"[{idx}] OK ({r.status_code})")
                    return True
                # ถ้าโดน 429/403 ลอง backoff
                if r.status_code in (429, 403, 400, 500):
                    await asyncio.sleep(0.3 * (attempt + 1) + random.uniform(0.0, 0.2))
                    continue
                print(f"[{idx}] status {r.status_code}")
                return False
            except Exception as e:
                if attempt < RETRIES:
                    await asyncio.sleep(0.3 * (attempt + 1) + random.uniform(0.0, 0.2))
                    continue
                print(f"[{idx}] ERROR: {e}")
                return False

async def main():
    sem = asyncio.Semaphore(CONCURRENCY)
    success = 0
    async with httpx.AsyncClient(http2=True, timeout=20.0) as client:
        tasks = [submit_once(client, sem, i+1) for i in range(NUM_RESPONSES)]
        for coro in asyncio.as_completed(tasks):
            ok = await coro
            if ok: success += 1
    print(f"Done. Successful posts: {success}/{NUM_RESPONSES}")

if __name__ == "__main__":
    asyncio.run(main())
