import urllib.request
import re
import json
import csv
import sys
import os
from datetime import datetime, timedelta

def parse_rfq_item(js_str, scrape_date_str):
    # Clean JS hex escapes like \x2f -> /
    s = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), js_str)
    
    def extract_str(key):
        m = re.search(r'\b' + key + r'\s*:\s*([\'"])(.*?)\1', s, re.DOTALL)
        return m.group(2).strip() if m else ""

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
    if qty and unit:
        quantity_required = f"{qty} {unit}"
    elif qty:
        quantity_required = qty
    else:
        quantity_required = unit

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

def scrape_all_pages(base_url, output_csv):
    scrape_date_str = datetime.now().strftime("%d-%m-%Y")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    all_rfqs = []
    seen_ids = set()
    page = 1

    print(f"Starting Alibaba RFQ Scraper...")
    print(f"Target URL: {base_url}")
    print(f"Scraping Date: {scrape_date_str}\n")

    while True:
        url = f"{base_url}&page={page}"
        print(f"Fetching Page {page}...", flush=True)

        req = urllib.request.Request(url, headers=headers)
        try:
            html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Error fetching page {page}: {e}. Retrying once...")
            try:
                html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', errors='ignore')
            except Exception as e2:
                print(f"Failed page {page} fetch: {e2}. Stopping.")
                break

        matches = re.findall(r'window\.PAGE_DATA\["index"\]\.data\.push\((\{.*?\}\s*)\);', html, re.DOTALL)
        
        if not matches:
            print(f"No RFQs found on page {page}. Scraping finished.")
            break

        new_items_on_page = 0
        for m in matches:
            rfq = parse_rfq_item(m, scrape_date_str)
            rfq_id = rfq["RFQ ID"]
            if rfq_id not in seen_ids:
                seen_ids.add(rfq_id)
                all_rfqs.append(rfq)
                new_items_on_page += 1

        print(f"Page {page}: Extracted {len(matches)} items ({new_items_on_page} new, Total collected: {len(all_rfqs)})", flush=True)

        if new_items_on_page == 0:
            print(f"No new items on page {page}. Stopping.")
            break

        page += 1

    # Save to CSV
    fieldnames = [
        "RFQ ID", "Title", "Buyer Name", "Buyer Image", "Inquiry Time",
        "Quotes Left", "Country", "Quantity Required", "Email Confirmed",
        "Experienced Buyer", "Complete Order via RFQ", "Typical Replies",
        "Interactive User", "Inquiry URL", "Inquiry Date", "Scraping Date"
    ]

    with open(output_csv, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rfqs)

    print(f"\nScraping complete!")
    print(f"Total RFQs scraped: {len(all_rfqs)}")
    print(f"Output saved to: {output_csv}")
    return all_rfqs

if __name__ == "__main__":
    target_url = "https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y&tracelog=newest"
    output_filename = f"alibaba_rfq_scraped_{datetime.now().strftime('%Y-%m-%d')}.csv"
    
    # Also support writing to standard name or argument
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]

    scrape_all_pages(target_url, output_filename)
