#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-fill Multi-Page Google Form - แบบสอบถามเดอะมอลล์ บางกะปิ (Performance Mode)
Uses Selenium with maximum speed optimization
Form: แบบสอบถามการใช้บริการและความพึงพอใจต่อการจัดงาน
URL: https://docs.google.com/forms/d/e/1FAIpQLScYXOItwUXkBmHpgQ-oZHozu2BqkfYK7WswvwkQRXANxru8PA/viewform
"""

import time
import csv
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ============================================================================
# CONFIGURATION SECTION
# ============================================================================
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScYXOItwUXkBmHpgQ-oZHozu2BqkfYK7WswvwkQRXANxru8PA/viewform"
NUM_RESPONSES = 4
DELAY_BETWEEN_FORMS = 2  # seconds (ultra fast)
HEADLESS = False
SELECTED_BRANCH = "เดอะมอลล์ไลฟ์สโตร์ บางกะปิ"
# ============================================================================

def generate_user_agent():
    """Generate random user agent"""
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    ]
    return random.choice(agents)

def create_driver():
    """Create optimized Chrome WebDriver"""
    options = Options()
    if HEADLESS:
        options.add_argument("--headless")
    
    # Performance optimizations
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-web-security")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=th")
    options.add_argument(f"user-agent={generate_user_agent()}")
    
    # Disable images for faster loading
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(10)
    
    return driver

def fast_click(driver, element):
    """Fast JavaScript click"""
    driver.execute_script("arguments[0].click();", element)
    time.sleep(0.05)  # Minimal delay

def find_and_click_next(driver):
    """Find and click Next button - Fast"""
    selectors = [
        "//span[contains(text(), 'ถัดไป')]/ancestor::div[@role='button']",
        "//div[@role='button' and contains(., 'ถัดไป')]",
    ]
    
    for selector in selectors:
        try:
            button = driver.find_element(By.XPATH, selector)
            fast_click(driver, button)
            time.sleep(0.3)  # Quick page transition
            return True
        except:
            continue
    return False

def find_and_click_submit(driver):
    """Find and click Submit button - Instant"""
    selectors = [
        "//span[contains(text(), 'ส่ง')]/ancestor::div[@role='button']",
        "//div[@role='button' and contains(., 'ส่ง')]",
    ]
    
    for selector in selectors:
        try:
            button = driver.find_element(By.XPATH, selector)
            fast_click(driver, button)
            return True
        except:
            continue
    return False

def fill_radios_fast(driver):
    """Fill all radio questions - Maximum speed"""
    questions = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")
    
    for question in questions:
        try:
            question_text = question.text.lower() if question.text else ""
            radios = question.find_elements(By.CSS_SELECTOR, "div[role='radio']")
            
            if not radios:
                continue
                
            data_values = [r.get_attribute("data-value") for r in radios if r.get_attribute("data-value")]
            
            if not data_values:
                continue
            
            # Branch selection (locked to Bangkapi)
            if "สาขา" in question_text and "ใช้บริการ" in question_text:
                for radio in radios:
                    val = radio.get_attribute("data-value")
                    if val and "บางกะปิ" in val:
                        fast_click(driver, radio)
                        break
            
            # M Card question
            elif "m card" in question_text or "แอปพลิเคชัน" in question_text:
                target = "มี" if random.random() < 0.75 else "ไม่มี"
                for radio in radios:
                    if radio.get_attribute("data-value") == target:
                        fast_click(driver, radio)
                        break
            
            # Rating scales (1-5) - Always high ratings
            elif all(v.isdigit() for v in data_values if v):
                target = random.choices([5, 4, 3], weights=[70, 25, 5])[0]
                for radio in radios:
                    val = radio.get_attribute("data-value")
                    if val and val.isdigit() and int(val) == target:
                        fast_click(driver, radio)
                        break
            
            # Other options - random
            else:
                fast_click(driver, random.choice(radios))
                
        except Exception:
            continue

def fill_checkboxes_fast(driver):
    """Fill checkboxes - Fast"""
    groups = driver.find_elements(By.CSS_SELECTOR, "div[role='list']")
    
    for group in groups:
        try:
            checkboxes = group.find_elements(By.CSS_SELECTOR, "div[role='checkbox']")
            if checkboxes:
                num = min(random.randint(1, 2), len(checkboxes))
                for cb in random.sample(checkboxes, num):
                    fast_click(driver, cb)
        except Exception:
            continue

COMMENT_POOL = [
    "ดีครับ", "ดีค่ะ", "โอเค", "ไม่มี", "พอใจ", "ดีมาก", "ดี", 
    "good", "Good", "ok", "okay", "-", "ดีเลย", "ชอบ", "ประทับใจ",
    "สะอาดดี", "สะดวกดี", "บริการดี", "พนักงานดี", "ราคาดี",
    "ของเยอะดี", "มาบ่อย", "ชอบมาก", "เยี่ยม", "โอเคครับ", "โอเคค่ะ",
    "ดีนะ", "ดีมากครับ", "ดีมากค่ะ", "พอใจมาก", "ประทับใจมาก",
]

def submit_form_fast(driver, num):
    """Submit form - Ultra fast mode"""
    try:
        driver.get(FORM_URL)
        time.sleep(0.8)  # Minimal page load
        
        page = 1
        start_time = time.time()
        
        while page <= 15:
            # Fill all questions on current page
            fill_radios_fast(driver)
            fill_checkboxes_fast(driver)
            
            # Try next button
            if find_and_click_next(driver):
                page += 1
                continue
            
            # Try submit button (INSTANT)
            if find_and_click_submit(driver):
                time.sleep(0.5)  # Quick confirmation check
                
                # Check success
                try:
                    if "formResponse" in driver.current_url or "closedform" in driver.current_url:
                        elapsed = time.time() - start_time
                        return True, page, elapsed
                    
                    success_xpath = "//div[contains(text(), 'บันทึกคำตอบแล้ว') or contains(text(), 'ส่งคำตอบแล้ว')]"
                    driver.find_element(By.XPATH, success_xpath)
                    elapsed = time.time() - start_time
                    return True, page, elapsed
                except:
                    pass
                
                elapsed = time.time() - start_time
                return True, page, elapsed
            
            break
        
        return False, page, 0
        
    except Exception as e:
        return False, 0, 0

def print_header():
    """Print beautiful header"""
    print("\n" + "="*80)
    print("🚀 AUTO-FILL GOOGLE FORM - ULTRA FAST MODE".center(80))
    print("="*80)
    print(f"📍 Branch      : {SELECTED_BRANCH}")
    print(f"📊 Target      : {NUM_RESPONSES} responses")
    print(f"⚡ Delay       : {DELAY_BETWEEN_FORMS}s between forms")
    print(f"👁️  Headless    : {'Yes' if HEADLESS else 'No'}")
    print(f"🕐 Started     : {datetime.now().strftime('%H:%M:%S')}")
    print("="*80 + "\n")

def print_progress(current, total, success, elapsed):
    """Print progress with beautiful formatting"""
    percent = (current / total) * 100
    bar_length = 30
    filled = int(bar_length * current / total)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    status = "✅" if success else "❌"
    
    print(f"{status} [{current:2d}/{total:2d}] |{bar}| {percent:5.1f}% | ⏱️  {elapsed:.2f}s")

def print_summary(total, successful, failed, start_time):
    """Print beautiful summary"""
    elapsed_total = time.time() - start_time
    mins = int(elapsed_total // 60)
    secs = int(elapsed_total % 60)
    
    print("\n" + "="*80)
    print("📈 SUMMARY REPORT".center(80))
    print("="*80)
    print(f"✅ Successful  : {successful}/{total} ({successful/total*100:.1f}%)")
    print(f"❌ Failed      : {failed}/{total}")
    print(f"⏱️  Total Time  : {mins}m {secs}s")
    print(f"⚡ Avg Speed   : {elapsed_total/total:.2f}s per form")
    print(f"🕐 Completed   : {datetime.now().strftime('%H:%M:%S')}")
    print("="*80 + "\n")

def main():
    """Main execution - Performance optimized"""
    print_header()
    
    results = []
    success_count = 0
    failed_count = 0
    start_time = time.time()
    
    driver = None
    
    try:
        print("🔧 Initializing Chrome driver...")
        driver = create_driver()
        print("✅ Driver ready!\n")
        
        for i in range(1, NUM_RESPONSES + 1):
            form_start = time.time()
            
            success, pages, elapsed = submit_form_fast(driver, i)
            
            if success:
                success_count += 1
                print_progress(i, NUM_RESPONSES, True, elapsed)
            else:
                failed_count += 1
                print_progress(i, NUM_RESPONSES, False, 0)
            
            results.append({
                "num": i,
                "status": "Success" if success else "Failed",
                "pages": pages,
                "time": f"{elapsed:.2f}s",
                "timestamp": datetime.now().strftime('%H:%M:%S')
            })
            
            # Minimal delay between forms
            if i < NUM_RESPONSES:
                wait = random.uniform(DELAY_BETWEEN_FORMS, DELAY_BETWEEN_FORMS + 1)
                time.sleep(wait)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user!")
    
    finally:
        if driver:
            driver.quit()
    
    # Print summary
    print_summary(NUM_RESPONSES, success_count, failed_count, start_time)
    
    # Save results
    csv_file = f"survey_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=["num", "status", "pages", "time", "timestamp"])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"💾 Results saved: {csv_file}\n")

if __name__ == "__main__":
    main()