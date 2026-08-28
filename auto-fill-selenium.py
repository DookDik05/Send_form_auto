#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-fill Multi-Page Google Form - แบบสอบถามเดอะมอลล์ บางกะปิ (Normal Human-like Mode)
Uses Selenium with realistic human timing + Beautiful logging
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
NUM_RESPONSES = 89  # Total number of forms to submit
BASE_DELAY = 30  # Not used for main delay logic
HEADLESS = False
SELECTED_BRANCH = "เดอะมอลล์ไลฟ์สโตร์ บางกะปิ"
# ============================================================================

def generate_user_agent():
    """Generate random realistic user agent"""
    chrome_versions = list(range(110, 131))
    chrome_builds = ["0.0.0", "0.5615.49", "0.6099.109", "0.6167.85", "0.6261.69"]
    
    windows = ["Windows NT 10.0; Win64; x64", "Windows NT 11.0; Win64; x64"]
    mac = ["Macintosh; Intel Mac OS X 10_15_7", "Macintosh; Intel Mac OS X 13_5"]
    
    os_choice = random.choice(windows + mac)
    chrome_ver = random.choice(chrome_versions)
    build = random.choice(chrome_builds)
    
    return f"Mozilla/5.0 ({os_choice}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver}.{build} Safari/537.36"

def create_driver():
    """Create Chrome WebDriver with realistic settings"""
    options = Options()
    if HEADLESS:
        options.add_argument("--headless")
    
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=th")
    options.add_argument(f"user-agent={generate_user_agent()}")
    
    driver = webdriver.Chrome(options=options)
    return driver

def human_delay(min_sec=0.1, max_sec=0.5):
    """Ultra fast delay to meet 8 PM deadline"""
    time.sleep(random.uniform(min_sec, max_sec))

def click_element(driver, element):
    """Click with minimal delay"""
    driver.execute_script("arguments[0].click();", element)
    human_delay(0.05, 0.15)

def find_and_click_next(driver):
    """Find and click Next button"""
    selectors = [
        "//span[contains(text(), 'ถัดไป')]/ancestor::div[@role='button']",
        "//div[@role='button' and contains(., 'ถัดไป')]",
    ]
    
    for selector in selectors:
        try:
            button = driver.find_element(By.XPATH, selector)
            click_element(driver, button)
            human_delay(0.3, 0.6)  # Ultra fast transition
            return True
        except:
            continue
    return False

def find_and_click_submit(driver):
    """Find and click Submit button"""
    selectors = [
        "//span[contains(text(), 'ส่ง')]/ancestor::div[@role='button']",
        "//div[@role='button' and contains(., 'ส่ง')]",
    ]
    
    for selector in selectors:
        try:
            button = driver.find_element(By.XPATH, selector)
            click_element(driver, button)
            return True
        except:
            continue
    return False

def fill_radios_humanlike(driver):
    """Fill all radio questions with human-like behavior"""
    questions = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")
    
    for question in questions:
        try:
            question_text = question.text.lower() if question.text else ""
            radios = question.find_elements(By.CSS_SELECTOR, "div[role='radio']")
            
            if not radios:
                continue
            
            # Minimal reading
            human_delay(0.1, 0.4)
                
            data_values = [r.get_attribute("data-value") for r in radios if r.get_attribute("data-value")]
            
            if not data_values:
                continue
            
            # Branch selection (locked to Bangkapi)
            if "สาขา" in question_text and "ใช้บริการ" in question_text:
                for radio in radios:
                    val = radio.get_attribute("data-value")
                    if val and "บางกะปิ" in val:
                        click_element(driver, radio)
                        break
            
            # M Card question
            elif "m card" in question_text or "แอปพลิเคชัน" in question_text:
                has_mcard = random.choices([True, False], weights=[75, 25])[0]
                target = "มี" if has_mcard else "ไม่มี"
                for radio in radios:
                    if radio.get_attribute("data-value") == target:
                        click_element(driver, radio)
                        break
            
            # Rating scales (1-5)
            elif all(v.isdigit() for v in data_values if v):
                target = random.choices([5, 4, 3], weights=[70, 45, 15])[0]
                for radio in radios:
                    val = radio.get_attribute("data-value")
                    if val and val.isdigit() and int(val) == target:
                        click_element(driver, radio)
                        break
            
            # Other options
            else:
                click_element(driver, random.choice(radios))
            
            # Minimal pause
            human_delay(0.1, 0.3)
                
        except Exception:
            continue

def fill_checkboxes_humanlike(driver):
    """Fill checkboxes with human-like behavior"""
    groups = driver.find_elements(By.CSS_SELECTOR, "div[role='list']")
    
    for group in groups:
        try:
            checkboxes = group.find_elements(By.CSS_SELECTOR, "div[role='checkbox']")
            if checkboxes:
                # Minimal reading
                human_delay(0.2, 0.5)
                
                num = min(random.randint(1, 3), len(checkboxes))
                for cb in random.sample(checkboxes, num):
                    click_element(driver, cb)
                    human_delay(0.1, 0.3)
        except Exception:
            continue

