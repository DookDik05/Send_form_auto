#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-fill Google Form - แบบลงทะเบียน INSPIRE THE GAME คลินิกกีฬา ปลุกพลังฝัน
Uses Selenium with realistic human timing
Form URL: https://docs.google.com/forms/d/e/1FAIpQLSdhA8GSrZL5-4a0Q_rWnmfkW6KFphzxLDgzcqbwaH3AATwzmQ/viewform
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
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScsICkaaxZv0_LUytICMhVsFrHtx1F0aCQRcFdTx0jrKJcQHQ/viewform"
NUM_RESPONSES = 239  # จำนวนฟอร์มที่ต้องการส่ง
HEADLESS = True     # ตั้งเป็น True เพื่อรันโดยไม่เปิดหน้าต่าง
# ============================================================================

# CSS Selectors
RADIO_SELECTOR = "div[role='radio']"
TEXT_INPUT_SELECTOR = "input.whsOnd.zHQkBf, textarea"

# Thai first names pool - Extended for 300 unique names
FIRST_NAMES_MALE = [
    "สมชาย", "สมศักดิ์", "สุรชัย", "วีระ", "ประสิทธิ์", "สมบัติ", "วิชัย", "สมหมาย",
    "ชัยวัฒน์", "ธนกฤต", "พีรพัฒน์", "นันทวัฒน์", "ภูมิพัฒน์", "กิตติพงศ์", "พงศกร",
    "ณัฐพล", "ณัฐวุฒิ", "ธนภัทร", "พชร", "ภัทรพล", "อธิป", "อนุชา", "เอกชัย",
    "กฤษณะ", "กฤษฎา", "กันต์", "เกียรติศักดิ์", "ขจรเกียรติ", "คมสัน", "จักรพงศ์",
    "จิรวัฒน์", "เจษฎา", "ชนาธิป", "ชยพล", "ชาญชัย", "ณรงค์ศักดิ์", "ณัฐกิตติ์",
    "ดนุพล", "ทวีศักดิ์", "ทศพร", "ธนวัฒน์", "ธนาธิป", "ธีรพงศ์", "นพดล", "นฤเบศร์",
    "บุญเลิศ", "ปริญญา", "ปัญญา", "พิชญ์", "พิทักษ์", "ภคพงศ์", "ภาคิน", "ภานุวัฒน์",
    "มงคล", "ยศพล", "รณชัย", "วรเมธ", "วรวิทย์", "วัชรพล", "วันชัย", "วิรัตน์",
    "ศรัณย์", "ศักดา", "ศิวกร", "สถาพร", "สมพงษ์", "สมยศ", "สราวุธ", "สหรัฐ",
    "สันติ", "สิทธิชัย", "สิทธิพร", "สุทธิพงษ์", "สุรเชษฐ์", "สุริยา", "อดิศร", "อนันต์",
    "อภิชาติ", "อภิสิทธิ์", "อรรถพล", "อัครพล", "อานนท์", "อิทธิพล", "อุดม", "เอกพล",
    "กมล", "กรวิชญ์", "กฤตภาส", "กฤตเมธ", "กฤติน", "กวิน", "กิตติ", "กิตติธัช",
    "เกรียงไกร", "เกรียงศักดิ์", "คณิศร", "จตุพล", "จักรกฤษณ์", "จิณณวัตร", "จิรพัฒน์", "จิรศักดิ์",
]

