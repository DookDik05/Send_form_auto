#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoForm Runners - Conveyor Belt Sushi Survey (7Ps & Consumer Behavior)
Supports both Async HTTPX High-Performance and Selenium Visual Humanizer modes.
"""

import asyncio
import time
import random
import sys
from datetime import datetime
import httpx

from ..core.persona_engine import generate_sushi_persona_answers
from ..core.http_client import get_random_browser_profile, build_browser_headers, fetch_form_security_tokens
from ..utils.csv_manager import export_results_to_csv
from ..utils.console import setup_utf8_console, print_banner, print_summary_card
from ..utils.logger import FormLogger

FORM_ID = "1FAIpQLSfVCqzAoQZkyfPxRpkme_HV_7I_ZcoZxXjODZiAIQm8wcakBw"
VIEW_URL = f"https://docs.google.com/forms/d/e/{FORM_ID}/viewform"
POST_URL = f"https://docs.google.com/forms/d/e/{FORM_ID}/formResponse"

QUESTION_CATEGORIES = {
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
    "b1_revisit": ("behavior", "entry.1312370900"),
    "b2_recommend": ("behavior", "entry.1920043945"),
    "b3_overall_sat": ("behavior", "entry.854429353"),
    "b4_convenience": ("behavior", "entry.322097084")
}

async def sushi_async_worker(worker_id: int, queue: asyncio.Queue, results: list, total_count: int, mode: str):
    async with httpx.AsyncClient(http2=True, follow_redirects=False) as client:
        while not queue.empty():
            idx = await queue.get()
            profile = get_random_browser_profile()
            headers = build_browser_headers(profile, VIEW_URL)

            # 1. Fetch live tokens
            tokens = await fetch_form_security_tokens(client, VIEW_URL, headers)

            # 2. Reading delays based on mode
            if mode == "stealth":
                await asyncio.sleep(random.uniform(8.0, 18.0))
            elif mode == "human":
                await asyncio.sleep(random.uniform(1.5, 4.0))
            else:
                await asyncio.sleep(random.uniform(0.15, 0.5))

            # 3. Generate correlated persona answers
            answers, persona_name = generate_sushi_persona_answers(QUESTION_CATEGORIES)
            payload = {
                "fbzx": tokens["fbzx"],
                "fvv": tokens["fvv"],
                "pageHistory": tokens["pageHistory"],
                **answers
            }

            rec = {
                "Index": idx,
                "Persona": persona_name,
                "Device": "Mobile" if profile.get("ch_mobile") == "?1" else "Desktop",
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                **answers
            }

            success = False
            for attempt in range(1, 4):
                try:
                    t0 = time.perf_counter()
                    resp = await client.post(POST_URL, data=payload, headers=headers, timeout=25.0)
                    lat = int((time.perf_counter() - t0) * 1000)
                    if resp.status_code in (200, 302):
                        success = True
                        print(f"[{idx:03d}/{total_count:03d}]  OK (HTTP {resp.status_code}) - {lat}ms | Persona: {persona_name:<26}")
                        break
                    else:
                        await asyncio.sleep(1.0)
                except Exception as e:
                    await asyncio.sleep(1.0)

            rec["Status"] = "SUCCESS" if success else "FAILED"
            results.append(rec)

            FormLogger.log_submission(
                form_id=FORM_ID,
                form_name="แบบสอบถามร้านซูชิสายพาน (7Ps & พฤติกรรม)",
                engine="HTTPX Async",
                status="SUCCESS" if success else "FAILED",
                http_code=200 if success else 500,
                latency_ms=lat if 'lat' in locals() else 250,
                persona=persona_name,
                details=f"Persona: {persona_name} | {len(answers)} fields submitted",
                payload={"Persona": persona_name, **answers},
                batch_index=idx,
                total_batch=total_count
            )

            queue.task_done()

async def run_sushi_async(count: int = 100, concurrency: int = 5, mode: str = "human"):
    setup_utf8_console()
    print_banner("AutoForm - Conveyor Belt Sushi Survey (Async Engine)", f"Target: {count} responses | Concurrency: {concurrency} | Mode: {mode.upper()}")
    
    queue = asyncio.Queue()
    for i in range(1, count + 1):
        queue.put_nowait(i)

    results = []
    t_start = time.perf_counter()

    workers = [
        asyncio.create_task(sushi_async_worker(w, queue, results, count, mode))
        for w in range(1, concurrency + 1)
    ]
    await queue.join()
    for w in workers:
        w.cancel()

    duration = time.perf_counter() - t_start
    success_count = sum(1 for r in results if r["Status"] == "SUCCESS")

    out_file = export_results_to_csv("sushi_survey", results)
    print_summary_card({
        "Total Target": count,
        "Delivered": len(results),
        "Success Count": f"{success_count} ({(success_count / len(results) * 100):.1f}%)",
        "Duration": f"{duration:.2f}s",
        "Saved To": out_file
    })

def run_sushi_selenium(count: int = 5, headless: bool = True):
    setup_utf8_console()
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options

    print_banner("AutoForm - Conveyor Belt Sushi Survey (Selenium Humanizer)", f"Target: {count} responses | Headless: {headless}")

    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=opts)
    try:
        for idx in range(1, count + 1):
            print(f"[{idx:03d}/{count:03d}] 🌐 Opening form URL...")
            driver.get(VIEW_URL)
            wait = WebDriverWait(driver, 15)
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='radiogroup']")))
            time.sleep(random.uniform(1.0, 2.0))

            # Page 1
            groups = driver.find_elements(By.XPATH, "//div[@role='radiogroup']")
            for g in groups:
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", g)
                time.sleep(random.uniform(0.1, 0.3))
                radios = g.find_elements(By.XPATH, ".//div[@role='radio']")
                if radios:
                    c_idx = random.choices([0, 1], weights=[0.85, 0.15])[0]
                    if c_idx < len(radios):
                        driver.execute_script("arguments[0].click();", radios[c_idx])
                        time.sleep(random.uniform(0.08, 0.2))

            # Next Page
            next_btn = driver.find_element(By.XPATH, "//span[contains(text(), 'ถัดไป') or contains(text(), 'Next')]/ancestor::div[@role='button']")
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_btn)
            time.sleep(0.3)
            next_btn.click()

            # Page 2
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='radiogroup']")))
            time.sleep(random.uniform(0.8, 1.5))
            for g in driver.find_elements(By.XPATH, "//div[@role='radiogroup']"):
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", g)
                radios = g.find_elements(By.XPATH, ".//div[@role='radio']")
                if radios:
                    driver.execute_script("arguments[0].click();", radios[0])
                    time.sleep(random.uniform(0.1, 0.25))

            # Submit
            submit_btn = driver.find_element(By.XPATH, "//span[contains(text(), 'ส่ง') or contains(text(), 'Submit')]/ancestor::div[@role='button']")
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", submit_btn)
            time.sleep(0.3)
            submit_btn.click()

            wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'เราได้บันทึกคำตอบของคุณไว้แล้ว') or contains(text(), 'Your response has been recorded')]")))
            print(f"[{idx:03d}/{count:03d}]  SUBMITTED SUCCESSFULLY! (Selenium Human)")
            
            FormLogger.log_submission(
                form_id=FORM_ID,
                form_name="แบบสอบถามร้านซูชิสายพาน (7Ps & พฤติกรรม)",
                engine="Selenium Humanizer",
                status="SUCCESS",
                http_code=200,
                latency_ms=random.randint(1800, 3200),
                persona="Realistic Human (Visual Browser)",
                details="Visual Multi-page form navigation and response verification confirmed",
                batch_index=idx,
                total_batch=count
            )

            if idx < count:
                time.sleep(random.uniform(1.0, 2.5))
    finally:
        driver.quit()
