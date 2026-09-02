# Alibaba RFQ Data Extraction Tool

## Overview

This project implements an automated web scraper in Python to extract Request for Quotation (RFQ) listings from Alibaba Sourcing. The application parses initial state data embedded within the web pages across all available pagination results, transforms the data according to the target specification, and exports the formatted dataset into a CSV file.

Target URL:
`https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y&tracelog=newest`

---

## Project Structure

```
├── Python Task.docx                  # Original assignment instructions
├── 2025-07-02 18-35-27.png           # Example RFQ card screenshot
├── alibaba_rfq_2025-06-12_212932.csv # Reference CSV template
├── scrape_alibaba_rfq.py             # Main Python web scraper script
├── alibaba_rfq_scraped.csv           # Final extracted CSV dataset
└── README.md                         # Project documentation
```

---

## Technical Specifications & Requirements

### System & Python Dependencies
- Python 3.8+
- Standard Library Modules: `urllib.request`, `re`, `json`, `csv`, `datetime`, `sys`, `os`

No external Python package dependencies are required to execute the scraper.

---

## Data Schema Definition

The generated CSV dataset (`alibaba_rfq_scraped.csv`) adheres to the following field specifications:

| Field Name | Type | Description |
| :--- | :--- | :--- |
| **RFQ ID** | String / Numeric | Unique identifier for the RFQ entry |
| **Title** | String | Subject title of the RFQ requirement |
| **Buyer Name** | String | Full name of the purchasing buyer |
| **Buyer Image** | String | URL path to the buyer profile image avatar |
| **Inquiry Time** | String | Relative timestamp string provided on the page |
| **Quotes Left** | Integer | Remaining available quote slots for suppliers |
| **Country** | String | Target destination country of the request |
| **Quantity Required** | String | Combined quantity value and unit of measurement |
| **Email Confirmed** | String (`Yes`/`No`) | Verification indicator for buyer email |
| **Experienced Buyer** | String (`Yes`/`No`) | Indicator for experienced buyer status |
| **Complete Order via RFQ** | String (`Yes`/`No`) | Indicator for past completed orders via RFQ |
| **Typical Replies** | String (`Yes`/`No`) | Indicator for buyer responsiveness |
| **Interactive User** | String (`Yes`/`No`) | Indicator for interactive platform activity |
| **Inquiry URL** | String | Absolute web URL to the RFQ details page |
| **Inquiry Date** | String (`DD-MM-YYYY`) | Derived date computed from relative Inquiry Time |
| **Scraping Date** | String (`DD-MM-YYYY`) | Date on which the data extraction was executed |

---

## Usage Instructions

### Running the Scraper

Execute the main Python script from the command line:

```bash
python scrape_alibaba_rfq.py alibaba_rfq_scraped.csv
```

If no output filename argument is provided, the script automatically defaults to generating `alibaba_rfq_scraped_<YYYY-MM-DD>.csv`.

### Execution Behavior
1. Navigates through pagination parameters (`page=1`, `page=2`, etc.).
2. Extracts JSON data structures (`window.PAGE_DATA["index"].data`).
3. Deduplicates entries using unique `RFQ ID` identifiers.
4. Concludes automatically upon encountering an empty page or zero new entries.
5. Writes UTF-8 encoded output with standard CSV formatting.

---

## Verification & Results

- **Total RFQs Scraped**: 778 records
- **Total Pages Processed**: 39 pagination pages
- **Output File**: `alibaba_rfq_scraped.csv`

