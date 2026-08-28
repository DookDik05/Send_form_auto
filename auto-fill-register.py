import requests
import re
import time
import random
from bs4 import BeautifulSoup
import csv

# Form details from HTML
FORM_ID = "1FAIpQLSdhA8GSrZL5-4a0Q_rWnmfkW6KFphzxLDgzcqbwaH3AATwzmQ"
VIEW_URL = f"https://docs.google.com/forms/d/e/{FORM_ID}/viewform"
POST_URL = f"https://docs.google.com/forms/d/e/{FORM_ID}/formResponse"

# Entry field mappings from the HTML
ENTRY_FIELDS = {
    "firstname": "entry.117544671",      # ชื่อจริง (First Name)
    "lastname": "entry.1852837798",      # นามสกุล (Last Name)
    "gender": "entry.1872413877",        # เพศ (Gender)
    "age": "entry.1398273699",           # อายุ (Age)
    "sport": "entry.1830449883",         # กีฬาที่สนใจ (Interested Sports)
}

# User-Agent list for randomization
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
]

# Registration data
REGISTRANTS = [
    "พัทธมน ประเสริญวงศ์", "ทิญา เกษมทรัพย์", "ภูบดินทร์ ธนโชควาณิช",
    "ทีปกร ภูงาม", "บวรวิทย์ ชัยชนา", "ปีวรา ไกรรอด",
    "เมษา โอภาสเจริญ", "พิชัย นิมิตวานิชกร", "พงษ์นรินทร์ เลิศพานิชกุล",
    "จิโรจน์ ประเสริฐชัยวัฒน์", "เอกภาพ อุดมเดชรักษา", "ศุภาพิชญ์ ปิติโอภาสพงศ์",
    "ไตรทศ ปิ่นแก้ว", "ธญา แสงกระจ่าง", "กัญจนพร ภัชรปรีดา",
    "สรวิทย์ นันทพินิจ", "ดรัณภพ ธนากานต์", "พชระ รัศมีเดช",
    "ป้องเกียรติ นันทภักดิ์", "ธิศา กลิ่นโพธิ์", "ธนินท์ วรรณสิริ",
    "สุรยุทธ์ พงศ์พินิจ", "อัญชิสา ทองชัยภูมิ", "ภูริพัฒน์ ดุสิตวรรณ",
    "ณัฐรัชต์ ปรางค์ทรัพย์", "ภาคิน วรวงศ์คุณากร", "ณภัตรา พรมบุตร",
    "อานนท์ วีระกิตธนา", "ธัญญา ธาดาวรวงศ์", "วิชญาพร ประชายุต",
    "สุนิศา สตาภิรมย์", "พงศ์ สิริปัจทรัพย์", "พิชญาภรณ์ กิตติภัทรา",
    "กลวัชร วัฒนกิจเวช", "ยศธร ก้องวัฒนะกุล", "นิญา สวัสดิวงศ์",
    "สิตาพัชญ์ มงคลจิต", "วิมลพักตร์ สุพรรณภาคิน", "เปรมา พันธ์ภูผา",
    "กุลนันท์ จันทรสมเกียรติ", "สุรเชษฐ์ แก้วมาลา", "ชัญญา สิริวาณิชย์",
    "สุพิญญา สุขเกษร", "อธิฐาน กาญจนาศักดาพร", "ธัญญา ธาราวงศ์",
    "นวตา เฉลิมประเสริฐ", "ภูมิ แสนศิรี", "วรรณิศา วงศ์เจริญ",
    "บัลยงก์ สิริวาณิชย์", "ไรยา วีรภัทรเมธี", "เอกชัย ภูภาค",
    "พัฒนภัทร ภัชรภิรมย์", "กมาลา ต้นทอง", "เมษา วรวุฒิอนันตกุล",
    "ณิชนันทน์ สุวรรณวงศ์", "พรต พงศ์พาณิชย์", "พีรยา ปรางค์ทรัพย์",
    "ถิรพุทธ พงศ์พาณิชย์", "กฤติธัช โสภาภักดิ์", "เจนจิรา ศิริพัฒน์",
    "นิศา นวลจันทร์", "นรุตมา ปิติวัฒน์", "ปีวรา วรารักษ์",
    "ถิรพล สกุลวงศ์", "ภูริวัฒน์ จีระวงษา", "ณัฐ ปราสาทงาม",
    "เจิมจันทร์ แสงกระจ่าง", "เนกษ์ วิวัฒนาศักดิ์", "คัทลียา ดุสิตวรรณ",
    "จันทร์ทิพย์ ทรัพย์ปรีชา", "รังสิมันต์ พิชิตชัย", "บดินทร์ อุดมเดชรักษา",
    "จารีย์ วงศ์เจริญ", "ธิติรัตน์ ทรัพย์ปรีชา", "พรพิมล จันทร์ตรานันท์",
    "ชนินี วงวรางค์", "ศศิมา โตศิลา", "ตฤณ ปัทมเดชา",
    "เขมิกา พินิจนันท์", "ณัฐกิตติ์ เลิศวิทยา", "ชนาธินาถ วีระพงศ์ศาล",
    "จารีย์ ภัชรภิรมย์", "ชนิสา แสนเลิศ", "ปริญญา วีรภัทรเมธี",
]

