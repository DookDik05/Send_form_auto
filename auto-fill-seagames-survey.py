#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-fill Google Form - แบบประเมินความพึงพอใจ กิจกรรมสร้างกระแสการรับรู้ ซีเกมส์ 33
Uses Selenium with realistic human timing
Form: แบบประเมินความพึงพอใจ กิจกรรม "INSPIRE THE GAME คลินิกกีฬา ปลุกพลังฝัน"
URL: https://docs.google.com/forms/d/e/1FAIpQLSeklchUtv4O-H1SpMgWkBm1RVVJWgqqNO4KZeBeqaEtQt_UAg/viewform
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
from selenium.webdriver.common.action_chains import ActionChains

# ============================================================================
# CONFIGURATION SECTION
# ============================================================================
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdtJkrUm9-pHPOqWlDQ-oYx_b8FJaBo8G_4fOTmWpzMC8XrFA/viewform"
NUM_RESPONSES = 80  # จำนวนฟอร์มที่ต้องการส่ง
HEADLESS = True    # ตั้งเป็น True เพื่อรันโดยไม่เปิดหน้าต่าง
# ============================================================================

# CSS Selectors
RADIO_SELECTOR = "div[role='radio']"
CHECKBOX_SELECTOR = "div[role='checkbox']"

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
    options = Options()

    # === Headless (ใหม่ของ Chrome เร็วกว่าแบบเก่า) ===
    options.add_argument("--headless=new")

    # === Performance Kill Switches ===
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ปิดของไม่จำเป็น
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-translate")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--mute-audio")

    # ปิดรูปภาพ (impact สูง)
    options.add_argument("--blink-settings=imagesEnabled=false")

    # Window + language
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=th-TH")

    # Random realistic UA
    options.add_argument(f"user-agent={generate_user_agent()}")

    driver = webdriver.Chrome(options=options)
    return driver

def human_delay(min_sec=0, max_sec=0.05):
    """Absolute minimum delay"""
    time.sleep(random.uniform(min_sec, max_sec))

def human_like_click(driver, element):
    """Click element with human-like behavior - move to element first"""
    try:
        # Scroll element into view
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        human_delay(0.2, 0.4)
        
        # Move to element and click
        actions = ActionChains(driver)
        actions.move_to_element(element)
        actions.pause(random.uniform(0.1, 0.3))
        actions.click()
        actions.perform()
        
        human_delay(0.1, 0.3)
    except Exception:
        # Fallback to JS click
        driver.execute_script("arguments[0].click();", element)
        human_delay(0.1, 0.2)


def get_checkbox_label(checkbox):
    """Get the label/value of a checkbox - uses data-answer-value or aria-label"""
    label = checkbox.get_attribute("data-answer-value")
    if not label:
        label = checkbox.get_attribute("aria-label")
    if not label:
        label = checkbox.text
    return label or ""


def select_radio_by_keyword(driver, question_container, keyword):
    """Select a radio option that contains the keyword - improved version"""
    try:
        # Scroll to question container first
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", question_container)
        time.sleep(0.2)  # Short wait after scroll
        
        radios = question_container.find_elements(By.CSS_SELECTOR, RADIO_SELECTOR)
        if not radios:
            return False
        
        for radio in radios:
            val = radio.get_attribute("data-value") or ""
            aria = radio.get_attribute("aria-label") or ""
            text = radio.text or ""
            
            # Check if keyword matches any of the possible labels
            if keyword in val or keyword in aria or keyword in text:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio)
                time.sleep(0.1)
                driver.execute_script("arguments[0].click();", radio)
                return True
        
    except Exception as e:
        print(f"Radio error: {e}")
    return False


def select_single_checkbox_by_keyword(driver, question_container, keyword):
    """Select exactly ONE checkbox that matches the keyword (for single-choice checkbox questions like 2.3)"""
    try:
        checkboxes = question_container.find_elements(By.CSS_SELECTOR, CHECKBOX_SELECTOR)
        for cb in checkboxes:
            label = get_checkbox_label(cb)
            if keyword in label:
                human_like_click(driver, cb)
                return True
    except Exception as e:
        print(f"Single checkbox error: {e}")
    return False


