import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# ================= 🚨 100% 精準校對版（不含任何多餘空格） 🚨 =================
TELEGRAM_BOT_TOKEN = '8982537531:AAFcNzqKE3FXTCzchHRZRZ9EIRRdLNc1MI'
TELEGRAM_CHAT_ID = '1411929518'
# =========================================================================

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
    report = f"🌟 【全球市場財經情報 - {today}】 🌟\n\n Bars 📊 全球財經頭條\n\n" + get_global_news()
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': report, 'disable_web_page_preview': True}
    
    res = requests.post(url, json=payload)
    print(f"發送結果: {res.status_code}, 內容: {res.text}")
