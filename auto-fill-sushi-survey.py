#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-fill Google Form: แบบสอบถามปัจจัยทางการตลาดที่ส่งผลต่อการเลือกใช้บริการ ร้านซูชิสายพานของผู้บริโภค
High-speed Concurrent Asynchronous Submitter with Telemetry & CSV Logging
URL: https://docs.google.com/forms/d/e/1FAIpQLSfVCqzAoQZkyfPxRpkme_HV_7I_ZcoZxXjODZiAIQm8wcakBw/viewform
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

# Default configuration (overrideable via command line: python auto-fill-sushi-survey.py [COUNT] [CONCURRENCY])
NUM_RESPONSES = int(sys.argv[1]) if len(sys.argv) > 1 else 100
CONCURRENCY = int(sys.argv[2]) if len(sys.argv) > 2 else 10
TIMEOUT_SEC = 25.0           # Timeout ต่อ request
RETRY_LIMIT = 3              # จำนวนครั้งที่จะลองใหม่เมื่อพบข้อผิดพลาดหรือ 429

# ============================================================================
# LIKERT 5-POINT CHOICES & WEIGHT DISTRIBUTION
# ============================================================================
LIKERT_OPTIONS = [
    "5 = เห็นด้วยอย่างยิ่ง / สำคัญมากที่สุด",
    "4 = เห็นด้วย / สำคัญมาก",
    "3 = เห็นด้วยปานกลาง / สำคัญปานกลาง",
    "2 = ไม่เห็นด้วย / สำคัญน้อย",
    "1 = ไม่เห็นด้วยอย่างยิ่ง / สำคัญน้อยที่สุด"
]

# ค่าน้ำหนักความพึงพอใจ (80% ให้คะแนน 5, 18% ให้คะแนน 4, 2% ให้คะแนน 3)
LIKERT_WEIGHTS = [0.80, 0.18, 0.02, 0.00, 0.00]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1"
]

# ============================================================================
# ENTRY IDS MAPPING (20 QUESTIONS)
# ============================================================================
FORM_ENTRIES = {
    # ส่วนที่ 1: ปัจจัยส่วนประสมทางการตลาด (7Ps)
    # 1. ด้านผลิตภัณฑ์ (Product)
    "p1_freshness": "entry.392049935",      # ความสดใหม่และคุณภาพวัตถุดิบ
    "p1_taste": "entry.1477233486",          # รสชาติอร่อย เอกลักษณ์
    "p1_variety": "entry.1542818651",        # ความหลากหลายบนสายพาน

    # 2. ด้านราคา (Price)
    "p2_value": "entry.737780018",           # ความคุ้มค่า
    "p2_clarity": "entry.2122703884",        # ความชัดเจน แบ่งตามสีจาน
    "p2_affordable": "entry.1725959706",     # ราคาเข้าถึงง่าย เหมาะสมงบ

    # 3. ด้านช่องทางจัดจำหน่าย (Place)
    "p3_location": "entry.1319162207",       # เดินทางสะดวก เข้าถึงง่าย
    "p3_mall": "entry.372289045",            # อยู่ในห้างหรือชุมชน

    # 4. ด้านส่งเสริมการตลาด (Promotion)
    "p4_promo": "entry.1175131233",          # โปรโมชั่น ส่วนลด บัตรสมาชิก
    "p4_social": "entry.732199028",          # รีวิวผ่านโซเชียลมีเดีย

    # 5. ด้านบุคลากร (People)
    "p5_service": "entry.459040376",         # พนักงานสุภาพ เป็นมิตร
    "p5_knowledge": "entry.1410867681",      # พนักงานมีความรู้ แนะนำถูกต้อง

    # 6. ด้านกระบวนการให้บริการ (Process)
    "p6_speed": "entry.1428864009",          # สายพานรวดเร็ว ไม่ต้องรอนาน
    "p6_tablet": "entry.168920346",          # สั่งสะดวกผ่านแท็บเล็ต/สายพาน

    # 7. ด้านลักษณะทางกายภาพ (Physical Evidence)
    "p7_cleanliness": "entry.1229830647",    # ความสะอาด บรรยากาศ
    "p7_decoration": "entry.285798591",      # ตกแต่งสวยงาม สไตล์ญี่ปุ่น

    # ส่วนที่ 2: พฤติกรรมผู้บริโภค (Consumer Behavior)
    "b1_revisit": "entry.1312370900",        # ตั้งใจกลับมาใช้บริการอีก
    "b2_recommend": "entry.1920043945",      # แนะนำเพื่อนและครอบครัว
    "b3_overall_sat": "entry.854429353",     # ความพึงพอใจโดยรวม
    "b4_convenience": "entry.322097084"      # ตอบสนองความสะดวกรวดเร็ว
}

