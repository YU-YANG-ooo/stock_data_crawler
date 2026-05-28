import re
import pandas as pd

positive_keywords = [
    '利多', '創新高', '漲', '突破', '買入', '財報亮眼', '營收成長', '獲利', '上漲', '強勢', '放量', '黃金交叉', '買盤',
    '擴廠', '合作', '受惠', '上看', '推進', '狂飆', '新高', '新天價', '轉機'
]

negative_keywords = [
    '利空', '創新低', '跌', '崩', '賣出', '下修', '虧損', '弱勢', '死亡交叉', '量縮', '賣壓', '減產', '恐', '警示',
    '風險', '過熱', '賣超', '棄', '大砍', '戰爭', '危險', '翻車', '修正'
]

def clean_title(title):
    title = re.split(r'\s[-－]\s', title)[0]
    title = re.sub(r'[(（][^)）]*[)）]', '', title)
    title = re.sub(r'【[^】]*】', '', title)
    title = re.sub(r'[《》「」〈〉]', '', title)
    title = re.sub(r'[／/|]', ' ', title)
    
    title = re.sub(r'\s+', ' ', title)
    title = title.strip()
    return title

def sentiment_classify(title):
    for keyword in positive_keywords:
        if keyword in title:
            return 'positive'
    for keyword in negative_keywords:
        if keyword in title:
            return 'negative'
    return 'neutral'


def get_daily_sentiment(news_df):
    news_df['clean'] = news_df['title'].apply(clean_title)
    news_df['sentiment'] = news_df['clean'].apply(sentiment_classify)
    news_df['date'] = pd.to_datetime(news_df['pub_date']).dt.date
    
    sentiment_score = {'positive': 1, 'negative': -1, 'neutral': 0}
    news_df['score'] = news_df['sentiment'].map(sentiment_score)
    
    daily = news_df.groupby('date')['score'].sum().reset_index()
    daily['label'] = daily['score'].apply(lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral'))
    return daily
