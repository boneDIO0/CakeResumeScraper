# db_export.py
import psycopg2
import json

# 載入爬蟲產出的 JSON 檔案（或直接從程式傳入 jobs list 也可）
with open("cake_jobs_pages.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

# 資料庫連線設定
conn = psycopg2.connect(
    dbname="cake",
    user="postgres",
    password="stanley*0916",
    host="localhost",  # 如果你本機跑 PostgreSQL
    port=5432
)

cur = conn.cursor()

# 寫入每一筆職缺資料
for job in jobs:
    cur.execute("""
        INSERT INTO jobs (title, url, company, location, requirements)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        job["title"],
        job["url"],
        job["company"],
        job["location"],         # PostgreSQL 可以直接接收 Python list 當作陣列
        job["requirements"]
    ))

conn.commit()
cur.close()
conn.close()

print(f"✅ 共寫入 {len(jobs)} 筆資料到資料庫")
