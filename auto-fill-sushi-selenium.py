#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-fill Google Form: แบบสอบถามร้านซูชิสายพาน (Selenium Realistic Human Browser)
Features:
  - Real Chrome Headless / Visual Automation
  - Human Scrolling & Mouse Action Simulation
  - Randomized Thinking Delays per question
  - Multi-page navigation (คลิกถัดไป -> ส่ง)
"""

import time
import random
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Windows Console UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# ============================================================================
# CONFIGURATION
# ============================================================================
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfVCqzAoQZkyfPxRpkme_HV_7I_ZcoZxXjODZiAIQm8wcakBw/viewform"
NUM_RESPONSES = int(sys.argv[1]) if len(sys.argv) > 1 else 10
HEADLESS = True  # เปลี่ยนเป็น False เพื่อดู Chrome รันแบบสดๆ

def get_driver():
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Modern User-Agents
    uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ]
    options.add_argument(f"user-agent={random.choice(uas)}")
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

def fill_sushi_form_human(driver, run_idx):
    print(f"[{run_idx:03d}/{NUM_RESPONSES:03d}] 🌐 Opening form URL...")
    driver.get(FORM_URL)
    wait = WebDriverWait(driver, 15)
    
    # รอจนคำถามแรกโหลดขึ้นมา
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='listitem' or @role='radiogroup']")))
    time.sleep(random.uniform(1.2, 2.5)) # Human initial reading delay

    # 1. จัดการคำถามหน้าแรก (Part 1: 7Ps)
    radio_groups = driver.find_elements(By.XPATH, "//div[@role='radiogroup']")
    print(f"  • Found {len(radio_groups)} questions on Page 1. Filling answers...")

    for i, group in enumerate(radio_groups):
        # สุ่มเลื่อนหน้าจอลงมาอย่างเป็นธรรมชาติ
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", group)
        time.sleep(random.uniform(0.15, 0.45))

        radios = group.find_elements(By.XPATH, ".//div[@role='radio']")
        if radios:
            # สุ่มเลือกแบบเน้นคะแนน 5 (มากที่สุด) หรือ 4 (มาก)
            # radios index: 0 = 5 ดาว, 1 = 4 ดาว, 2 = 3 ดาว, 3 = 2 ดาว, 4 = 1 ดาว
            chosen_idx = random.choices([0, 1, 2], weights=[0.82, 0.16, 0.02])[0]
            if chosen_idx < len(radios):
                target_radio = radios[chosen_idx]
                try:
                    target_radio.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", target_radio)
                time.sleep(random.uniform(0.1, 0.35))

    # กดปุ่ม "ถัดไป" (Next Page)
    time.sleep(random.uniform(0.8, 1.6))
    next_btn = driver.find_element(By.XPATH, "//span[contains(text(), 'ถัดไป') or contains(text(), 'Next')]/ancestor::div[@role='button']")
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_btn)
    time.sleep(0.3)
    next_btn.click()
    print("  • Navigated to Page 2 (Consumer Behavior)...")

    # 2. จัดการคำถามหน้า 2 (Part 2: พฤติกรรมผู้บริโภค)
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='radiogroup']")))
    time.sleep(random.uniform(0.8, 1.5))
    
    page2_groups = driver.find_elements(By.XPATH, "//div[@role='radiogroup']")
    for group in page2_groups:
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", group)
        time.sleep(random.uniform(0.15, 0.4))
        radios = group.find_elements(By.XPATH, ".//div[@role='radio']")
        if radios:
            chosen_idx = random.choices([0, 1], weights=[0.88, 0.12])[0]
            if chosen_idx < len(radios):
                target_radio = radios[chosen_idx]
                try:
                    target_radio.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", target_radio)
                time.sleep(random.uniform(0.1, 0.3))

    # กดปุ่ม "ส่ง" (Submit)
    time.sleep(random.uniform(0.8, 1.8))
    submit_btn = driver.find_element(By.XPATH, "//span[contains(text(), 'ส่ง') or contains(text(), 'Submit')]/ancestor::div[@role='button']")
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", submit_btn)
    time.sleep(0.4)
    submit_btn.click()

    # รอหน้ายืนยันการส่ง
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'เราได้บันทึกคำตอบของคุณไว้แล้ว') or contains(text(), 'Your response has been recorded')]")))
    print(f"[{run_idx:03d}/{NUM_RESPONSES:03d}]  SUBMITTED SUCCESSFULLY! (Human Selenium)\n")

def main():
    print("=" * 68)
    print("🤖 AutoForm Selenium Humanizer - Sushi Survey")
    print(f"🎯 Target: {NUM_RESPONSES} responses | Headless Mode: {HEADLESS}")
    print("=" * 68 + "\n")

    driver = get_driver()
    try:
        for i in range(1, NUM_RESPONSES + 1):
            fill_sushi_form_human(driver, i)
            # หน่วงเวลาระหว่างรอบ 1.5 - 3.5 วินาที
            if i < NUM_RESPONSES:
                time.sleep(random.uniform(1.5, 3.5))
    finally:
        driver.quit()
        print("🎉 All Selenium Humanizer Submissions Completed!")

if __name__ == "__main__":
    main()
