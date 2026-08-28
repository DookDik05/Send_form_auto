#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-fill Satisfaction Survey Form - Configurable
Easily change the number of responses and delay time
Form: แบบประเมินความพึงพอใจ กิจกรรมสร้างกระแสการรับรู้การเป็นเจ้าภาพจัดการแข่งขันกีฬาชีเกมส์ 33
URL: https://docs.google.com/forms/d/e/1FAIpQLSeklchUtv4O-H1SpMgWkBm1RVVJWgqqNO4KZeBeqaEtQt_UAg/viewform
"""

import requests
import time
import csv
import re
import random
from datetime import datetime

# ============================================================================
# CONFIGURATION SECTION - Change these values as needed
# ============================================================================

# Number of responses to submit
NUM_RESPONSES = 700

# Delay between submissions in seconds (e.g., 15 = 4 responses/minute)
DELAY_SECONDS = 1

# ============================================================================
# END OF CONFIGURATION SECTION
# ============================================================================

# Form configuration
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeklchUtv4O-H1SpMgWkBm1RVVJWgqqNO4KZeBeqaEtQt_UAg/viewform"
FORM_ACTION = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSeklchUtv4O-H1SpMgWkBm1RVVJWgqqNO4KZeBeqaEtQt_UAg/formResponse"

# Form entry IDs from analysis
ENTRY_FIELDS = {
    "gender": "entry.1872413877",
    "age": "entry.1398273699",
    "occupation": "entry.1830449883",
    "know_host": "entry.1097410147",
    "media_channel": "entry.364052023",
    "interest_level": "entry.817785705",
    "participation": "entry.955737227",
    "benefits": "entry.216707116",
    "suggestions": "entry.629693393",
}

# Options
GENDERS = ["ชาย", "หญิง"]
AGES = ["18 - 25 ปี", "26 - 35 ปี", "36 - 45 ปี"]
OCCUPATIONS = ["นักเรียน/นักศึกษา", "พนักงานบริษัทเอกชน", "ข้าราชการ/พนักงานรัฐวิสาหกิจ", "ประกอบอาชีพอิสระ", "ค้าขาย/เจ้าของธุรกิจ"]
KNOW_HOSTS = ["ทราบ", "ไม่ทราบ"]
MEDIA_CHANNELS = ["สื่อสังคมออนไลน์ (เช่น Facebook, Twitter, Instagram, TikTok)", "เว็บไซต์ข่าว/แอปพลิเคชันข่าว", "ป้ายโฆษณา/สื่อประชาสัมพันธ์ภายนอก"]
INTEREST_LEVELS = ["สนใจมากที่สุด", "สนใจมาก", "สนใจปานกลาง", "สนใจน้อย", "ไม่สนใจเลย"]
PARTICIPATION_OPTIONS = ["เข้าชมการแข่งขันในสนาม", "ชมการถ่ายทอดสดผ่านโทรทัศน์หรือช่องทางออนไลน์", "เข้าร่วมกิจกรรมประชาสัมพันธ์หรือกิจกรรมเสริมต่างๆ", "ซื้อสินค้าหรือของที่ระลึกที่เกี่ยวข้อง"]
BENEFITS = ["ด้านเศรษฐกิจ: เพิ่มรายได้จากการท่องเที่ยวและการใช้จ่ายที่เกี่ยวข้อง", "ด้านภาพลักษณ์: สร้างชื่อเสียงและภาพลักษณ์ที่ดีของประเทศในระดับนานาชาติ", "ด้านสังคม: ส่งเสริมการกีฬาและสร้างแรงบันดาลใจให้กับคนในประเทศ", "ด้านการท่องเที่ยว: ดึงดูดนักท่องเที่ยวต่างชาติให้เดินทางมาไทยมากขึ้น"]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

# Results tracking
results = []


def get_fbzx(session):
    """Extract fbzx token from form page"""
    try:
        response = session.get(FORM_URL)
        match = re.search(r'name="fbzx"\s+value="([^"]+)"', response.text)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"Error getting fbzx: {e}")
    return None


def submit_form(session, idx, gender, age, occupation, know_host, media_channels, interest_level, participation, benefits, suggestions):
    """Submit a single form response"""
    try:
        fbzx = get_fbzx(session)
        if not fbzx:
            return False, "Failed to get fbzx token"
        
        payload = {
            ENTRY_FIELDS["gender"]: gender,
            ENTRY_FIELDS["age"]: age,
            ENTRY_FIELDS["occupation"]: occupation,
            ENTRY_FIELDS["know_host"]: know_host,
            ENTRY_FIELDS["media_channel"]: media_channels,
            ENTRY_FIELDS["interest_level"]: interest_level,
            ENTRY_FIELDS["participation"]: participation,
            ENTRY_FIELDS["benefits"]: benefits,
            ENTRY_FIELDS["suggestions"]: suggestions,
            "fbzx": fbzx,
        }
        
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": FORM_URL,
            "Content-Type": "application/x-www-form-urlencoded",
        }
        
        response = session.post(FORM_ACTION, data=payload, headers=headers, timeout=10)
        
        if response.status_code in [200, 301, 302]:
            return True, "OK"
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)


def main():
    """Main function to submit 96 responses - CONFIGURABLE"""
    print("=" * 90)
    print("Satisfaction Survey Auto-fill - Configurable")
    print("=" * 90)
    print(f"Form: แบบประเมินความพึงพอใจ")
    print(f"Target: {NUM_RESPONSES} responses")
    print(f"Delay: {DELAY_SECONDS} seconds per response ({60//DELAY_SECONDS} responses/minute)")
    print(f"Gender: 50% Male, 50% Female")
    print(f"Age: 18-45 years old only")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    session = requests.Session()
    success_count = 0
    failed_count = 0
    
    for idx in range(1, NUM_RESPONSES + 1):  # Configurable number of responses
        # Random data selection
        gender = random.choice(GENDERS)
        age = random.choice(AGES)
        occupation = random.choice(OCCUPATIONS)
        know_host = random.choice(KNOW_HOSTS)
        media_channels = random.choice(MEDIA_CHANNELS)
        interest_level = random.choice(INTEREST_LEVELS)
        participation = random.choice(PARTICIPATION_OPTIONS)
        benefits = random.choice(BENEFITS)
        suggestions = f"ข้อเสนอแนะที่ {idx}: กรุณาจัดการแข่งขันกีฬาให้ดีขึ้น"
        
        # Submit form
        success, message = submit_form(
            session, idx, gender, age, occupation, know_host,
            media_channels, interest_level, participation, benefits, suggestions
        )
        
        if success:
            success_count += 1
            status = "✓ OK"
        else:
            failed_count += 1
            status = f"✗ {message}"
        
        print(f"[{idx:2d}/{NUM_RESPONSES}] {gender:4s} | Age: {age:10s} | {status}")
        
        # Store result
        results.append({
            "response_num": idx,
            "gender": gender,
            "age": age,
            "occupation": occupation,
            "know_host": know_host,
            "media_channel": media_channels,
            "interest_level": interest_level,
            "participation": participation,
            "benefits": benefits,
            "status": "Success" if success else "Failed"
        })
        
        # Wait before next submission (except for the last one)
        if idx < NUM_RESPONSES:
            print(f"  Waiting {DELAY_SECONDS} seconds before next submission...")
            for remaining in range(DELAY_SECONDS, 0, -1):
                print(f"\r  {remaining:2d} seconds remaining...", end="", flush=True)
                time.sleep(1)
            print()  # New line
    
    # Print summary
    print("\n" + "=" * 90)
    print("SUMMARY")
    print("=" * 90)
    print(f"Total Submissions: {NUM_RESPONSES}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failed_count}")
    print(f"Success Rate: {(success_count/NUM_RESPONSES)*100:.1f}%")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Save to CSV
    csv_filename = f"satisfaction_survey_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ["response_num", "gender", "age", "occupation", "know_host", "media_channel", "interest_level", "participation", "benefits", "status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Results saved to: {csv_filename}")


if __name__ == "__main__":
    main()