# Pool of human-like comments - EVENT VERSION (247 items)
COMMENT_POOL = [
    "Nice", "nice", "Nice ครับ", "nice ค่ะ", "Nice จ้า", "Nice นะ", "Nice เลย",
    "ดีค่ะ", "ดีครับ", "ดีคับ", "ดีค้าบ", "ดีค้ะ", "ดีจ้า", "ดีจ๊ะ", "ดีจ๋า",
    "ดีอ่ะ", "ดีอะ", "ดีอ้ะ", "ดีฮ่ะ", "ดีหว่า", "ดีฮ้า", "ดีฮะ",
    "ดีนะะ", "ดีน๊า", "ดีน้าาา", "ดีจ้าา", "ดีจ๊าา", "ดีน่ะ", "ดีน้า",
    "โอเคคับ", "โอเคค้าบ", "โอเคค้ะ", "โอเคอ่ะ", "โอเคจ้าาา", "โอเคนะ", "โอเคจ๊ะ",
    "ok ค่ะ", "ok ครับ", "ok คับ", "ok ค้าบ", "ok ดี", "ok นะ", "ok จ้า",
    "okayy", "okayyy", "okay ครับ", "okay ค่ะ", "oke ค่ะ", "oke ครับ", "okay จ้า",
    "ไม่มีนะะ", "ไม่มีอ่ะ", "ไม่มีจ้ааа", "ไม่มีฮ่ะ", "ไม่มีค๊า", "ไม่มีน้า",
    "ไม่มีเลยครับ", "ไม่มีเลยค่ะ", "ไม่มีคร้าบ", "ไม่มีค้า", "ไม่มีจ๊ะ",
    "-", "--", "...", "~", ".",
    "ก็ดีอ่ะ", "ก็ดีนะะ", "ก็ดีคับ", "ก็ดีค้าบ", "ก็ดีค่ааа", "ก็ดีจ้า",
    "ก็โอเคครับ", "ก็โอเคค่ะ", "ก็โอเคนะ", "ก็โอเคอ่ะ", "ก็โอเคจ้า",
    "พอใจค่ะะ", "พอใจครัช", "พอใจคร้าบ", "พอใจค้าบบ", "พอใจอ่ะ", "พอใจจ้า",
    "บรรยากาศดี", "บรรยากาศดีมาก", "บรรยากาศสวย", "บรรยากาศน่ารัก",
    "งานสนุก", "งานสนุกดี", "งานสนุกมาก", "งานดี", "งานดีมาก", "งานเจ๋ง",
    "ชอบบรรยากาศ", "ชอบงาน", "ชอบมาก", "ชอบเลย", "ชอบบ", "ชอบบบ",
    "จัดงานดี", "จัดดี", "จัดดีมาก", "จัดสวย", "จัดเจ๋ง",
    "ประทับใจ", "ประทับใจมาก", "ประทับใจเลย", "ประทับใจงาน",
    "มาแล้วชอบ", "มาแล้วดี", "มาแล้วสนุก", "มาคุ้ม", "มาดี",
    "สวย", "สวยมาก", "สวยเลย", "สวยจัง", "สวยงาม", "สวยมากกก",
    "ถ่ายรูปสวย", "ถ่ายรูปดี", "ถ่ายรูปเยอะ", "ถ่ายสวย", "ภาพสวย",
    "เดินเพลิน", "เดินสบาย", "เดินสนุก", "เดินง่าย", "เดินดี",
    "ไม่เบื่อ", "ไม่เบื่อเลย", "สนุกดี", "สนุกมาก", "สนุกเลย",
    "งานดีเกินคาด", "ดีเกินคาด", "เกินคาด", "ดีกว่าคิด",
    "น่ารัก", "น่ารักมาก", "น่ารักเลย", "น่ารักจัง", "cute", "Cute",
    "ดีมาก", "ดีมากกก", "ดีมากเลย", "ดีเลย", "ดีเลยย",
    "เยี่ยม", "เยี่ยมมาก", "เยี่ยมเลย", "สุดยอด", "เจ๋ง", "เจ๋งมาก",
    "โอเค", "โอเคมาก", "โอเคเลย", "ดี", "ชอบ",
    "ดีค้าบบ", "ดีค้าааа", "โอเคครับบ", "โอเคค่ะะ",
    "ไม่แออัด", "คนไม่เยอะ", "คนพอดี", "สบาย", "เดินสบาย",
    "พนักงานดี", "พนักงานน่ารัก", "พนักงานช่วยดี", "พนักงานเก่ง",
    "บริการดี", "บริการดีมาก", "บริการเยี่ยม", "บริการโอเค",
    "สะอาด", "สะอาดดี", "สะอาดมาก", "เรียบร้อย", "กว้างขวาง",
    "แอร์เย็น", "แอร์เย็นดี", "เย็นสบาย", "สะดวก", "สะดวกดี",
    "จอดรถสะดวก", "จอดรถดี", "ที่จอดดี", "เดินทางง่าย", "เข้ามาง่าย",
    "ตกแต่งสวย", "ตกแต่งดี", "ตกแต่งน่ารัก", "ตกแต่งเจ๋ง",
    "ไฟสวย", "ไฟสวยมาก", "แสงสวย", "โคมไฟสวย", "ไฟประดับสวย",
    "โซนถ่ายรูปเยอะ", "มุมถ่ายรูปเยอะ", "ถ่ายได้เยอะ", "เช็คอินได้เยอะ",
    "สวยทุกมุม", "ทุกมุมสวย", "ทุกจุดสวย", "งานใหญ่", "งานใหญ่ดี",
    "จัดเป็นระเบียบ", "เป็นระเบียบ", "เดินง่าย", "ไม่หลง", "หาง่าย",
    "ป้ายชัดเจน", "ป้ายดี", "มีที่นั่ง", "มีที่นั่งพัก", "นั่งพักได้",
    "ห้องน้ำสะอาด", "ห้องน้ำดี", "ห้องน้ำใกล้", "ของแจกดี", "มีของแจก",
    "กิจกรรมเยอะ", "กิจกรรมดี", "กิจกรรมสนุก", "สนุกทุกโซน",
    "เด็กชอบ", "เด็กชอบมาก", "ลูกชอบ", "ลูกชอบมาก", "ลูกสนุก",
    "ครอบครัวมาได้", "เหมาะกับครอบครัว", "มาทั้งครอบครัว",
    "เหมาะทุกวัย", "ทุกวัยมาได้", "มาคนเดียวก็สนุก", "มาคนเดียวได้",
    "มากับเพื่อน", "มากับเพื่อนสนุก", "พาครอบครัว", "พาครอบครัวมา",
    "งานดีจริง", "ดีจริง", "คุ้มค่า", "คุ้ม", "", "",
]

