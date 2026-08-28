# auto-form-admin.py
import requests, random, re, time

VIEW_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfGErFMwiRBEn0Y5yNulltD9u_Ypag-b0U6wG_BHXP_TMxXEA/viewform"
POST_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfGErFMwiRBEn0Y5yNulltD9u_Ypag-b0U6wG_BHXP_TMxXEA/formResponse"
NUM = 300  # จำนวนที่ต้องการส่ง

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Referer": VIEW_URL,
})

# ตัวเลือกตามฟอร์ม
can_attend_choices = ["ได้ ฉันยินดีไปร่วมงาน", "ขออภัย ไม่สะดวกไปร่วมงานจริงๆ"]
source_choices = ["เว็บไซต์", "เพื่อน", "หนังสือพิมพ์", "โฆษณา"]

first_names = ["สมชาย","สมหญิง","ปิยะ","กนก","ชลธิชา","ธีรนันท์","อภิวัฒน์","รัชนก","พัชรพล","อรณิชา"]
last_names  = ["ใจดี","เดชะ","สุนทร","วงศ์สุวรรณ","ทิพย์มณี","ศรีสุข","เรืองรอง","จิตอารี","พงษ์ศักดิ์","นาคินทร์"]

def fetch_hidden():
    html = session.get(VIEW_URL, timeout=20).text
    def grab(pat, default=""):
        m = re.search(pat, html)
        return m.group(1) if m else default
    return {
        "fbzx": grab(r'name="fbzx"\s+value="([^"]+)"'),
        "fvv": grab(r'name="fvv"\s+value="([^"]+)"', "1"),
        "pageHistory": grab(r'name="pageHistory"\s+value="([^"]+)"', "0"),
        "token": grab(r'name="token"\s+value="([^"]+)"', ""),  # บางฟอร์มไม่มี
    }

def make_payload(hidden):
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    comment = random.choice(["", "เจอกันในงานครับ", "สนใจรายละเอียดเพิ่ม", "สอบถามเวลาเริ่มกิจกรรม"])
    payload = {
        # entry IDs จากฟอร์มของคุณ
        "entry.877086558": random.choice(can_attend_choices),
        "entry.1498135098": name,
        "entry.1424661284": random.choice(source_choices),
        "entry.2606285": comment,

        # hidden fields จำเป็นของ Google Forms
        "fvv": hidden["fvv"],
        "pageHistory": hidden["pageHistory"],
        "fbzx": hidden["fbzx"],
    }
    if hidden["token"]:
        payload["token"] = hidden["token"]
    return payload

def submit_once(i, hidden_fields):
    # ไม่ต้อง fetch_hidden() ทุกครั้งแล้ว ใช้ hidden_fields ที่รับเข้ามาแทน
    r = session.post(POST_URL, data=make_payload(hidden_fields), timeout=20, allow_redirects=False)
    ok = r.status_code in (200, 302)
    print(f"[{i}] {'OK' if ok else 'NG'} ({r.status_code})")
    return ok

if __name__ == "__main__":
    print("Fetching initial form data...")
    try:
        # ดึง hidden fields แค่ครั้งเดียวก่อนเริ่มลูป
        hidden_data = fetch_hidden()
        print("Initial data fetched. Starting submissions...")
    except Exception as e:
        print(f"Failed to fetch initial form data: {e}")
        exit()

    ok = 0
    for i in range(1, NUM + 1):
        try:
            # ส่ง hidden_data ที่ดึงมาแล้วเข้าไปในฟังก์ชัน
            if submit_once(i, hidden_data):
                ok += 1
        except Exception as e:
            print(f"[{i}] ERROR: {e}")
        # ปรับลดเวลาหน่วงลงเล็กน้อย
        time.sleep(random.uniform(0.3, 0.8))
    print(f"Done. Success: {ok}/{NUM}")
