# -*- coding: utf-8 -*-
"""
Auto-fill Google Form - แบบสอบถาม FDA EXPO 2026 (FINAL DEBUG VERSION)
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# ============================================================================
# CONFIGURATION
# ============================================================================
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfSYFcbxBYREO297MkI_tS_NabQtPIlZcOIrqjMWMWBSakIQQ/viewform"
NUM_RESPONSES = 67
HEADLESS = True  
DEBUG = False  # ปิดเพื่อให้เร็วขึ้น

# ============================================================================
# DATA POOLS
# ============================================================================
GENDERS = ["ชาย", "หญิง", "ไม่ระบุ"]
GENDER_WEIGHTS = [40, 50, 10]
AGES = ["น้อยกว่า 21 ปี", "21-30 ปี", "31-40 ปี", "41-50 ปี", "51-60 ปี", "61 ปีขึ้นไป"]
AGE_WEIGHTS = [5, 25, 30, 25, 10, 5]
OCCUPATIONS = ["ข้าราชการ/พนักงานของรัฐ", "พนักงานรัฐวิสาหกิจ/บริษัท", "นักเรียน/นักศึกษา", "เจ้าของกิจการ"]
OCCUPATION_WEIGHTS = [25, 35, 15, 25]
NEWS_CHANNELS = ["โทรทัศน์", "วิทยุ", "หนังสือพิมพ์", "ป้ายโฆษณา", "การชักชวน/คำบอกเล่า", "สื่อออนไลน์"]
PRODUCT_TYPES = ["ผลิตภัณฑ์ที่ใช้ในชีวิตประจำวัน", "ผลิตภัณฑ์ภูมิปัญญาท้องถิ่น", "นวัตกรรมสุขภาพที่ได้มาตรฐานและมีความปลอดภัย"]
BUDGETS = ["ไม่เกิน 1,000 บาท", "1,001-3,000 บาท", "3,001-5,000 บาท", "5,001-10,000 บาท", "มากกว่า 10,000 บาท"]
BUDGET_WEIGHTS = [25, 35, 20, 12, 8]
VISIT_REASONS = ["ได้เลือกซื้อผลิตภัณฑ์สุขภาพไทยที่ตรงกับความต้องการ", "ผลิตภัณฑ์ที่จำหน่ายมีความหลากหลายและน่าสนใจ", "ผลิตภัณฑ์สุขภาพไทยมีคุณภาพและได้รับมาตราฐาน", "ภายในงานมีกิจกรรมที่น่าสนใจ", "เพื่อสนับสนุนสินค้าจาก อย."]
BENEFITS = ["ได้รับผลิตภัณฑ์ตรงกับความต้องการ", "ได้รับความรู้และประสบการณ์", "ได้รับผลิตภัณฑ์ที่มีคุณภาพและมาตราฐานเหมาะสมกับราคา", "ได้รับประโยชน์ทางการค้า/ธุรกิจ"]
COMMENTS = ["งานจัดได้ดีมากครับ", "สินค้าหลากหลายดี", "อยากให้มีงานแบบนี้อีก", "สถานที่เดินทางสะดวก", "ได้ความรู้เยอะมาก", "-", "ดีเยี่ยม", "ประทับใจครับ", "อยากให้เพิ่มร้านค้าอีก", "ขอบคุณครับ"]

def create_driver():
    options = Options()
    if HEADLESS: options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=th-TH") 
    return webdriver.Chrome(options=options)

def safe_delay(min_sec=0.2, max_sec=0.4):
    time.sleep(random.uniform(min_sec, max_sec))

def generate_form_data():
    return {
        'gender': random.choices(GENDERS, weights=GENDER_WEIGHTS)[0],
        'age': random.choices(AGES, weights=AGE_WEIGHTS)[0],
        'occupation': random.choices(OCCUPATIONS, weights=OCCUPATION_WEIGHTS)[0],
        'news_channels': random.sample(NEWS_CHANNELS, k=random.randint(1, 3)),
        'product_types': random.sample(PRODUCT_TYPES, k=random.randint(1, 2)),
        'budget': random.choices(BUDGETS, weights=BUDGET_WEIGHTS)[0],
        'visit_reasons': random.sample(VISIT_REASONS, k=random.randint(2, 3)),
        'benefits': random.sample(BENEFITS, k=random.randint(1, 3))
    }

def scroll_to_element(driver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
        time.sleep(0.15)
    except:
        pass

def select_option_by_keyword(driver, container, keyword, mode="radio"):
    try:
        scroll_to_element(driver, container)
        selector = "div[role='radio']" if mode == "radio" else "div[role='checkbox']"
        options = container.find_elements(By.CSS_SELECTOR, selector)
        for opt in options:
            data = (opt.get_attribute("data-value") or opt.get_attribute("aria-label") or opt.text or "")
            if keyword in data:
                is_checked = opt.get_attribute("aria-checked") == "true"
                if not is_checked:
                    driver.execute_script("arguments[0].click();", opt)
                    safe_delay(0.2, 0.4)
                return True
        return False
    except:
        return False

def fill_text_field(driver, container, text):
    try:
        inputs = container.find_elements(By.CSS_SELECTOR, "input[type='text'], textarea")
        if inputs:
            inputs[0].clear()
            inputs[0].send_keys(text)
            return True
    except:
        pass
    return False

def click_next_button(driver):
    """คลิกปุ่มถัดไป (Next)"""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.3)
    
    # พยายามหาปุ่มที่มีคำว่า "ถัดไป" หรือ "Next"
    keywords = ["ถัดไป", "Next"]
    
    # 1. ลองหาจาก Text โดยตรง
    for kw in keywords:
        try:
            xpath = f"//span[contains(text(), '{kw}')]/ancestor::div[@role='button']"
            btns = driver.find_elements(By.XPATH, xpath)
            for btn in btns:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].click();", btn)
                    return True
        except:
            continue
            
    return False

def debug_and_click_submit(driver):
    """
    ฟังก์ชันไม้ตาย: หาปุ่ม Submit โดยการกวาดทุกปุ่มบนหน้ามาเช็ค
    """
    print("  🔎 Debugging Submit Button...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.3)

    # หาปุ่มทั้งหมดบนหน้าที่มี role='button'
    buttons = driver.find_elements(By.CSS_SELECTOR, "div[role='button']")
    print(f"  🔘 Found {len(buttons)} buttons on page.")

    target_button = None

    for i, btn in enumerate(buttons):
        txt = btn.text.strip()
        print(f"     [{i}] Text: '{txt}'") # ปริ้นท์ข้อความบนปุ่มออกมาดู
        
        # เงื่อนไขการเลือกปุ่ม: ต้องมีคำว่า "ส่ง" หรือ "Submit"
        if "ส่ง" in txt or "Submit" in txt:
            target_button = btn
            print(f"     ✅ Match found at index {i}!")
            break
            
    # ถ้าหาตามข้อความไม่เจอ ให้ลองกดปุ่มตัวสุดท้าย (ปกติปุ่มส่งจะอยู่ขวาสุด/ล่างสุด)
    if not target_button and len(buttons) > 0:
        print("  ⚠️ No text match. Trying the LAST button (Risk method)...")
        target_button = buttons[-1]

    if target_button:
        try:
            # เน้นสีปุ่มที่จะกด (สีเขียว)
            driver.execute_script("arguments[0].style.border='5px solid green';", target_button)
            time.sleep(0.5)
            # สั่งคลิกด้วย JavaScript
            driver.execute_script("arguments[0].click();", target_button)
            return True
        except Exception as e:
            print(f"  ❌ Click failed: {e}")
            return False
    else:
        print("  ❌ No valid button found to click.")
        return False

def submit_form(driver):
    start_time = time.time()
    driver.get(FORM_URL)
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='listitem']")))
    except:
        print("  ❌ Time out loading form")
        return False, 0

    safe_delay(1, 2)
    data = generate_form_data()
    
    # --- PAGE 1 ---
    print("  📄 Page 1 processing...")
    questions = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")
    for q in questions:
        text = q.text.lower()
        if "เพศ" in text and "อายุ" not in text: select_option_by_keyword(driver, q, data['gender'])
        elif "อายุ" in text and "ปี" in text: select_option_by_keyword(driver, q, data['age'])
        elif "อาชีพ" in text: select_option_by_keyword(driver, q, data['occupation'])
        elif "ทราบข่าว" in text: 
            for item in data['news_channels']: select_option_by_keyword(driver, q, item, "checkbox")
        elif "ประเภท" in text: 
            for item in data['product_types']: select_option_by_keyword(driver, q, item, "checkbox")
        elif "วงเงิน" in text: select_option_by_keyword(driver, q, data['budget'])
        elif "เหตุผล" in text: 
            for item in data['visit_reasons']: select_option_by_keyword(driver, q, item, "checkbox")
        elif "ประโยชน์" in text: 
            for item in data['benefits']: select_option_by_keyword(driver, q, item, "checkbox")
            
    if not click_next_button(driver):
        print("  ❌ Failed to click Next")
        return False, time.time() - start_time
    
    safe_delay(0.5, 0.8)

    # --- PAGE 2 ---
    print("  📄 Page 2 Ratings...")
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='radio']")))
        questions = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")
        for q in questions:
            if "ส่วนที่" in q.text or len(q.text) < 5: continue
            rating = str(random.choice([4, 5]))
            select_option_by_keyword(driver, q, rating)
            
        if not click_next_button(driver):
            print("  ❌ Failed to click Next (Page 2)")
            return False, time.time() - start_time
    except:
        pass 

    safe_delay(0.5, 0.8)

    # --- PAGE 3 ---
    print("  📄 Page 3 Comments...")
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
        questions = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")
        for q in questions:
            if "ข้อคิดเห็น" in q.text or "เสนอแนะ" in q.text:
                comment = random.choice(COMMENTS)
                fill_text_field(driver, q, comment)
        
        # ✅ เรียกใช้ฟังก์ชันใหม่ Debug & Click Submit
        if not debug_and_click_submit(driver):
            print("  ❌ Critical: Could not submit form.")
            return False, time.time() - start_time

    except Exception as e:
        print(f"  ⚠️ Error page 3: {e}")

    # --- VERIFY SUBMISSION ---
    try:
        WebDriverWait(driver, 10).until(EC.url_contains("formResponse"))
        print("  ✅ Form submitted successfully!")
        return True, time.time() - start_time
    except:
        if "บันทึกคำตอบ" in driver.page_source or "recorded" in driver.page_source:
             print("  ✅ Form submitted (Text verified)!")
             return True, time.time() - start_time
        
    print("  ❌ Submission verification failed")
    return False, time.time() - start_time

def main():
    print("🚀 Starting Auto-fill...")
    driver = create_driver()
    success_count = 0
    try:
        for i in range(NUM_RESPONSES):
            print(f"\n--- Form {i+1}/{NUM_RESPONSES} ---")
            driver.delete_all_cookies()
            success, _ = submit_form(driver)
            if success: success_count += 1
            time.sleep(random.uniform(1, 2))  # ลดเวลาระหว่างฟอร์ม
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    finally:
        driver.quit()
        print(f"\n📊 Summary: Success {success_count}/{NUM_RESPONSES}")

if __name__ == "__main__":
    main()