FIRST_NAMES_FEMALE = [
    "สมหญิง", "สุภา", "สุดา", "วันเพ็ญ", "สุวรรณา", "พรรณี", "สมจิตร", "มาลี",
    "นิตยา", "วิไล", "รัชนี", "อรุณี", "ศิริ", "สุนีย์", "สายฝน", "พัชรี",
    "ธิดารัตน์", "วรรณา", "อารีย์", "นภา", "ปราณี", "พิมพ์", "มณี", "ราตรี",
    "ลัดดา", "วาสนา", "ศรีสุดา", "สุชาดา", "อรพรรณ", "อุไร", "กัญญา", "กาญจนา",
    "ชนิดา", "ชมพูนุช", "ดวงใจ", "ตรีรัตน์", "ทิพย์", "ธนิดา", "นันทิกา", "นิษา",
    "บุษบา", "ปภาวี", "ปิยะฉัตร", "ปิยะดา", "พรทิพย์", "พรนภา", "พัชราภรณ์", "ภัทรา",
    "มนัสนันท์", "รวิวรรณ", "รุ่งนภา", "วริศรา", "ศิริพร", "สิริมา", "อภิญญา", "อมรรัตน์",
    "กนกวรรณ", "กมลชนก", "กมลพร", "กรรณิการ์", "กัญญาณัฐ", "กัญญารัตน์", "กานต์ธิดา", "กุลธิดา",
    "ขวัญใจ", "จันจิรา", "จารุวรรณ", "จิดาภา", "จิราพร", "จิราภรณ์", "จุฬาลักษณ์", "ชญานิศ",
    "ชนากานต์", "ชลธิชา", "ชลิตา", "ชวัลลักษณ์", "ชัญญา", "ณัฏฐณิชา", "ณัฐกานต์", "ณัฐชา",
    "ณัฐธิดา", "ณัฐนันท์", "ณัฐริกา", "ณิชา", "ณิชาภัทร", "ดลยา", "ดารารัตน์", "ทิพวรรณ",
    "ธนพร", "ธนัชชา", "ธนัญญา", "ธัญจิรา", "ธัญชนก", "ธัญญลักษณ์", "ธัญพิชชา", "ธิดาพร",
    "นริศรา", "นลินี", "นันท์นภัส", "นันทิชา", "นิภาพร", "เนตรนภา", "บุญญิสา", "บุณยานุช",
]

# Thai last names pool - Extended
LAST_NAMES = [
    "ใจดี", "มีสุข", "รักดี", "ทองดี", "สุขสวัสดิ์", "เจริญสุข", "ประเสริฐ", "บุญมา",
    "พงษ์พานิช", "วงศ์สกุล", "แซ่ลิ้ม", "แซ่ตัน", "แซ่โง้ว", "จันทร์เพ็ญ", "พิทักษ์ธรรม",
    "สมบูรณ์", "มหาศาล", "ศรีสว่าง", "วิชัยดิษฐ", "เพชรรัตน์", "ทองคำ", "เงินยวง",
    "อุดมทรัพย์", "สิริโชติ", "พรหมมา", "เทพสุวรรณ", "แก้วมณี", "เกษมสุข", "ศิริวรรณ",
    "พิมพ์ทอง", "ศักดิ์สิทธิ์", "อมรเทพ", "จิตรกุล", "สุขเกษม", "วิไลลักษณ์", "บุญรอด",
    "พลอยแก้ว", "เพ็ชรดี", "รุ่งโรจน์", "สายทอง", "หงษ์ทอง", "อินทร์เรือง", "โชติกุล",
    "ชัยรัตน์", "นาคสุข", "บุญส่ง", "ภักดี", "วรวุฒิ", "สุวรรณภูมิ", "อนุรักษ์",
    "กล้าหาญ", "ขวัญชัย", "จันทร์แก้ว", "จิตรปราณี", "ชาญวิทย์", "ดวงจันทร์", "ทองสุข",
    "ธรรมรักษ์", "นพรัตน์", "นิรันดร์", "บัวทอง", "ประสาทพร", "พงษ์ทอง", "มีชัย",
    "ยิ้มแย้ม", "รัตนกุล", "ลิ้มประเสริฐ", "วงศ์ประเสริฐ", "ศรีประเสริฐ", "สกุลดี", "สมใจ",
    "สุขสมบูรณ์", "หิรัญรัตน์", "อารีรัตน์", "เจียมเจริญ", "แจ่มใส", "โตสกุล", "ไพศาล",
    "กาญจนวัฒน์", "เขมกุล", "จรูญศรี", "ชนะพันธ์", "ดีประเสริฐ", "ต่อสกุล", "ธนะสาร",
]

