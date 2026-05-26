import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# ================= 🚨 已自動為你填入加密密鑰 🚨 =================
TELEGRAM_BOT_TOKEN = '8982537531:AAFcNzqKE3FXTCzchHRZRZ9EIRRdLNc1MI'
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
                news_list.append(f"📰 *{title}*\n🔗 [點擊閱讀]({link})")
            return "\n\n".join(news_list)
    except Exception as e:
        return f"新聞抓取失敗: {str(e)}"
    return "暫無最新財經新聞"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    today = datetime.today().strftime('%Y-%m-%d')
    report_text = f"🌟 *【全球市場財經情報 - {today}】* 🌟\n\n"
    report_text += "📊 __全球財經頭條__\n\n"
    report_text += get_global_news()
    
    send_telegram(report_text)
