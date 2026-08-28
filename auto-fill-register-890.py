#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-fill Registration Form - 890 Registrants from JSON
Form: แบบลงทะเบียนกิจกรรมสร้างกระแสการรับรู้การเป็นเจ้าภาพจัดการแข่งขันกีฬาชีเกมส์ 33
URL: https://docs.google.com/forms/d/e/1FAIpQLScYXOItwUXkBmHpgQ-oZHozu2BqkfYK7WswvwkQRXANxru8PA/viewform
"""

import requests
import time
import csv
import re
import json
import random
from datetime import datetime

# ============================================================================
# CONFIGURATION SECTION - Change these values as needed
# ============================================================================

# JSON file containing registrant data
JSON_FILE = "mock_data_890.json"

# Number of responses to submit (set to None to use all from JSON)
NUM_RESPONSES = 890

# Delay between submissions in seconds (e.g., 15 = 4 responses/minute)
DELAY_SECONDS = 15

# ============================================================================
# END OF CONFIGURATION SECTION
# ============================================================================

# Form configuration
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScYXOItwUXkBmHpgQ-oZHozu2BqkfYK7WswvwkQRXANxru8PA/viewform"
FORM_ACTION = "https://docs.google.com/forms/u/0/d/e/1FAIpQLScYXOItwUXkBmHpgQ-oZHozu2BqkfYK7WswvwkQRXANxru8PA/formResponse"

# Entry IDs (from get_form_entry_ids.py)
ENTRY_IDS = {
    "firstname": "entry.117544671",      # ชื่อ
    "lastname": "entry.1852837798",      # นามสกุล
    "gender": "entry.1872413877",        # เพศ
    "age": "entry.1398273699",           # อายุ
    "sports": "entry.1830449883",        # กีฬาที่สนใจ
}

# Options for random fields
GENDERS = ["ชาย", "หญิง"]
AGES = ["18 - 25 ปี", "26 - 35 ปี", "36 - 45 ปี"]
SPORTS = ["ฟุตบอล", "แบดมินตัน", "วอลเลย์บอล", "ว่ายน้ำ", "เทนนิส", "ปิงปอง", "ยิงธนู", "กีฬาโต้สุ"]

# User agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edge/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
]


def load_registrants(json_file: str, limit: int = None):
    """Load registrant data from JSON file"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if limit and limit < len(data):
        return data[:limit]
    return data


def get_fbzx(session: requests.Session):
    """Fetch the form page and extract the fbzx token"""
    try:
        response = session.get(FORM_URL, timeout=10)
        match = re.search(r'name="fbzx"\s+value="([^"]+)"', response.text)
        if match:
            return match.group(1)
        match = re.search(r'"fbzx":"([^"]+)"', response.text)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"  Warning: Could not fetch fbzx: {e}")
    return None


def submit_form(session: requests.Session, firstname: str, lastname: str, 
                gender: str, age: str, sports: str):
    """Submit a single form response"""
    try:
        fbzx = get_fbzx(session)
        
        payload = {
            ENTRY_IDS["firstname"]: firstname,
            ENTRY_IDS["lastname"]: lastname,
            ENTRY_IDS["gender"]: gender,
            ENTRY_IDS["age"]: age,
            ENTRY_IDS["sports"]: sports,
            "fvv": "1",
            "partialResponse": "[]",
            "pageHistory": "0",
            "fbzx": fbzx if fbzx else "",
        }
        
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": FORM_URL,
            "Content-Type": "application/x-www-form-urlencoded",
        }
        
        response = session.post(FORM_ACTION, data=payload, headers=headers, timeout=10)
        
        if response.status_code in [200, 302, 303]:
            return True, "OK"
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)


def main():
    """Main function to submit registrations - CONFIGURABLE"""
    print("=" * 100)
    print("Auto-fill Registration Form - 890 Registrants from JSON")
    print("=" * 100)
    
    # Load registrants from JSON
    print(f"Loading registrants from: {JSON_FILE}")
    registrants = load_registrants(JSON_FILE, NUM_RESPONSES)
    total_registrants = len(registrants)
    
    print(f"Form: {FORM_URL[:80]}...")
    print(f"Target: {total_registrants} registrations")
    print(f"Delay: {DELAY_SECONDS} seconds ({60//DELAY_SECONDS} registrations/minute)")
    print(f"Estimated time: ~{(total_registrants * DELAY_SECONDS) // 60} minutes")
    print(f"Gender: Random (50% Male, 50% Female)")
    print(f"Age: Random (18-45 years)")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)
    print()
    
    session = requests.Session()
    results = []
    success_count = 0
    failed_count = 0
    
    for idx, person in enumerate(registrants, start=1):
        firstname = person.get("firstName", "")
        lastname = person.get("lastName", "")
        fullname = person.get("fullName", f"{firstname} {lastname}")
        
        # Random data selection
        gender = random.choice(GENDERS)
        age = random.choice(AGES)
        sports = random.choice(SPORTS)
        
        # Submit form
        success, message = submit_form(session, firstname, lastname, gender, age, sports)
        
        if success:
            success_count += 1
            status = "✓ OK"
        else:
            failed_count += 1
            status = f"✗ {message}"
        
        # Display progress
        print(f"[{idx:3d}/{total_registrants}] {fullname:25s} | {gender:4s} | {age:12s} | {sports:12s} | {status}")
        
        # Store result
        results.append({
            "response_num": idx,
            "firstname": firstname,
            "lastname": lastname,
            "fullname": fullname,
            "gender": gender,
            "age": age,
            "sports": sports,
            "status": "Success" if success else "Failed",
            "message": message
        })
        
        # Wait before next submission (except for the last one)
        if idx < total_registrants:
            for remaining in range(DELAY_SECONDS, 0, -1):
                print(f"\r  {remaining:2d} seconds remaining...", end="", flush=True)
                time.sleep(1)
            print("\r" + " " * 30 + "\r", end="")  # Clear countdown line
    
    # Print summary
    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print(f"Total Submissions: {total_registrants}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failed_count}")
    print(f"Success Rate: {(success_count/total_registrants)*100:.1f}%")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)
    
    # Save to CSV
    csv_filename = f"registration_results_{total_registrants}.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ["response_num", "firstname", "lastname", "fullname", "gender", "age", "sports", "status", "message"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\nResults saved to: {csv_filename}")


if __name__ == "__main__":
    main()
