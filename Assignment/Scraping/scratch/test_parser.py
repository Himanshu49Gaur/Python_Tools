import re
import json
from datetime import datetime, timedelta

def parse_rfq_item(js_str, scrape_date_str="02-09-2026"):
    # Clean JS hex escapes like \x2f -> /
    s = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), js_str)
    
    # Helper to extract regex key string values
    def extract_str(key):
        m = re.search(r'\b' + key + r'\s*:\s*([\'"])(.*?)\1', s, re.DOTALL)
        return m.group(2).strip() if m else ""

    # Helper to extract parseInt or raw number
    def extract_num(key):
        m = re.search(r'\b' + key + r'\s*:\s*parseInt\(["\']?(\d+)["\']?', s)
        if m:
            return m.group(1)
        m = re.search(r'\b' + key + r'\s*:\s*["\']?(\d+)["\']?', s)
        return m.group(1) if m else "0"

    rfq_id = extract_str("id") or extract_str("rfqId")
    title = extract_str("subject")
    buyer_name = extract_str("buyerName")
    portrait_path = extract_str("portraitPath")
    if portrait_path:
        if portrait_path.startswith("http") or portrait_path.startswith("//"):
            buyer_image = portrait_path
        else:
            buyer_image = f"//ae01.alicdn.com/kf/{portrait_path}"
            if not buyer_image.endswith(".jpg"):
                buyer_image += "_50x50.jpg"
    else:
        buyer_image = ""

    inquiry_time = extract_str("openTimeStr")
    quotes_left = extract_num("rfqLeftCount")
    country = extract_str("country")
    
    qty = extract_str("quantity") or extract_str("quantityValue")
    unit = extract_str("quantityUnit") or extract_str("quantityValueUnit")
    quantity_required = f"{qty} {unit}".strip()

    # Extract tags
    tags_match = re.search(r'tags:\s*(\[.*?\])\s*\|\|', s, re.DOTALL)
    tags = []
    if tags_match:
        tag_json_str = tags_match.group(1)
        tag_json_str = re.sub(r'([a-zA-Z0-9_]+)\s*:', r'"\1":', tag_json_str)
        try:
            tags = json.loads(tag_json_str)
        except Exception:
            pass
    
    tag_names = {t.get("tagName") for t in tags if isinstance(t, dict)}
    email_confirmed = "Yes" if "emailConfirm" in tag_names else "No"
    experienced_buyer = "Yes" if "experienced_buyer" in tag_names else "No"
    complete_order_via_rfq = "Yes" if "complete_order_via_rfq" in tag_names else "No"
    typical_replies = "Yes" if "typically_replies" in tag_names else "No"
    interactive_user = "Yes" if "interactive_user" in tag_names else "No"

    inquiry_url = extract_str("url")
    if inquiry_url.startswith("//"):
        inquiry_url = "https:" + inquiry_url
    elif inquiry_url.startswith("/"):
        inquiry_url = "https://sourcing.alibaba.com" + inquiry_url

    # Calculate Inquiry Date from Inquiry Time
    scrape_dt = datetime.strptime(scrape_date_str, "%d-%m-%Y")
    inquiry_date = scrape_date_str
    
    inquiry_time_lower = inquiry_time.lower()
    days_match = re.search(r'(\d+)\s*day', inquiry_time_lower)
    months_match = re.search(r'(\d+)\s*month', inquiry_time_lower)
    years_match = re.search(r'(\d+)\s*year', inquiry_time_lower)
    
    if days_match:
        days = int(days_match.group(1))
        inquiry_dt = scrape_dt - timedelta(days=days)
        inquiry_date = inquiry_dt.strftime("%d-%m-%Y")
    elif months_match:
        months = int(months_match.group(1))
        inquiry_dt = scrape_dt - timedelta(days=months*30)
        inquiry_date = inquiry_dt.strftime("%d-%m-%Y")
    elif years_match:
        years = int(years_match.group(1))
        inquiry_dt = scrape_dt - timedelta(days=years*365)
        inquiry_date = inquiry_dt.strftime("%d-%m-%Y")
    else:
        inquiry_date = scrape_date_str

    return {
        "RFQ ID": rfq_id,
        "Title": title,
        "Buyer Name": buyer_name,
        "Buyer Image": buyer_image,
        "Inquiry Time": inquiry_time,
        "Quotes Left": quotes_left,
        "Country": country,
        "Quantity Required": quantity_required,
        "Email Confirmed": email_confirmed,
        "Experienced Buyer": experienced_buyer,
        "Complete Order via RFQ": complete_order_via_rfq,
        "Typical Replies": typical_replies,
        "Interactive User": interactive_user,
        "Inquiry URL": inquiry_url,
        "Inquiry Date": inquiry_date,
        "Scraping Date": scrape_date_str
    }

if __name__ == "__main__":
    with open('scratch/page.html', 'r', encoding='utf-8') as f:
        html = f.read()
    matches = re.findall(r'window\.PAGE_DATA\["index"\]\.data\.push\((\{.*?\}\s*)\);', html, re.DOTALL)
    if matches:
        res = parse_rfq_item(matches[0])
        for k, v in res.items():
            print(f"{k}: {v}")
