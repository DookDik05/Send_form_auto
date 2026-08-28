/**
 * AutoForm Pro Max - Thai Synthetic Identity & Demographic Dataset
 * Authentic thai names, surnames, phone numbers, provinces, and realistic comments
 */

export const THAI_NAMES = [
  "สมชาย", "สมหญิง", "ปิยะ", "กนก", "ชลธิชา", "ธีรนันท์", "อภิวัฒน์", "รัชนก", "พัชรพล", "อรณิชา",
  "กิตติพงษ์", "นัฐวุฒิ", "ศิริพร", "ธนภัทร", "วรัญญา", "ชัยวัฒน์", "ชุติมา", "ภูมิพัฒน์", "ณภัทร", "มนัสนันท์",
  "จิราภรณ์", "สุรศักดิ์", "วิภาวี", "เกรียงไกร", "นภัสสร", "ธนกร", "ปาณิสรา", "วรวิทย์", "ศุภชัย", "กานดา",
  "ทิพวรรณ", "เอกชัย", "สุพัตรา", "ธีรภัทร", "สุภาภรณ์", "วีรยุทธ", "กมลชนก", "ปฏิภาณ", "ดาริกา", "ทรงเกียรติ"
];

export const THAI_LASTNAMES = [
  "ใจดี", "เดชะ", "สุนทร", "วงศ์สุวรรณ", "ทิพย์มณี", "ศรีสุข", "เรืองรอง", "จิตอารี", "พงษ์ศักดิ์", "นาคินทร์",
  "ศิริวัฒนา", "รัตนไพศาล", "พงษ์พิพัฒน์", "ประเสริฐสุข", "เลิศวิริยะ", "สมบูรณ์ทรัพย์", "มงคลสวัสดิ์", "ตันติพาณิชย์",
  "ชัยประสิทธิ์", "สุขเกษม", "บุญญานุรักษ์", "เตชะวัฒนากุล", "สิริโภคา", "พิริยะกุล", "มณีรัตน์", "เกียรติขจร"
];

export const THAI_PROVINCES = [
  "กรุงเทพมหานคร", "อุดรธานี", "ขอนแก่น", "นนทบุรี", "ปทุมธานี", "เชียงใหม่", "ชลบุรี", "นครราชสีมา",
  "สงขลา", "ภูเก็ต", "อุบลราชธานี", "สุราษฎร์ธานี", "สมุทรปราการ", "พิษณุโลก", "ระยอง", "นครปฐม"
];

export const THAI_COMMENTS_BANK = [
  "การจัดกิจกรรมภาพรวมดีมาก วิทยากรให้ความรู้ชัดเจนครับ",
  "สถานที่จัดงานสะดวกสบาย เดินทางง่ายมาก",
  "อยากให้จัดกิจกรรมดีๆ แบบนี้อีกในอนาคตค่ะ",
  "ประทับใจการบริการของทีมงานทุกคน ให้ข้อมูลและคำแนะนำดีมาก",
  "เอกสารและสื่อประชาสัมพันธ์เข้าใจง่าย ครบถ้วน",
  "อาหารและเครื่องดื่มมีคุณภาพเพียงพอ ขอชื่นชมครับ",
  "ระบบลงทะเบียนรวดเร็ว ไม่ต้องรอนานเลย",
  "บรรยากาศในงานคึกคัก สนุกสนานและได้ประโยชน์จริง",
  "ขอขอบคุณผู้จัดงานและทีมงานทุกท่านสำหรับการดูแลเป็นอย่างดี",
  "ระยะเวลาในการบรรยายเหมาะสม ไม่เยิ่นเย้อ ได้เนื้อหาเน้นๆ ครับ"
];

export const THAI_ORGANIZATIONS = [
  "สำนักงานสาธารณสุขจังหวัด", "โรงพยาบาลศูนย์", "มหาวิทยาลัยขอนแก่น", "การกีฬาแห่งประเทศไทย",
  "สถาบันการพลศึกษา", "เทศบาลนครอุดรธานี", "องค์การบริหารส่วนจังหวัด", "สมาคมผู้ประกอบการ",
  "ศูนย์ส่งเสริมอุตสาหกรรมภาค", "สำนักงานส่งเสริมเศรษฐกิจดิจิทัล"
];

/**
 * Generate a realistic Thai random profile
 */
export function generateRandomThaiProfile() {
  const firstName = THAI_NAMES[Math.floor(Math.random() * THAI_NAMES.length)];
  const lastName = THAI_LASTNAMES[Math.floor(Math.random() * THAI_LASTNAMES.length)];
  const province = THAI_PROVINCES[Math.floor(Math.random() * THAI_PROVINCES.length)];
  const org = THAI_ORGANIZATIONS[Math.floor(Math.random() * THAI_ORGANIZATIONS.length)];
  const comment = THAI_COMMENTS_BANK[Math.floor(Math.random() * THAI_COMMENTS_BANK.length)];
  
  // Phone prefixes: 08x, 09x, 06x
  const prefixes = ["081", "082", "086", "089", "092", "094", "097", "061", "063", "065"];
  const prefix = prefixes[Math.floor(Math.random() * prefixes.length)];
  const suffix = Math.floor(1000000 + Math.random() * 9000000).toString().substring(0, 7);
  const phone = `${prefix}-${suffix.substring(0, 3)}-${suffix.substring(3)}`;
  
  // Mock email
  const engRomanNames = ["somchai", "somying", "piya", "kanok", "cholthicha", "teerapat", "apiwat", "nuttawut", "thanakorn", "varanya"];
  const emailDomain = ["gmail.com", "hotmail.com", "outlook.co.th", "yahoo.com"];
  const userNum = Math.floor(10 + Math.random() * 90);
  const email = `${engRomanNames[Math.floor(Math.random() * engRomanNames.length)]}.${lastName.substring(0, 3).toLowerCase()}${userNum}@${emailDomain[Math.floor(Math.random() * emailDomain.length)]}`;

  return {
    fullName: `${firstName} ${lastName}`,
    firstName,
    lastName,
    phone,
    email,
    province,
    organization: org,
    comment
  };
}