# Sports pool
SPORTS = [
    "ฟุตบอล", "วอลเลย์บอล", "บาสเกตบอล", "แบดมินตัน", "เทนนิส", "ว่ายน้ำ", 
    "วิ่ง", "มวยไทย", "เทควันโด", "ยิมนาสติก", "กอล์ฟ", "ยกน้ำหนัก",
    "ปิงปอง", "ตะกร้อ", "ยูโด", "คาราเต้", "มวยสากล", "จักรยาน",
    "เปตอง", "กรีฑา", "กระโดดร่ม", "ยิงปืน", "ยิงธนู", "เรือพาย",
    "สเก็ตบอร์ด", "ฟันดาบ", "โปโลน้ำ", "ซอฟท์บอล", "รักบี้", "ฮอกกี้",
    "เอ็กซ์ตรีม", "ปีนเขา", "โยคะ", "พิลาทิส", "ฟิตเนส", "เต้น",
]

# Pre-generated unique registrations list
UNIQUE_REGISTRATIONS = []

def generate_unique_registrations(count):
    """Pre-generate unique (first_name, last_name) combinations"""
    global UNIQUE_REGISTRATIONS
    
    used_names = set()
    registrations = []
    
    # Create all possible combinations
    all_male_combos = [(fn, ln, 'ชาย') for fn in FIRST_NAMES_MALE for ln in LAST_NAMES]
    all_female_combos = [(fn, ln, 'หญิง') for fn in FIRST_NAMES_FEMALE for ln in LAST_NAMES]
    
    # Shuffle and combine
    random.shuffle(all_male_combos)
    random.shuffle(all_female_combos)
    
    # Take alternating from male and female to balance
    male_index = 0
    female_index = 0
    
    while len(registrations) < count:
        # Randomly pick male or female (balanced)
        if random.random() < 0.48 and male_index < len(all_male_combos):
            fn, ln, gender = all_male_combos[male_index]
            male_index += 1
        elif female_index < len(all_female_combos):
            fn, ln, gender = all_female_combos[female_index]
            female_index += 1
        elif male_index < len(all_male_combos):
            fn, ln, gender = all_male_combos[male_index]
            male_index += 1
        else:
            break
        
        name_key = f"{fn} {ln}"
        if name_key not in used_names:
            used_names.add(name_key)
            
            # Generate age and sport
            age = random.choices(
                ['ต่ำกว่า 18', '18 - 25', '26 - 35', '36 - 45', '46 - 60', 'มากกว่า 60'],
                weights=[10, 30, 25, 20, 10, 5]
            )[0]
            sport = random.choice(SPORTS)
            
            registrations.append({
                'first_name': fn,
                'last_name': ln,
                'gender': gender,
                'age': age,
                'sport': sport
            })
    
    UNIQUE_REGISTRATIONS = registrations
    print(f"✅ Generated {len(registrations)} unique registrations")
    return registrations


def get_registration_data(index):
    """Get registration data by index (0-based)"""
    if index < len(UNIQUE_REGISTRATIONS):
        return UNIQUE_REGISTRATIONS[index]
    else:
        # Fallback: generate new random data
        gender = random.choices(['ชาย', 'หญิง'], weights=[48, 52])[0]
        if gender == 'ชาย':
            first_name = random.choice(FIRST_NAMES_MALE)
        else:
            first_name = random.choice(FIRST_NAMES_FEMALE)
        
        return {
            'first_name': first_name,
            'last_name': random.choice(LAST_NAMES),
            'gender': gender,
            'age': random.choice(['18 - 25', '26 - 35', '36 - 45']),
            'sport': random.choice(SPORTS)
        }


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
    """Click element with human-like behavior"""
    try:
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        human_delay(0.2, 0.4)
        
        actions = ActionChains(driver)
        actions.move_to_element(element)
        actions.pause(random.uniform(0.1, 0.3))
        actions.click()
        actions.perform()
        
        human_delay(0.1, 0.3)
    except Exception:
        driver.execute_script("arguments[0].click();", element)
        human_delay(0.1, 0.2)


