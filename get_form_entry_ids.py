# get_form_all_entries.py
import re, json, csv
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

# ===== แก้เฉพาะบรรทัดนี้ =====
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdhA8GSrZL5-4a0Q_rWnmfkW6KFphzxLDgzcqbwaH3AATwzmQ/viewform"
OUT_JSON = "entries_all.json"
OUT_CSV  = "entries_all.csv"
MAX_PAGES = 12  # กันไว้สุดๆ
# =============================

def to_viewform(url: str) -> str:
    u = urlparse(url)
    m = re.search(r"/forms/(?:u/\d+/)?(?:d/e|d)/([A-Za-z0-9_-]+)/", u.path)
    if not m:
        raise ValueError("หา FORM_ID ไม่เจอจาก URL")
    form_id = m.group(1)
    return f"https://docs.google.com/forms/d/e/{form_id}/viewform"

def extract_hidden_tokens(soup: BeautifulSoup):
    def val(name):
        el = soup.select_one(f'input[name="{name}"]')
        return el.get("value") if el else ""
    return {
        "fbzx": val("fbzx"),
        "fvv": val("fvv") or "1",
        "pageHistory": val("pageHistory") or "0",
        "token": val("token") or "",
    }

def dedup(seq):
    out, seen = [], set()
    for x in seq:
        if x and x not in seen:
            seen.add(x); out.append(x)
    return out

def extract_entries_from_page(soup: BeautifulSoup, page_index: int):
    results = []
    ids = []
    id_to_container = {}

    def probe_container(container):
        title = ""
        if container is None:
            return "", []
        head = container.select_one('[role="heading"], .freebirdFormviewerComponentsQuestionBaseHeader, .HoXoMd')
        if head:
            title = head.get_text(" ", strip=True)
        else:
            title = container.get_text(" ", strip=True)
            title = re.sub(r"\s{2,}", " ", title).strip()

        choices = []
        for lab in container.select("label, .ulDsOb span, .aDTYNe, .YEVVod span, .uVccjd span, .aDTYNe, .uVccjd, .YEVVod"):
            txt = lab.get_text(" ", strip=True)
            if txt and len(txt) <= 400 and not txt.endswith(":"):
                choices.append(txt)
        return title, dedup(choices)[:50]

    # --- 1) collect hidden inputs globally (some forms put name on hidden inputs only) ---
    for hid in soup.select('input[name^="entry."]'):
        nm = hid.get("name")
        m = re.match(r"entry\.(\d+)", nm or "")
        if not m:
            continue
        eid = m.group(1)
        if eid not in ids:
            ids.append(eid)
        # map container if hidden input sits near a question container
        node = hid
        for _ in range(8):
            node = getattr(node, "parent", None)
            if node is None: break
            if node.has_attr("role") and node["role"] in ("listitem", "group"):
                id_to_container[eid] = node
                break

    # --- 2) scan visible question containers for explicit 'entry.<num>' occurrences ---
    containers = list(soup.select('[role="listitem"], [role="group"], .freebirdFormviewerViewItemsItemItem, .freebirdFormviewerViewItemsItemItemRoot'))
    for cont in containers:
        html = cont.decode_contents() if getattr(cont, "decode_contents", None) else ""
        for m in re.finditer(r"entry\.(\d+)", html):
            eid = m.group(1)
            if eid not in ids:
                ids.append(eid)
            if eid not in id_to_container:
                id_to_container[eid] = cont

    # --- 3) parse data-params/jsmodel attributes for numeric IDs (Google Forms embeds ids there as bare numbers) ---
    for el in soup.find_all(attrs={"data-params": True}) + soup.find_all(attrs={"jsmodel": True}):
        texts = []
        for a in ("data-params", "jsmodel", "data-params-raw", "data-params-json"):
            if el.has_attr(a):
                texts.append(el.get(a, ""))
        joined = " ".join(texts)
        # collect long-ish numbers (entry ids are large integers)
        for num in re.findall(r"\b(\d{6,12})\b", joined):
            if num not in ids:
                ids.append(num)
            if num not in id_to_container:
                # try to find nearby container
                node = el
                for _ in range(8):
                    if node is None: break
                    if getattr(node, "has_attr", lambda x: False)("role") and node.get("role") in ("listitem", "group"):
                        id_to_container[num] = node
                        break
                    node = getattr(node, "parent", None)

    # --- 4) visible controls fallback: try to map controls to hidden inputs in their containers ---
    controls = list(soup.select('input:not([type="hidden"]), textarea, div[role="textbox"], div[contenteditable="true"], .Hvn9fb'))
    for el in controls:
        node = el
        for _ in range(10):
            node = getattr(node, "parent", None)
            if node is None: break
            if node.has_attr("role") and node["role"] in ("listitem", "group"):
                break
        container = node or (el.parent if getattr(el, "parent", None) else None)
        if container is None:
            continue
        # find a hidden input inside container
        hid = container.select_one('input[name^="entry."]')
        if hid and hid.get("name"):
            mm = re.match(r"entry\.(\d+)", hid.get("name"))
            if mm:
                eid = mm.group(1)
                if eid not in ids:
                    ids.append(eid)
                if eid not in id_to_container:
                    id_to_container[eid] = container

    # --- 5) final fallback: scan <script> text for 'entry.<num>' occurrences ---
    if not ids:
        script_text = "\n".join(s.get_text(" ", strip=True) for s in soup.find_all("script"))
        for m in re.finditer(r"entry\.(\d+)", script_text):
            eid = m.group(1)
            if eid not in ids:
                ids.append(eid)

    # assemble results using available container/title/choices info
    for eid in ids:
        if not re.match(r"^\d+$", eid):
            continue
        if any(r.get("entry") == eid for r in results):
            continue
        cont = id_to_container.get(eid)
        title, choices = probe_container(cont)
        results.append({
            "page": page_index,
            "entry": eid,
            "name": f"entry.{eid}",
            "title": title,
            "choices_hint": choices
        })

    return results