# Sport choices (appropriate Thai sports)
SPORTS = ["ฟุตบอล", "แบดมินตัน", "วอลเลย์บอล", "ว่ายน้ำ", "เทนนิส", "ปิงปอง", "ยิงธนู", "กีฬาโต้สุ"]

# Gender choices (50/50 male/female)
GENDERS = ["ชาย", "หญิง"]

# Age choices (18-45 years old only)
AGES = ["18 - 25 ปี", "26 - 35 ปี", "36 - 45 ปี"]


def split_name(full_name: str) -> tuple:
    """Split Thai name into first name and last name"""
    parts = full_name.strip().split()
    if len(parts) >= 2:
        # Assume first word is first name, rest is last name
        firstname = parts[0]
        lastname = " ".join(parts[1:])
    else:
        firstname = full_name
        lastname = ""
    return firstname, lastname


def get_fbzx(session: requests.Session) -> str:
    """Extract fbzx token from form page"""
    try:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": VIEW_URL,
        }
        response = session.get(VIEW_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Search for fbzx value in HTML
        match = re.search(r'name="fbzx"\s+value="([^"]+)"', response.text)
        if match:
            return match.group(1)
        
        # Try alternative pattern
        match = re.search(r'"fbzx"\s*:\s*"([^"]+)"', response.text)
        if match:
            return match.group(1)
        
        raise ValueError("Could not find fbzx token")
    except Exception as e:
        print(f"Error getting fbzx: {e}")
        raise


def submit_form(session: requests.Session, firstname: str, lastname: str, 
                gender: str = None, age: str = None, sport: str = None) -> bool:
    """Submit the registration form"""
    try:
        # Get fresh fbzx token
        fbzx = get_fbzx(session)
        
        # Prepare form data
        data = {
            ENTRY_FIELDS["firstname"]: firstname,
            ENTRY_FIELDS["lastname"]: lastname,
            ENTRY_FIELDS["gender"]: gender or random.choice(GENDERS),
            ENTRY_FIELDS["age"]: age or random.choice(AGES),
            ENTRY_FIELDS["sport"]: sport or random.choice(SPORTS),
            "fvv": "1",
            "partialResponse": '[null,null,"616011175945338852"]',
            "pageHistory": "0",
            "fbzx": fbzx,
        }
        
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": VIEW_URL,
            "Content-Type": "application/x-www-form-urlencoded",
        }
        
        # Submit form
        response = session.post(POST_URL, data=data, headers=headers, 
                               allow_redirects=False, timeout=15)
        
        if response.status_code in (200, 302, 303):
            return True
        else:
            print(f"  Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  Error: {e}")
        return False


def main():
    print(f"Starting registration for {len(REGISTRANTS)} people")
    print(f"Form: {VIEW_URL}")
    print(f"Delay: 15 seconds between submissions (4 people/minute)")
    print(f"Gender: 50% Male, 50% Female")
    print(f"Age: 18-45 years old only")
    print(f"Sports: Thai sports randomly selected\n")
    
    results = {
        "total": len(REGISTRANTS),
        "success": 0,
        "failed": 0,
        "results": []
    }
    
    session = requests.Session()
    
    for idx, name in enumerate(REGISTRANTS, 1):
        firstname, lastname = split_name(name)
        
        print(f"[{idx}/{len(REGISTRANTS)}] Submitting: {firstname} {lastname}...", end=" ")
        
        success = submit_form(session, firstname, lastname)
        
        if success:
            print("✓ OK")
            results["success"] += 1
            results["results"].append({
                "name": name,
                "firstname": firstname,
                "lastname": lastname,
                "status": "Success"
            })
        else:
            print("✗ FAILED")
            results["failed"] += 1
            results["results"].append({
                "name": name,
                "firstname": firstname,
                "lastname": lastname,
                "status": "Failed"
            })
        
        # Wait 15 seconds before next submission (except for last one)
        if idx < len(REGISTRANTS):
            print(f"  Waiting 15 seconds before next submission...")
            for remaining in range(15, 0, -1):
                print(f"\r  {remaining} seconds remaining...", end="", flush=True)
                time.sleep(1)
            print("\n")
    
    # Print summary
    print("\n" + "="*60)
    print(f"SUMMARY")
    print("="*60)
    print(f"Total: {results['total']}")
    print(f"Success: {results['success']}")
    print(f"Failed: {results['failed']}")
    print(f"Success Rate: {(results['success']/results['total']*100):.1f}%")
    
    # Save results to CSV
    output_file = "registration_results.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "firstname", "lastname", "status"])
        writer.writeheader()
        writer.writerows(results["results"])
    
    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
