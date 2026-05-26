import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import re

# ================= 👑 你的完美正確密鑰（請勿更動） 👑 =================
TELEGRAM_BOT_TOKEN = '8982537531:AAHNZE6Dj8jhoU4k70t97DwLebcx9iT1H1Q'
TELEGRAM_CHAT_ID = '1411929518'
# =========================================================================

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def clean_html(raw_html):
    if not raw_html: return "無內容摘要"
    clean_text = re.sub(r'<[^>]+>', '', raw_html)
    clean_text = clean_text.replace('&nbsp;', ' ').strip()
    return clean_text

def get_yahoo_news_with_summary():
    url = "https://finance.yahoo.com/news/rssindex"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            news = []
            for item in root.findall('.//item')[:3]:
                title = item.find('title').text
                link = item.find('link').text  # 👈 捉返條連結出嚟
                
                summary_el = item.find('description')
                raw_summary = summary_el.text if summary_el is not None else ""
                
                summary = clean_html(raw_summary)
                if not summary or summary == "無內容摘要":
                    summary = "請點擊下方連結查看即時內文"
                elif len(summary) > 100: 
                    summary = summary[:100] + "..."
                
                # 💡 終極排版：有標題、有摘要、兼且提供真正可點擊的連結！
                news.append(f"📌 *【{title}】*\n📝 內容摘要: {summary}\n🔗 完整內文: [點擊這裡跳轉]({link})")
            return "\n\n".join(news)
    except Exception as e:
        print(f"Yahoo 新聞出錯: {e}")
    return "暫無最新財經新聞"

def get_twitter_rss(username, display_name):
    urls = [
        f"https://rsshub.app/twitter/user/{username}/replies=0",
        f"https://nitter.net/{username}/rss"
    ]
    for url in urls:
        try:
            res = requests.get(url, headers=headers, timeout=8)
            if res.status_code == 200:
                root = ET.fromstring(res.content)
                items = root.findall('.//item')
                if items:
                    title = items[0].find('title').text
                    title = clean_html(title)
                    if len(title) > 100: title = title[:100] + "..."
                    return f"🌟 *【{display_name}】*\n💬 最新發言: {title}"
        except:
            continue
    return f"🌟 *【{display_name}】*\n💬 今日無發言或網絡暫時繁忙"

if __name__ == "__main__":
    today = datetime.today().strftime('%Y-%m-%d')
    
    yahoo_section = get_yahoo_news_with_summary()
    
    bloomberg_tweet = get_twitter_rss('DeitaXtreme', 'Walter Bloomberg 突發')
    whales_tweet = get_twitter_rss('unusual_whales', 'Unusual Whales 內幕期權')
    
    saylor_tweet = get_twitter_rss('saylor', 'Michael Saylor 比特幣之神')
    cobie_tweet = get_twitter_rss('cobie', 'Cobie 幣圈泰斗')
    
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
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID, 
        'text': report, 
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    
    res = requests.post(url, json=payload)
    print(f"發送結果: {res.status_code}")
