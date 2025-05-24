# scheduler.py

import schedule
import time
import logging
from extract_jobs import scrape_jobs

logging.basicConfig(
    filename='log/scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def job_task():
    try:
        logging.info("📦 爬蟲排程開始執行")
        scrape_jobs()
        logging.info("✅ 爬蟲排程成功完成")
    except Exception as e:
        logging.error(f"❌ 排程發生錯誤: {str(e)}")

# 每天早上 7 點執行
schedule.every().day.at("07:00").do(job_task)

print("⏳ 已啟動排程，等待每日 07:00 執行...")

while True:
    schedule.run_pending()
    time.sleep(1)
