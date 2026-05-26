import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# ================= 👑 你的完美正確密鑰（請勿更動） 👑 =================
TELEGRAM_BOT_TOKEN = '8982537531:AAHNZE6Dj8jhoU4k70t97DwLebcx9iT1H1Q'
TELEGRAM_CHAT_ID = '1411929518'
# =========================================================================

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def get_yahoo_news():
    url = "https://finance.yahoo.com/news/rssindex"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            news = []
            for item in root.findall('.//item')[:3]:  # 抓3條Yahoo新聞
                title = item.find('title').text
                link = item.find('link').text
                news.append(f"📰 {title}\n🔗 連結: {link}")
            return "\n\n".join(news)
    except:
        pass
    return "暫無最新財經新聞"

def get_twitter_rss(username, display_name):
    # 使用免費的 RSSHub 橋樑獲取 Twitter 內容
    url = f"https://rsshub.app/twitter/user/{username}/replies=0"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            items = root.findall('.//item')
            if items:
                # 抓取該大佬最新的一條推文
                title = items[0].find('title').text
                # 簡單清洗一下太長的字
                if len(title) > 80: title = title[:80] + "..."
                return f"🐦 【{display_name}】最新發言：\n💬 {title}"
    except:
        pass
    return f"🐦 【{display_name}】今日無發言或抓取失敗"

if __name__ == "__main__":
    today = datetime.today().strftime('%Y-%m-%d')
    
    # 1. 抓取新聞
    yahoo_section = get_yahoo_news()
    
    # 2. 抓取 Twitter 大佬們的消息
    bloomberg_tweet = get_twitter_rss('DeitaXtreme', 'Walter Bloomberg 突發新聞')
    whales_tweet = get_twitter_rss('unusual_whales', 'Unusual Whales 華爾街內幕')
    bilello_tweet = get_twitter_rss('charliebilello', 'Charlie Bilello 數據大師')
    
    # 3. 組裝成超級大報告
    report = (
        f"🌟 🌟 【全球市場情報站 - {today}】 🌟 🌟\n\n"
        f"📊 【Yahoo 財經頭條】\n{yahoo_section}\n\n"
        f"---------------------------\n"
        f"🔥 【Twitter 大佬實時觀測】\n\n"
        f"{bloomberg_tweet}\n\n"
        f"{whales_tweet}\n\n"
        f"{bilello_tweet}"
    )
    
    # 4. 發送給 Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': report, 'disable_web_page_preview': True}
    
    res = requests.post(url, json=payload)
    print(f"發送結果: {res.status_code}")
