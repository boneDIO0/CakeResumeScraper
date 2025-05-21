from bs4 import BeautifulSoup

def clean_text(text: str) -> str:
    """去除多餘空白與換行符號"""
    return text.strip().replace("\xa0", " ").replace("\r", "").replace("\n", " ").strip()

def clean_html(raw_html: str) -> str:
    """移除 HTML 標籤 + 清理文字"""
    soup = BeautifulSoup(raw_html, "html.parser")
    return clean_text(soup.get_text())

def normalize_list(items: list[str]) -> list[str]:
    """清洗 list 內容，去除多餘空白"""
    return [clean_text(item) for item in items if item.strip()]

def html_to_list(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    return [li.get_text(strip=True) for li in soup.select("li")]