def pick_likert():
    """สุ่มเลือกคำตอบตามค่าน้ำหนักที่กำหนด"""
    return random.choices(LIKERT_OPTIONS, weights=LIKERT_WEIGHTS, k=1)[0]

async def fetch_hidden_tokens(client: httpx.AsyncClient):
    """ดึง Security Tokens fbzx และ pageHistory ล่าสุดจาก Google Form"""
    resp = await client.get(VIEW_URL, timeout=TIMEOUT_SEC)
    html = resp.text
    
    def grab(pat, default=""):
        m = re.search(pat, html)
        return m.group(1) if m else default

    return {
        "fbzx": grab(r'name="fbzx"\s+value="([^"]+)"', "-969805304991096499"),
        "fvv": grab(r'name="fvv"\s+value="([^"]+)"', "1"),
        "pageHistory": grab(r'name="pageHistory"\s+value="([^"]+)"', "0,1")
    }

async def submit_worker(worker_id: int, queue: asyncio.Queue, results: list, tokens: dict, client: httpx.AsyncClient):
    """Worker ประจำการส่งฟอร์มแบบ Asynchronous"""
    while not queue.empty():
        item_index = await queue.get()
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": VIEW_URL,
            "Origin": "https://docs.google.com",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # สร้าง Payload ให้ครบทุกข้อตามสเปค
        response_record = {
            "Index": item_index,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        payload = {
            "fbzx": tokens["fbzx"],
            "fvv": tokens["fvv"],
            "pageHistory": tokens["pageHistory"]
        }

        for key, entry_id in FORM_ENTRIES.items():
            ans = pick_likert()
            payload[entry_id] = ans
            response_record[key] = ans

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
                    print(f"[{item_index:03d}/{NUM_RESPONSES:03d}]  OK (HTTP {status_code}) - {latency_ms}ms (Worker {worker_id})")
                    break
                elif status_code == 429:
                    print(f"[{item_index:03d}] ⚠️ HTTP 429 Rate Limit. Backing off {attempt * 1.5}s...")
                    await asyncio.sleep(attempt * 1.5)
                else:
                    print(f"[{item_index:03d}] ⚠️ HTTP {status_code}. Retrying ({attempt}/{RETRY_LIMIT})...")
                    await asyncio.sleep(0.5)

            except Exception as e:
                print(f"[{item_index:03d}] ❌ Error: {e}. Retrying ({attempt}/{RETRY_LIMIT})...")
                await asyncio.sleep(0.8)

        response_record["Status"] = "SUCCESS" if success else f"FAIL_{status_code}"
        results.append(response_record)

        # สุ่มเวลาหน่วงเบาๆ ให้เป็นธรรมชาติ
        await asyncio.sleep(random.uniform(0.15, 0.45))
        queue.task_done()

async def main():
    print("=" * 68)
    print("🍣 Auto-fill Google Form: แบบสอบถามร้านซูชิสายพาน (Conveyor Belt Sushi)")
    print(f"🎯 Target Volume: {NUM_RESPONSES} submissions")
    print(f"⚡ Concurrency: {CONCURRENCY} workers")
    print("=" * 68)

    async with httpx.AsyncClient(http2=True, follow_redirects=False) as client:
        print("🔍 Fetching security tokens from Google Form...")
        try:
            tokens = await fetch_hidden_tokens(client)
            print(f"✅ Tokens Loaded: fbzx={tokens['fbzx']}, pageHistory={tokens['pageHistory']}\n")
        except Exception as e:
            print(f"❌ Failed to fetch tokens: {e}")
            tokens = {"fbzx": "-969805304991096499", "fvv": "1", "pageHistory": "0,1"}

        queue = asyncio.Queue()
        for i in range(1, NUM_RESPONSES + 1):
            queue.put_nowait(i)

        results = []
        start_all = time.perf_counter()

        # สร้าง Worker Pool
        workers = [
            asyncio.create_task(submit_worker(w_id, queue, results, tokens, client))
            for w_id in range(1, CONCURRENCY + 1)
        ]

        await queue.join()
        for w in workers:
            w.cancel()

        total_time = time.perf_counter() - start_all

    # สรุปผลการทำงาน
    success_count = sum(1 for r in results if r["Status"] == "SUCCESS")
    speed_rps = success_count / total_time if total_time > 0 else 0

    print("\n" + "=" * 68)
    print("🏁 EXECUTION SUMMARY")
    print(f"  • Total Sent: {len(results)} / {NUM_RESPONSES}")
    print(f"  • Success Rate: {success_count}/{len(results)} ({(success_count / len(results) * 100):.1f}%)")
    print(f"  • Total Time: {total_time:.2f} seconds")
    print(f"  • Throughput: {speed_rps:.2f} submissions / sec")
    print("=" * 68)

    # บันทึกผลลัพธ์เป็นไฟล์ CSV
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
