import requests
from bs4 import BeautifulSoup
from datetime import datetime

#抓取Google News RSS 新聞
def news_data_get(stock_id, keyword):
    url = f'https://news.google.com/rss/search?q={keyword}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')
    news_list = []
    for item in items:
        pub_date_str = item.find('pubDate').text
        pub_date = datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %Z')
        
        news_list.append({
            'stock_id' : stock_id,
            'title' : item.find('title').text,
            'link' : item.find('link').text,
            'source' : item.find('source').text if item.find('source') else None,
            'pub_date' : pub_date
        })
    return news_list        