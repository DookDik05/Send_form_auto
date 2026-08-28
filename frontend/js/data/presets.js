/**
 * AutoForm Pro Max - Campaign Presets based on actual repository scripts
 */

export const CAMPAIGN_PRESETS = [
  {
    id: "seagames-survey-33",
    title: "แบบประเมินซีเกมส์ ครั้งที่ 33 (SEA Games)",
    subtitle: "กิจกรรม INSPIRE THE GAME คลินิกกีฬา ปลุกพลังฝัน",
    url: "https://docs.google.com/forms/d/e/1FAIpQLSeklchUtv4O-H1SpMgWkBm1RVVJWgqqNO4KZeBeqaEtQt_UAg/viewform",
    script: "auto-fill-seagames-survey.py",
    targetCount: 150,
    concurrency: 8,
    delayMin: 0.4,
    delayMax: 0.9,
    mode: "httpx",
    tags: ["Satisfaction", "Multi-page", "Sports"],
    color: "#6366f1",
    questions: [
      {
        entry: "entry.1086328584",
        title: "สัญชาติ (Nationality)",
        type: "radio",
        options: [
          { label: "คนไทย (Thai)", weight: 92 },
          { label: "ต่างชาติ (Foreigner)", weight: 8 }
        ]
      },
      {
        entry: "entry.721007974",
        title: "เพศ (Gender)",
        type: "radio",
        options: [
          { label: "ชาย (Male)", weight: 48 },
          { label: "หญิง (Female)", weight: 48 },
          { label: "อื่นๆ (Other)", weight: 4 }
        ]
      },
      {
        entry: "entry.540972076",
        title: "ช่วงอายุ (Age Range)",
        type: "radio",
        options: [
          { label: "ต่ำกว่า 18 ปี", weight: 8 },
          { label: "18 - 25 ปี", weight: 35 },
          { label: "26 - 35 ปี", weight: 32 },
          { label: "36 - 45 ปี", weight: 15 },
          { label: "46 ปีขึ้นไป", weight: 10 }
        ]
      },
      {
        entry: "entry.1792294564",
        title: "ความพึงพอใจภาพรวมการจัดกิจกรรม",
        type: "likert",
        options: [
          { label: "5 = มากที่สุด (Highly Satisfied)", weight: 85 },
          { label: "4 = มาก (Satisfied)", weight: 15 },
          { label: "3 = ปานกลาง (Neutral)", weight: 0 },
          { label: "2 = น้อย (Dissatisfied)", weight: 0 },
          { label: "1 = น้อยที่สุด (Very Dissatisfied)", weight: 0 }
        ]
      }
    ]
  },
  {
    id: "fda-expo-2026",
    title: "แบบลงทะเบียน FDA Expo 2026",
    subtitle: "การประชุมวิชาการและนิทรรศการ อย.",
    url: "https://docs.google.com/forms/d/e/1FAIpQLSdhA8GSrZL5-4a0Q_rWnmfkW6KFphzxLDgzcqbwaH3AATwzmQ/viewform",
    script: "auto-fill-fda-expo.py",
    targetCount: 300,
    concurrency: 12,
    delayMin: 0.3,
    delayMax: 0.7,
    mode: "httpx",
    tags: ["Registration", "Medical", "High-Volume"],
    color: "#06b6d4",
    questions: [
      {
        entry: "entry.1498135098",
        title: "ชื่อ-นามสกุล ผู้เข้าร่วม",
        type: "synthetic_thai_name"
      },
      {
        entry: "entry.877086558",
        title: "สถานะการเข้าร่วม",
        type: "radio",
        options: [
          { label: "ได้ ฉันยินดีไปร่วมงาน", weight: 95 },
          { label: "ขออภัย ไม่สะดวกไปร่วมงาน", weight: 5 }
        ]
      },
      {
        entry: "entry.1424661284",
        title: "ช่องทางที่ทราบข่าวสาร",
        type: "radio",
        options: [
          { label: "เว็บไซต์ทางการ อย.", weight: 55 },
          { label: "โซเชียลมีเดีย (Facebook / X)", weight: 30 },
          { label: "หนังสือพิมพ์ / ป้ายประชาสัมพันธ์", weight: 10 },
          { label: "เพื่อนร่วมงานแนะนำ", weight: 5 }
        ]
      }
    ]
  },
  {
    id: "registration-890-batch",
    title: "Batch Registration 890 Records",
    subtitle: "นำเข้าชุดข้อมูลสังเคราะห์ 890 รายการพร้อมระบบคุม Rate Limit",
    url: "https://docs.google.com/forms/d/e/1FAIpQLSeFltPTHhM4uNfOSh0vDuAWL5M-TFzD8KQiuLKF8J3G9jSnlw/viewform",
    script: "auto-fill-register-890.py",
    targetCount: 890,
    concurrency: 15,
    delayMin: 0.2,
    delayMax: 0.5,
    mode: "httpx",
    tags: ["Batch 890", "CSV Import", "Stress Test"],
    color: "#10b981",
    questions: [
      {
        entry: "entry.2008007542",
        title: "สาขาที่ท่านใช้บริการ",
        type: "radio",
        options: [
          { label: "เดอะมอลล์ไลฟ์สโตร์ ท่าพระ", weight: 22 },
          { label: "เดอะมอลล์ไลฟ์สโตร์ งามวงศ์วาน", weight: 28 },
          { label: "เดอะมอลล์ไลฟ์สโตร์ บางแค", weight: 20 },
          { label: "เดอะมอลล์ไลฟ์สโตร์ บางกะปิ", weight: 20 },
          { label: "เดอะมอลล์ โคราช", weight: 10 }
        ]
      }
    ]
  },
  {
    id: "selenium-human-bypass",
    title: "Anti-Detection Selenium Humanizer",
    subtitle: "จำลองพฤติกรรมมนุษย์ผ่าน Chrome Headless พร้อมสุ่ม Keystroke",
    url: "https://docs.google.com/forms/d/e/1FAIpQLSfGErFMwiRBEn0Y5yNulltD9u_Ypag-b0U6wG_BHXP_TMxXEA/viewform",
    script: "auto-fill-selenium.py",
    targetCount: 50,
    concurrency: 4,
    delayMin: 1.2,
    delayMax: 2.5,
    mode: "selenium",
    tags: ["Selenium", "Anti-Bot", "Realistic Timing"],
    color: "#f59e0b",
    questions: [
      {
        entry: "entry.1498135098",
        title: "ชื่อผู้ลงทะเบียน",
        type: "synthetic_thai_name"
      },
      {
        entry: "entry.2606285",
        title: "ความคิดเห็นเพิ่มเติม",
        type: "synthetic_thai_comment"
      }
    ]
  }
];