def select_multiple_checkboxes(driver, question_container, target_keywords, min_select=1, max_select=3, exclude_keywords=None):
    """
    Select multiple checkboxes that match target keywords
    - target_keywords: list of keywords to match (will select checkboxes containing these)
    - exclude_keywords: list of keywords to exclude (won't select checkboxes containing these)
    """
    if exclude_keywords is None:
        exclude_keywords = ["ไม่มี", "ไม่คิด", "__other"]
    
    try:
        checkboxes = question_container.find_elements(By.CSS_SELECTOR, CHECKBOX_SELECTOR)
        if not checkboxes:
            return False
        
        # Find matching checkboxes
        matching = []
        positive_only = []  # Checkboxes that are not excluded (even if not matching keywords)
        
        for cb in checkboxes:
            label = get_checkbox_label(cb)
            # Debug disabled for speed
            
            # Check if should be excluded
            should_exclude = False
            for exc in exclude_keywords:
                if exc in label:
                    should_exclude = True
                    break
            
            if should_exclude:
                pass  # Debug disabled
                continue
            
            positive_only.append(cb)
            
            # Check if matches any target keyword
            for kw in target_keywords:
                if kw in label:
                    matching.append(cb)
                    pass  # Debug disabled
                    break
        
        # Debug disabled for speed
        
        # Select from matching if available, otherwise from positive_only
        selection_pool = matching if matching else positive_only
        
        if selection_pool:
            num = min(random.randint(min_select, max_select), len(selection_pool))
            selected = random.sample(selection_pool, num)
            pass  # Debug disabled
            for cb in selected:
                human_like_click(driver, cb)
                human_delay(0.3, 0.6)
            return True
        else:
            pass  # Debug disabled
    except Exception as e:
        print(f"Multiple checkbox error: {e}")
    return False


def fill_text_field(question_container, text):
    """Fill a text input field with human-like typing"""
    try:
        text_input = question_container.find_element(By.CSS_SELECTOR, "textarea, input[type='text']")
        text_input.clear()
        
        # Type character by character for more human-like behavior
        for char in text:
            text_input.send_keys(char)
            time.sleep(random.uniform(0.02, 0.08))  # Typing speed variation
        
        return True
    except Exception:
        pass
    return False


# Pool of POSITIVE suggestions/comments
SUGGESTION_POOL = [
    "ดีครับ", "ดีค่ะ", "ดีมากครับ", "ดีมากค่ะ", "สนุกมาก", "เยี่ยมเลย",
    "จัดกิจกรรมดีมาก", "ชอบกิจกรรมมาก", "ประทับใจมาก", "สุดยอด",
    "อยากให้จัดอีก", "สนับสนุนไทยแลนด์", "สู้ๆ ทีมไทย", "สู้ๆ นักกีฬาไทย",
    "เชียร์ไทย", "ตื่นเต้นมาก", "รอชมการแข่งขัน", "ภูมิใจมาก",
    "หวังว่าจะสำเร็จ", "ขอบคุณที่จัดกิจกรรม", "นักกีฬาสู้ๆ", "ไทยแลนด์สู้ๆ",
    "ประชาสัมพันธ์ได้ดีมาก", "จัดได้ดีมาก", "ชอบมากๆ", "เจ๋งมาก",
    "อยากให้มีกิจกรรมแบบนี้อีก", "ส่งกำลังใจให้นักกีฬา", "ยอดเยี่ยม",
    "กิจกรรมน่าสนใจมาก", "ได้ความรู้ดี", "สนุกสนานมาก",
    "ภูมิใจที่ไทยเป็นเจ้าภาพ", "ดีใจที่ได้ร่วมกิจกรรม",
]


def generate_form_data():
    """Generate random POSITIVE form data"""
    data = {}
    
    # 1.1 เพศ - ชาย/หญิง/อื่นๆ
    data['gender'] = random.choices(
        ['ชาย', 'หญิง', 'อื่นๆ'],
        weights=[48, 50, 2]
    )[0]
    
    # 1.2 อายุ
    data['age'] = random.choices(
        ['ต่ำกว่า 18', '18 - 25', '26 - 35', '36 - 45', '46 - 60', 'มากกว่า 60'],
        weights=[10, 25, 25, 20, 15, 5]
    )[0]
    
    # 1.3 อาชีพ
    data['occupation'] = random.choices(
        ['นักเรียน', 'พนักงานบริษัท', 'ข้าราชการ', 'อาชีพอิสระ', 'ค้าขาย', 'อื่นๆ'],
        weights=[20, 25, 15, 15, 15, 10]
    )[0]
    
    # 2.1 ทราบหรือไม่ - เกือบทุกคนรู้
    data['awareness'] = random.choices(
        ['ทราบ', 'ไม่ทราบ'],
        weights=[95, 5]
    )[0]
    
    # 2.3 ระดับความสนใจ - เลือกอันเดียว (VERY POSITIVE)
    data['interest_level'] = random.choices(
        ['สนใจมากที่สุด', 'สนใจมาก', 'สนใจปานกลาง'],
        weights=[60, 35, 5]
    )[0]
    
    # 2.6 ข้อเสนอแนะ
    data['suggestion'] = random.choice(SUGGESTION_POOL)
    
    return data