def human_like_type(element, text):
    element.clear()
    element.send_keys(text)  # พิมพ์ทีเดียว


def select_radio_by_keyword(driver, question_container, keyword):
    """Select a radio option that contains the keyword"""
    try:
        radios = question_container.find_elements(By.CSS_SELECTOR, RADIO_SELECTOR)
        for radio in radios:
            val = radio.get_attribute("data-value") or radio.get_attribute("aria-label") or ""
            if keyword in val:
                human_like_click(driver, radio)
                return True
        for radio in radios:
            if keyword in radio.text:
                human_like_click(driver, radio)
                return True
    except Exception as e:
        print(f"Radio error: {e}")
    return False


def fill_text_input(question_container, text):
    """Fill a text input field"""
    try:
        text_input = question_container.find_element(By.CSS_SELECTOR, TEXT_INPUT_SELECTOR)
        human_like_type(text_input, text)
        return True
    except Exception as e:
        print(f"Text input error: {e}")
    return False


def submit_form(driver, index):
    """Submit form with human-like timing"""
    try:
        driver.get(FORM_URL)
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
        
        # Get unique registration data by index
        data = get_registration_data(index)
        print(f"  Registering: {data['first_name']} {data['last_name']} ({data['gender']}, {data['age']})")
        
        for question in questions:
            try:
                question_text = question.text.lower() if question.text else ""
                human_delay(0.3, 0.6)
                
                # ชื่อจริง
                if "ชื่อจริง" in question_text or "ชื่อ" in question_text and "นามสกุล" not in question_text:
                    fill_text_input(question, data['first_name'])
                
                # นามสกุล
                elif "นามสกุล" in question_text:
                    fill_text_input(question, data['last_name'])
                
                # เพศ
                elif "เพศ" in question_text:
                    select_radio_by_keyword(driver, question, data['gender'])
                
                # อายุ
                elif "อายุ" in question_text:
                    select_radio_by_keyword(driver, question, data['age'])
                
                # กีฬาที่สนใจ
                elif "กีฬา" in question_text or "สนใจ" in question_text:
                    fill_text_input(question, data['sport'])
                
                human_delay(0.2, 0.5)
                
            except Exception as e:
                print(f"Question error: {e}")
                continue
        
        # Scroll to bottom and submit
        driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        human_delay(0.8, 1.5)
        
        # Find and click submit button
        submit_selectors = [
            "//span[contains(text(), 'ส่ง')]/ancestor::div[@role='button']",
            "//div[@role='button' and contains(., 'ส่ง')]",
        ]
        
        for selector in submit_selectors:
            try:
                button = driver.find_element(By.XPATH, selector)
                human_like_click(driver, button)
                break
            except NoSuchElementException:
                continue
        
        human_delay(1.5, 2.5)
        
        elapsed = time.time() - start_time
        if "formResponse" in driver.current_url or "closedform" in driver.current_url:
            return True, elapsed
        
        return True, elapsed
        
    except Exception as e:
        print(f"Form error: {e}")
        return False, 0


def print_header():
    """Print beautiful header"""
    print("\n" + "="*80)
    print("🏆 AUTO-FILL REGISTRATION - INSPIRE THE GAME".center(80))
    print("="*80)
    print(f"📊 Target      : {NUM_RESPONSES} registrations")
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
    
    print(f"{status} [{current:3d}/{total}] |{bar}| {percent:5.1f}% | ⏱️  {time_str}")
    
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
    
    # Pre-generate all unique registrations
    generate_unique_registrations(NUM_RESPONSES)
    print()
    
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
            success, elapsed = submit_form(driver, i - 1)  # 0-based index
            
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
            
            # Delay between submissions
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
    csv_file = f"registration_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=["num", "status", "time", "timestamp"])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"💾 Results saved: {csv_file}\n")


if __name__ == "__main__":
    main()