def fetch_page(session: requests.Session, url: str, headers: dict, data: dict | None):
    r = session.post(url, data=data, headers=headers, timeout=30) if data else session.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def main():
    view_url = to_viewform(FORM_URL)
    form_response_url = view_url.replace("/viewform", "/formResponse")

    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": view_url,
        "Accept-Language": "th,en;q=0.8",
    }

    # --- Start with Page 0 ---
    current_soup = fetch_page(session, view_url, headers, data=None)
    tokens = extract_hidden_tokens(current_soup)
    all_entries = []
    
    page_hist = []
    for current_page_index in range(MAX_PAGES):
        # 1. Extract entries from the current page
        page_entries = extract_entries_from_page(current_soup, page_index=current_page_index)
        
        # If no new entries are found, we've likely reached the end.
        known_entries = {e["entry"] for e in all_entries}
        new_entries = [e for e in page_entries if e["entry"] not in known_entries]
        if not new_entries and current_page_index > 0:
            print(f"Page {current_page_index}: No new entries found. Assuming end of form.")
            break
        
        all_entries.extend(new_entries)

        # 2. Prepare payload to navigate to the NEXT page
        page_hist.append(str(current_page_index))
        payload = {
            "fvv": tokens["fvv"],
            "fbzx": tokens["fbzx"],
            "pageHistory": ",".join(page_hist),
            "draftResponse": "[]", # Keep this for navigation
        }
        if tokens.get("token"):
            payload["token"] = tokens["token"]

        # 3. Add DUMMY answers for the current page's entries to pass validation
        for entry_data in page_entries:
            # For choice-based questions, use the first choice hint. Otherwise, use a dummy text.
            dummy_answer = entry_data["choices_hint"][0] if entry_data["choices_hint"] else "dummy_text"
            payload[entry_data["name"]] = dummy_answer
            # For radio buttons, a sentinel is sometimes needed
            if "_sentinel" not in entry_data["name"]:
                 payload[f'{entry_data["name"]}_sentinel'] = ""


        # 4. POST to get the next page's content
        print(f"Navigating from page {current_page_index}...")
        try:
            current_soup = fetch_page(session, form_response_url, headers, data=payload)
        except requests.exceptions.HTTPError as e:
            print(f"Failed to navigate past page {current_page_index}. Maybe the form ended or an unhandled question type was found. Error: {e}")
            break

    # กำจัดซ้ำข้ามหน้า (กรณี DOM ซ้ำ)
    # Use an ordered dict keyed by normalized entry id to reliably remove duplicates
    from collections import OrderedDict
    od = OrderedDict()
    for e in all_entries:
        key = str(e.get("entry", "")).strip()
        if key and key not in od:
            od[key] = e
    all_entries = list(od.values())

    # แสดงผล
    print(f"\nForm view: {view_url}")
    print(f"พบ entries ทั้งหมด: {len(all_entries)}\n")
    for e in all_entries:
        print(f'[{e["page"]}] {e["name"]}: {e["title"][:120]}')
        if e["choices_hint"]:
            print("   choices_hint:", e["choices_hint"][:6], "..." if len(e["choices_hint"])>6 else "")

    # บันทึกไฟล์
    if OUT_JSON:
        with open(OUT_JSON, "w", encoding="utf-8") as f:
            json.dump({"view_url": view_url, "entries": all_entries}, f, ensure_ascii=False, indent=2, default=str)
        print(f"\nSaved JSON -> {OUT_JSON}")

    if OUT_CSV:
        with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["page", "entry_id", "name", "title", "choices_hint"])
            for e in all_entries:
                w.writerow([e["page"], e["entry"], e["name"], e["title"], " | ".join(e["choices_hint"])])
        print(f"Saved CSV -> {OUT_CSV}")

if __name__ == "__main__":
    main()
