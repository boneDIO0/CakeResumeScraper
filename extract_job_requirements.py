import requests
from bs4 import BeautifulSoup
import json
import time
from cleaning import *

BASE_URL = "https://www.cake.me"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; StudentBot/1.0; +https://ncu.edu.tw)"
}

jobs = []

# 👇 設定要抓取幾頁職缺
for page in range(1, 6):  # 抓取第1～5頁
    print(f"📄 正在擷取第 {page} 頁資料...")
    list_url = f"{BASE_URL}/jobs?order=latest&page={page}"
    
    response = requests.get(list_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.select("div.JobSearchItem_container__oKoBL")

    for card in job_cards:
        try:
            title_tag = card.select_one("a[class^='JobSearchItem_jobTitle__']")
            company_tag = card.select_one("a[class^='JobSearchItem_companyName__']")
            location_tags = card.select("a[class^='JobSearchItem_featureSegmentLink__']")

            job_url = BASE_URL + title_tag["href"] if title_tag else ""
            requirements = ""

            # 👇 爬取職缺詳細頁面
            if job_url:
                detail_resp = requests.get(job_url, headers=HEADERS)
                detail_soup = BeautifulSoup(detail_resp.text, "html.parser")

                section_blocks = detail_soup.select("div.ContentSection_contentSection__ELRlG")
                for section in section_blocks:
                    h3 = section.select_one("h3.ContentSection_title__fcZYs")
                    if h3 and "職務需求" in h3.text:
                        content_div = section.select_one("div.ContentSection_content__e3ios")
                        if content_div:
                            requirements = content_div.get_text(separator="\n", strip=True)
                        break

            job = {
                "title": clean_text(title_tag.text) if title_tag else "",
                "url": job_url,
                "company": clean_text(company_tag.text) if company_tag else "",
                "location": normalize_list([tag.text for tag in location_tags]),
                "requirements": clean_html(str(content_div)) if content_div else ""
            }

            jobs.append(job)
            time.sleep(1)  # 延遲請求，避免被封鎖

        except Exception as e:
            print("❌ 擷取失敗：", e)

# 儲存成 JSON 檔案
with open("cake_jobs_pages.json", "w", encoding="utf-8") as f:
    json.dump(jobs, f, ensure_ascii=False, indent=2)

print(f"✅ 共擷取 {len(jobs)} 筆職缺資料，儲存至 cake_jobs_pages.json")

import csv

# 儲存成 CSV 檔案
with open("cake_jobs_pages.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "url", "company", "location", "requirements"])
    writer.writeheader()

    for job in jobs:
        writer.writerow({
            "title": job["title"],
            "url": job["url"],
            "company": job["company"],
            "location": "、".join(job["location"]),  # 將 list 轉為文字，逗號或頓號分隔
            "requirements": job["requirements"].replace("\n", " ")  # 清理換行符
        })

print("✅ 已輸出為 cake_jobs_pages.csv")