def submit_form_humanlike(driver):
    """Submit form with human-like timing"""
    try:
        driver.get(FORM_URL)
        
        # Wait for page load - more human-like
        human_delay(2.0, 3.5)
        
        # Wait for form to be ready
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='listitem']"))
            )
        except TimeoutException:
            print("Timeout waiting for form")
            return False, 0
        
        start_time = time.time()
        
        # Get all questions
        questions = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")
        
        if not questions:
            print("No questions found")
            return False, 0
        
        form_data = generate_form_data()
        
        for question in questions:
            try:
                question_text = question.text.lower() if question.text else ""
                original_text = question.text or ""
                
                # Read question - minimal pause
                human_delay(0.05, 0.1)
                
                # Debug disabled for speed
                # short_text = original_text[:60].replace('\n', ' ')
                # print(f"\n[Q] {short_text}...")
                
                # 1.1 เพศ
                if "เพศ" in question_text and ("1.1" in original_text or "เพศ" in original_text):
                    if not select_radio_by_keyword(driver, question, form_data['gender']):
                        select_single_checkbox_by_keyword(driver, question, form_data['gender'])
                
                # 1.2 อายุ
                elif "อายุ" in question_text and ("1.2" in original_text or "อายุ" in original_text):
                    if not select_radio_by_keyword(driver, question, form_data['age']):
                        select_single_checkbox_by_keyword(driver, question, form_data['age'])
                
                # 1.3 อาชีพ
                elif "อาชีพ" in question_text and ("1.3" in original_text or "อาชีพ" in original_text):
                    if not select_radio_by_keyword(driver, question, form_data['occupation']):
                        select_single_checkbox_by_keyword(driver, question, form_data['occupation'])
                
                # 2.1 ทราบหรือไม่
                elif "ทราบหรือไม่" in question_text or "ทราบ" in question_text and "เจ้าภาพ" in question_text or "2.1" in original_text:
                    if not select_radio_by_keyword(driver, question, form_data['awareness']):
                        select_single_checkbox_by_keyword(driver, question, form_data['awareness'])
                
                # 2.2 ช่องทางรับรู้ข่าวสาร (checkboxes) - เลือก 1-2 ช่องทาง
                elif "ช่องทาง" in question_text or "รับรู้ข่าวสาร" in question_text or "2.2" in original_text:
                    channels = ["สื่อสังคมออนไลน์", "Facebook", "TikTok", "เว็บไซต์ข่าว", "ป้ายโฆษณา"]
                    select_multiple_checkboxes(driver, question, channels, min_select=1, max_select=2)
                
                # 2.3 ตัวเลือกระดับความสนใจ (แต่ละตัวเป็น listitem แยก) - เลือกตามที่ generate
                elif question_text.strip() == form_data['interest_level'].lower():
                    # เจอตัวเลือกที่ตรงกับที่ต้องการ - คลิก checkbox ในนี้
                    checkboxes = question.find_elements(By.CSS_SELECTOR, CHECKBOX_SELECTOR)
                    radios = question.find_elements(By.CSS_SELECTOR, RADIO_SELECTOR)
                    if checkboxes:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkboxes[0])
                        time.sleep(0.1)
                        driver.execute_script("arguments[0].click();", checkboxes[0])
                        print(f"  -> Selected interest: {form_data['interest_level']}")
                    elif radios:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radios[0])
                        time.sleep(0.1)
                        driver.execute_script("arguments[0].click();", radios[0])
                        print(f"  -> Selected interest (radio): {form_data['interest_level']}")
                
                # 2.3 หัวข้อระดับความสนใจ (header) - ข้ามไป ไม่ต้องทำอะไร
                elif "ในระดับใด" in question_text or "ระดับใด" in question_text or ("ความสนใจ" in question_text and "ติดตาม" in question_text) or "2.3" in original_text:
                    print(f"  -> 2.3 header, waiting for options...")
                
                # 2.4 การมีส่วนร่วม (checkboxes) - เลือก 1-2 อย่าง
                elif "มีส่วนร่วม" in question_text or "ส่วนร่วม" in question_text or "2.4" in original_text:
                    participation = ["เข้าชม", "ถ่ายทอดสด", "กิจกรรมประชาสัมพันธ์", "ซื้อสินค้า", "ของที่ระลึก"]
                    select_multiple_checkboxes(driver, question, participation, min_select=1, max_select=2)
                
                # 2.4 ตัวเลือกการมีส่วนร่วมแยก (individual options) - บางตัวสุ่มเลือก
                elif "เข้าชมการแข่งขัน" in question_text or "ถ่ายทอดสด" in question_text or "กิจกรรมประชาสัมพันธ์" in question_text or "ซื้อสินค้า" in question_text or "ของที่ระลึก" in question_text:
                    # สุ่มว่าจะเลือกตัวนี้ไหม (70% chance)
                    if random.random() < 0.7:
                        checkboxes = question.find_elements(By.CSS_SELECTOR, CHECKBOX_SELECTOR)
                        if checkboxes:
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkboxes[0])
                            time.sleep(0.1)
                            driver.execute_script("arguments[0].click();", checkboxes[0])
                            print(f"  -> Selected participation option")
                
                # 2.5 ผลดีต่อประเทศ (checkboxes) - เลือก 1-3 ด้าน
                elif "ส่งผลดี" in question_text or "ผลดีต่อประเทศ" in question_text or "2.5" in original_text:
                    benefits = ["เศรษฐกิจ", "ภาพลักษณ์", "สังคม", "ท่องเที่ยว"]
                    select_multiple_checkboxes(driver, question, benefits, min_select=1, max_select=3)
                
                # 2.5 ตัวเลือกผลดีแยก (individual options) - บางตัวสุ่มเลือก
                elif "ด้านเศรษฐกิจ" in question_text or "ด้านภาพลักษณ์" in question_text or "ด้านสังคม" in question_text or "ด้านการท่องเที่ยว" in question_text:
                    # สุ่มว่าจะเลือกตัวนี้ไหม (70% chance)
                    if random.random() < 0.7:
                        checkboxes = question.find_elements(By.CSS_SELECTOR, CHECKBOX_SELECTOR)
                        if checkboxes:
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkboxes[0])
                            time.sleep(0.1)
                            driver.execute_script("arguments[0].click();", checkboxes[0])
                            print(f"  -> Selected benefit option")
                
                # 2.6 ข้อเสนอแนะ (text)
                elif "ข้อเสนอแนะ" in question_text or "เสนอแนะ" in question_text or "2.6" in original_text:
                    fill_text_field(question, form_data['suggestion'])
                
                # Skip negative options
                elif "ไม่มีส่วนร่วม" in question_text or "ไม่คิดว่า" in question_text or "ไม่สนใจ" in question_text:
                    print(f"  -> Skipping negative option")
                
                # Pause between questions - more human-like
                human_delay(0.05, 0.1)
                
            except Exception as e:
                print(f"Question error: {e}")
                continue
        
        # Scroll to bottom before submit
        driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        human_delay(0.3, 0.5)
        
        # Find and click submit button
        submit_selectors = [
            "//span[contains(text(), 'ส่ง')]/ancestor::div[@role='button']",
            "//div[@role='button' and contains(., 'ส่ง')]",
        ]
        
        submitted = False
        for selector in submit_selectors:
            try:
                button = driver.find_element(By.XPATH, selector)
                human_like_click(driver, button)
                submitted = True
                break
            except NoSuchElementException:
                continue
        
        if not submitted:
            print("Submit button not found")
            return False, 0
        
        # Wait for submission
        human_delay(1.5, 2.5)
        
        # Check success
        elapsed = time.time() - start_time
        if "formResponse" in driver.current_url or "closedform" in driver.current_url:
            return True, elapsed
        
        try:
            success_xpath = "//div[contains(text(), 'บันทึกคำตอบแล้ว') or contains(text(), 'ส่งคำตอบแล้ว')]"
            driver.find_element(By.XPATH, success_xpath)
            return True, elapsed
        except NoSuchElementException:
            return True, elapsed  # Assume success
        
    except Exception as e:
        print(f"Form error: {e}")
        return False, 0


def print_header():
    """Print beautiful header"""
    print("\n" + "="*80)
    print("🏅 AUTO-FILL GOOGLE FORM - แบบประเมินซีเกมส์ 33".center(80))
    print("="*80)
    print(f"📊 Target      : {NUM_RESPONSES} responses")
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
        print(f"    ⏳ Waiting {wait_time}s...")


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
    """Main execution"""
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
            success, elapsed = submit_form_humanlike(driver)
            
            if success:
                success_count += 1
            else:
                failed_count += 1
            
            results.append({
                "num": i,
                "status": "Success" if success else "Failed",
                "time": f"{elapsed:.2f}s",
                "timestamp": datetime.now().strftime('%H:%M:%S')
            })
            
            # Delay between submissions - more human-like variation
            if i < NUM_RESPONSES:
                wait = random.randint(1, 3)  # Maximum speed
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
    csv_file = f"seagames_survey_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=["num", "status", "time", "timestamp"])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"💾 Results saved: {csv_file}\n")


if __name__ == "__main__":
    main()
