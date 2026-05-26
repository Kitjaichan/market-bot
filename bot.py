import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# ================= 👑 你的完美正確密鑰（請勿更動） 👑 =================
TELEGRAM_BOT_TOKEN = '8982537531:AAHNZE6Dj8jhoU4k70t97DwLebcx9iT1H1Q'
TELEGRAM_CHAT_ID = '1411929518'
# =========================================================================

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def get_yahoo_news_with_summary():
    url = "https://finance.yahoo.com/news/rssindex"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            news = []
            for item in root.findall('.//item')[:3]:  # 抓取前3條最核心新聞
                title = item.find('title').text
                
                summary_el = item.find('description')
                summary = summary_el.text if summary_el is not None else "無內容摘要"
                
                if "<" in summary:
                    summary = summary.split("<")[0]
                if len(summary) > 120: 
                    summary = summary[:120] + "..."
                
                news.append(f"📌 *【{title}】*\n📝 內容摘要: {summary}")
            return "\n\n".join(news)
    except:
        pass
    return "暫無最新財經新聞"

def get_twitter_rss(username, display_name):
    url = f"https://rsshub.app/twitter/user/{username}/replies=0"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            items = root.findall('.//item')
            if items:
                title = items[0].find('title').text
                if len(title) > 120: title = title[:120] + "..."
                return f"🌟 *【{display_name}】*\n💬 最新發言: {title}"
    except:
        pass
    return f"🌟 *【{display_name}】*\n💬 今日無發言或抓取暫時卡頓"

if __name__ == "__main__":
    today = datetime.today().strftime('%Y-%m-%d')
    
    # 1. 抓取有內文摘要的新聞
    yahoo_section = get_yahoo_news_with_summary()
    
    # 2. 抓取 Twitter 財經大佬消息
    bloomberg_tweet = get_twitter_rss('DeitaXtreme', 'Walter Bloomberg 突發')
    whales_tweet = get_twitter_rss('unusual_whales', 'Unusual Whales 內幕期權')
    
    # 3. 抓取 🪙 虛擬貨幣大佬消息
    saylor_tweet = get_twitter_rss('saylor', 'Michael Saylor 比特幣之神')
    cobie_tweet = get_twitter_rss('cobie', 'Cobie 幣圈泰斗')
    
    # 4. 組裝直讀大報告
    report = (
        f"🚀 🚀 *【全球市場 & 幣圈情報站 - {today}】* 🚀 🚀\n\n"
        f"📊 *【Yahoo 財經頭條直讀】*\n\n{yahoo_section}\n\n"
        f"---------------------------\n"
        f"🔥 *【美股大戶實時動態】*\n\n"
        f"{bloomberg_tweet}\n\n"
        f"{whales_tweet}\n\n"
        f"---------------------------\n"
        f"🪙 *【Crypto 虛擬貨幣狂潮】*\n\n"
        f"{saylor_tweet}\n\n"
        f"{cobie_tweet}"
    )
    
    # 5. 發送給 Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID, 
        'text': report, 
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    
    res = requests.post(url, json=payload)
    print(f"發送結果: {res.status_code}")
