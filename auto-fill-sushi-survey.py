#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-fill Google Form: แบบสอบถามร้านซูชิสายพาน (Human-Realistic Simulation Engine)
Features:
  - Persona-Based Statistical Correlation (ไม่สุ่มมั่ว มีความสมเหตุสมผลของมนุษย์)
  - Realistic Human Timing & Dynamic Jitter
  - Full Browser Headers & Client Hints Simulation
  - Dynamic Session Token Handshake (Unique fbzx per session)
  - CSV Telemetry Export
"""

import asyncio
import csv
import httpx
import random
import re
import sys
import time
from datetime import datetime

# Windows Console UTF-8 compatibility
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# ============================================================================
# CONFIGURATION
# ============================================================================
FORM_ID = "1FAIpQLSfVCqzAoQZkyfPxRpkme_HV_7I_ZcoZxXjODZiAIQm8wcakBw"
VIEW_URL = f"https://docs.google.com/forms/d/e/{FORM_ID}/viewform"
POST_URL = f"https://docs.google.com/forms/d/e/{FORM_ID}/formResponse"

# Command-line arguments: python auto-fill-sushi-survey.py [COUNT] [CONCURRENCY] [MODE]
# Modes: fast (0.3-0.8s delay), human (2.0-5.0s delay), stealth (8.0-18.0s delay)
NUM_RESPONSES = int(sys.argv[1]) if len(sys.argv) > 1 else 100
CONCURRENCY = int(sys.argv[2]) if len(sys.argv) > 2 else 5
MODE = sys.argv[3].lower() if len(sys.argv) > 3 else "fast"

TIMEOUT_SEC = 30.0
RETRY_LIMIT = 3

# ============================================================================
# LIKERT 5-POINT CHOICES
# ============================================================================
LIKERT_MAP = {
    5: "5 = เห็นด้วยอย่างยิ่ง / สำคัญมากที่สุด",
    4: "4 = เห็นด้วย / สำคัญมาก",
    3: "3 = เห็นด้วยปานกลาง / สำคัญปานกลาง",
    2: "2 = ไม่เห็นด้วย / สำคัญน้อย",
    1: "1 = ไม่เห็นด้วยอย่างยิ่ง / สำคัญน้อยที่สุด"
}

# ============================================================================
# BROWSER CLIENT SIGNATURES (Modern User-Agents & Sec-Ch-Ua Client Hints)
# ============================================================================
CLIENT_PROFILES = [
    {
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "ch_ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "ch_mobile": "?0",
        "ch_platform": '"Windows"'
    },
    {
        "ua": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "ch_ua": '"Chromium";v="123", "Google Chrome";v="123", "Not-A.Brand";v="99"',
        "ch_mobile": "?0",
        "ch_platform": '"Windows"'
    },
    {
        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "ch_ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "ch_mobile": "?0",
        "ch_platform": '"macOS"'
    },
    {
        "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
        "ch_ua": None,
        "ch_mobile": "?1",
        "ch_platform": '"iOS"'
    },
    {
        "ua": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.82 Mobile Safari/537.36",
        "ch_ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "ch_mobile": "?1",
        "ch_platform": '"Android"'
    }
]

# ============================================================================
# HUMAN PERSONA ARCHETYPES (จำลองบุคลิกภาพและความคิดเห็นของมนุษย์จริง)
# ============================================================================
# คนจริงจะไม่ตอบสุ่มมั่ว แต่จะมี "ทัศนคติโดยรวม" และความเชื่อมโยงของแต่ละข้อ
PERSONA_ARCHETYPES = [
    {
        "name": "Super Fan (Sushi Lover)",
        "weight": 0.55,  # 55% ของคนตอบ
        "base_score": 4.85,
        "category_bias": {
            "product": 0.2, "price": -0.1, "place": 0.1, "promo": 0.0,
            "people": 0.15, "process": 0.1, "physical": 0.2, "behavior": 0.25
        }
    },
    {
        "name": "Satisfied Pragmatist",
        "weight": 0.30,  # 30% ของคนตอบ
        "base_score": 4.35,
        "category_bias": {
            "product": 0.15, "price": -0.25, "place": 0.0, "promo": -0.1,
            "people": 0.05, "process": 0.05, "physical": 0.1, "behavior": 0.1
        }
    },
    {
        "name": "Value-Conscious Diner",
        "weight": 0.10,  # 10% ของคนตอบ
        "base_score": 3.95,
        "category_bias": {
            "product": 0.1, "price": -0.45, "place": -0.1, "promo": 0.2,
            "people": 0.0, "process": -0.1, "physical": 0.05, "behavior": -0.1
        }
    },
    {
        "name": "Critical Quality Inspector",
        "weight": 0.05,  # 5% ของคนตอบ
        "base_score": 3.75,
        "category_bias": {
            "product": 0.0, "price": -0.3, "place": 0.0, "promo": -0.2,
            "people": -0.1, "process": -0.2, "physical": 0.1, "behavior": -0.15
        }
    }
]

# Mapping Categories to Entry IDs
QUESTION_CATEGORIES = {
    # 7Ps
    "p1_freshness": ("product", "entry.392049935"),
    "p1_taste": ("product", "entry.1477233486"),
    "p1_variety": ("product", "entry.1542818651"),
    "p2_value": ("price", "entry.737780018"),
    "p2_clarity": ("price", "entry.2122703884"),
    "p2_affordable": ("price", "entry.1725959706"),
    "p3_location": ("place", "entry.1319162207"),
    "p3_mall": ("place", "entry.372289045"),
    "p4_promo": ("promo", "entry.1175131233"),
    "p4_social": ("promo", "entry.732199028"),
    "p5_service": ("people", "entry.459040376"),
    "p5_knowledge": ("people", "entry.1410867681"),
    "p6_speed": ("process", "entry.1428864009"),
    "p6_tablet": ("process", "entry.168920346"),
    "p7_cleanliness": ("physical", "entry.1229830647"),
    "p7_decoration": ("physical", "entry.285798591"),
    # Behavior
    "b1_revisit": ("behavior", "entry.1312370900"),
    "b2_recommend": ("behavior", "entry.1920043945"),
    "b3_overall_sat": ("behavior", "entry.854429353"),
    "b4_convenience": ("behavior", "entry.322097084")
}

def generate_human_answers():
    """สร้างคำตอบ 20 ข้อโดยใช้ Persona Algorithm ให้มี Correlation สมจริงตามพฤติกรรมมนุษย์"""
    persona = random.choices(
        PERSONA_ARCHETYPES,
        weights=[p["weight"] for p in PERSONA_ARCHETYPES],
        k=1
    )[0]
    
    # Random mood jitter สำหรับคนตอบคนนี้
    respondent_mood = random.gauss(0, 0.12)
    answers = {}
    
    for q_key, (category, entry_id) in QUESTION_CATEGORIES.items():
        cat_bias = persona["category_bias"].get(category, 0.0)
        # คำนวณคะแนนพื้นฐาน + category bias + อารมณ์คนตอบ + noise ของคำถามนั้นๆ
        raw_score = persona["base_score"] + cat_bias + respondent_mood + random.gauss(0, 0.28)
        
        # ปรับคะแนนให้อยู่ในช่วง 1 ถึง 5
        score = int(round(max(1, min(5, raw_score))))
        answers[entry_id] = LIKERT_MAP[score]
        
    return answers, persona["name"]

async def fetch_session_handshake(client: httpx.AsyncClient, headers: dict):
    """จำลองการเปิดหน้าเว็บเหมือนมนุษย์ และดึง Token fbzx สำหรับเซสชันนั้น"""
    view_headers = {
        **headers,
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1"
    }
    resp = await client.get(VIEW_URL, headers=view_headers, timeout=TIMEOUT_SEC)
    html = resp.text
    
    def grab(pat, default=""):
        m = re.search(pat, html)
        return m.group(1) if m else default

    return {
        "fbzx": grab(r'name="fbzx"\s+value="([^"]+)"', "-969805304991096499"),
        "fvv": grab(r'name="fvv"\s+value="([^"]+)"', "1"),
        "pageHistory": grab(r'name="pageHistory"\s+value="([^"]+)"', "0,1")
    }

async def submit_worker(worker_id: int, queue: asyncio.Queue, results: list):
    """Worker แต่ละตัวจำลองผู้ตอบแบบสอบถามจริง 1 คนต่อรอบ"""
    async with httpx.AsyncClient(http2=True, follow_redirects=False) as client:
        while not queue.empty():
            item_index = await queue.get()
            profile = random.choice(CLIENT_PROFILES)
            
            headers = {
                "User-Agent": profile["ua"],
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7",
                "Referer": VIEW_URL,
                "Origin": "https://docs.google.com",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            if profile.get("ch_ua"):
                headers["Sec-Ch-Ua"] = profile["ch_ua"]
                headers["Sec-Ch-Ua-Mobile"] = profile["ch_mobile"]
                headers["Sec-Ch-Ua-Platform"] = profile["ch_platform"]

            # 1. จำลองการเปิดเข้าหน้าฟอร์ม (GET) ดึง Token
            try:
                tokens = await fetch_session_handshake(client, headers)
            except Exception:
                tokens = {"fbzx": "-969805304991096499", "fvv": "1", "pageHistory": "0,1"}

            # 2. จำลองเวลาที่มนุษย์ใช้ในการอ่านและเลือกช้อยส์ (Human Reading Delay)
            if MODE == "stealth":
                reading_delay = random.uniform(8.0, 18.0)
            elif MODE == "human":
                reading_delay = random.uniform(2.0, 5.0)
            else:
                reading_delay = random.uniform(0.2, 0.6)

            await asyncio.sleep(reading_delay)

            # 3. สร้างคำตอบแบบ Human Persona
            answers_dict, persona_name = generate_human_answers()

            payload = {
                "fbzx": tokens["fbzx"],
                "fvv": tokens["fvv"],
                "pageHistory": tokens["pageHistory"],
                **answers_dict
            }

            response_record = {
                "Index": item_index,
                "Persona": persona_name,
                "Device": "Mobile" if profile["ch_mobile"] == "?1" else "Desktop",
                "ReadingTimeSec": round(reading_delay, 2),
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                **answers_dict
            }

            success = False
            status_code = 0

            for attempt in range(1, RETRY_LIMIT + 1):
                try:
                    start_t = time.perf_counter()
                    r = await client.post(POST_URL, data=payload, headers=headers, timeout=TIMEOUT_SEC)
                    latency_ms = int((time.perf_counter() - start_t) * 1000)
                    status_code = r.status_code

                    if status_code in (200, 302):
                        success = True
                        print(f"[{item_index:03d}/{NUM_RESPONSES:03d}]  OK (HTTP {status_code}) - {latency_ms}ms | Persona: {persona_name:<26} | Device: {response_record['Device']}")
                        break
                    elif status_code == 429:
                        print(f"[{item_index:03d}] ⚠️ HTTP 429 Rate Limit. Backing off {attempt * 2.0}s...")
                        await asyncio.sleep(attempt * 2.0)
                    else:
                        print(f"[{item_index:03d}] ⚠️ HTTP {status_code}. Retrying ({attempt}/{RETRY_LIMIT})...")
                        await asyncio.sleep(1.0)

                except Exception as e:
                    print(f"[{item_index:03d}] ❌ Error: {e}. Retrying ({attempt}/{RETRY_LIMIT})...")
                    await asyncio.sleep(1.2)

            response_record["Status"] = "SUCCESS" if success else f"FAIL_{status_code}"
            results.append(response_record)

            # พักก่อนรับงานชิ้นถัดไป
            await asyncio.sleep(random.uniform(0.3, 0.9))
            queue.task_done()

async def main():
    print("=" * 75)
    print("🍣 AutoForm Pro Max - Conveyor Belt Sushi Survey (Humanizer Engine)")
    print(f"🎯 Target: {NUM_RESPONSES} responses | Workers: {CONCURRENCY} | Mode: {MODE.upper()}")
    print("🧠 Persona Modeling: Brand Loyalist (55%), Pragmatist (30%), Value (10%), Critical (5%)")
    print("=" * 75 + "\n")

    queue = asyncio.Queue()
    for i in range(1, NUM_RESPONSES + 1):
        queue.put_nowait(i)

    results = []
    start_all = time.perf_counter()

    workers = [
        asyncio.create_task(submit_worker(w_id, queue, results))
        for w_id in range(1, CONCURRENCY + 1)
    ]

    await queue.join()
    for w in workers:
        w.cancel()

    total_time = time.perf_counter() - start_all
    success_count = sum(1 for r in results if r["Status"] == "SUCCESS")
    speed_rps = success_count / total_time if total_time > 0 else 0

    print("\n" + "=" * 75)
    print("🏁 EXECUTION SUMMARY")
    print(f"  • Total Responses: {len(results)} / {NUM_RESPONSES}")
    print(f"  • Success Rate: {success_count}/{len(results)} ({(success_count / len(results) * 100):.1f}%)")
    print(f"  • Total Duration: {total_time:.2f} seconds")
    print(f"  • Average Pace: {speed_rps:.2f} submissions / sec")
    print("=" * 75)

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"sushi_survey_results_{timestamp_str}.csv"
    
    if results:
        fieldnames = list(results[0].keys())
        with open(csv_filename, "w", newline="", encoding="utf-8-sig") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"📁 Results saved to: {csv_filename}\n")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