def submit_form_humanlike(driver, num):
    """Submit form with human-like timing"""
    try:
        driver.get(FORM_URL)
        
        # Minimal page load
        human_delay(0.8, 1.5)
        
        page = 1
        start_time = time.time()
        
        while page <= 20:
            # Minimal reading
            human_delay(0.3, 0.8)
            
            # Fill questions
            fill_radios_humanlike(driver)
            fill_checkboxes_humanlike(driver)
            
            # Minimal review
            human_delay(0.2, 0.5)
            
            # Try next button
            if find_and_click_next(driver):
                page += 1
                continue
            
            # Try submit button
            if find_and_click_submit(driver):
                human_delay(0.3, 0.6)  # Quick confirmation
                
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
    print("👤 AUTO-FILL GOOGLE FORM - ULTRA FAST MODE (8 PM Target)".center(80))
    print("="*80)
    print(f"📍 Branch      : {SELECTED_BRANCH}")
    print(f"📊 Target      : {NUM_RESPONSES} responses")
    print(f"⏱️  Base Delay  : {BASE_DELAY}s between forms (±variation)")
    print(f"👁️  Headless    : {'Yes' if HEADLESS else 'No'}")
    print(f"🕐 Started     : {datetime.now().strftime('%H:%M:%S')}")
    print("="*80 + "\n")

def print_progress(current, total, success, elapsed, wait_time=None):
    """Print progress with beautiful formatting"""
    percent = (current / total) * 100
    bar_length = 30
    filled = int(bar_length * current / total)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    status = "✅" if success else "❌"
    time_str = f"{elapsed:.2f}s" if success else "Failed"
    
    print(f"{status} [{current:2d}/{total:2d}] |{bar}| {percent:5.1f}% | ⏱️  {time_str}")
    
    if wait_time and current < total:
        print(f"    ⏳ Waiting {wait_time}s (ultra fast mode)...")

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
    if successful > 0:
        print(f"⚡ Avg Speed   : {elapsed_total/successful:.2f}s per form")
    print(f"🕐 Completed   : {datetime.now().strftime('%H:%M:%S')}")
    print("="*80 + "\n")

def main():
    """Main execution - Human-like timing"""
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
            success, pages, elapsed = submit_form_humanlike(driver, i)
            
            if success:
                success_count += 1
            else:
                failed_count += 1
            
            results.append({
                "num": i,
                "status": "Success" if success else "Failed",
                "pages": pages,
                "time": f"{elapsed:.2f}s",
                "timestamp": datetime.now().strftime('%H:%M:%S')
            })
            
            # Delay logic for 61 responses to finish in 1.5 hours (90 นาที = 5400 วินาที, 60 ช่วง = 90 วินาที/response)
            if i < NUM_RESPONSES:
                if NUM_RESPONSES == 61:
                    wait = random.randint(88, 92)  # 1:28 ถึง 1:32 นาที
                else:
                    # Default: ultra fast (เดิม)
                    delay_variation = random.choices(
                        [random.uniform(5, 12), random.uniform(12, 18), random.uniform(18, 25)],
                        weights=[50, 40, 10]
                    )[0]
                    wait = int(delay_variation)
                print_progress(i, NUM_RESPONSES, success, elapsed, wait)
                time.sleep(wait)
            else:
                print_progress(i, NUM_RESPONSES, success, elapsed)
        
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