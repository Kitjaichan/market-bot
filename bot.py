import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# ================= 🚨 終極雙保險設定 🚨 =================
TELEGRAM_BOT_TOKEN = '8982537531:AAFcNzqKE3FXTCzchHRZRZ9EIRRdLNc1MI'

# 這裡我把「Emilio」的 ID 放進去，確保一定發得到
TELEGRAM_CHAT_ID = '1411929518' 
# =============================================================

def get_global_news():
    url = "https://finance.yahoo.com/news/rssindex"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            news_list = []
            for item in root.findall('.//item')[:5]:
                title = item.find('title').text
                link = item.find('link').text
                news_list.append(f"📰 {title}\n🔗 連結: {link}")
            return "\n\n".join(news_list)
    except Exception as e:
        return f"新聞抓取失敗: {str(e)}"
    return "暫無最新財經新聞"

if __name__ == "__main__":
    today = datetime.today().strftime('%Y-%m-%d')
    report = f"🌟 【全球市場財經情報 - {today}】 🌟\n\n📊 全球財經頭條\n\n" + get_global_news()
    
    # 發送發送！
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': report, 'disable_web_page_preview': True}
    
    # 這行會在 GitHub 紀錄裡印出有沒有成功發給 Telegram
    res = requests.post(url, json=payload)
    print(f"發送結果: {res.status_code}, 內容: {res.text}")
