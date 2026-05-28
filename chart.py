import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sentiment import clean_title, sentiment_classify, get_daily_sentiment

plt.rcParams['font.family'] = 'Arial Unicode MS'
plt.rcParams['axes.unicode_minus'] = False

def plot_stock(df, stock_id, news_df = None):
    df = df.sort_values('date')
    df['MA5'] = df['close'].rolling(5).mean()
    df['MA10'] = df['close'].rolling(10).mean()
    df['MA20'] = df['close'].rolling(20).mean()
    df['volume_K'] = df['volume'] / 1000
    df['ma20_volume'] = df['volume_K'].rolling(20).mean()

    
    fig, ax = plt.subplots(2, 1, figsize = (14, 12))
    
    ax[0].plot(df['date'], df['close'], label='Close', linewidth=1.5)
    ax[0].plot(df['date'], df['MA5'], label='MA5', linewidth=1)
    ax[0].plot(df['date'], df['MA10'], label='MA10', linewidth=1)
    ax[0].plot(df['date'], df['MA20'], label='MA20', linewidth=1)
    
    if news_df is not None:
        daily = get_daily_sentiment(news_df)
        
        added_labels = set()
        for _, row in daily.iterrows():
            match = df[df['date'] == row['date']]
            if match.empty:
                continue
            price = match['close'].values[0]
            if row['label'] == 'positive':
                label = 'positive' if 'positive' not in added_labels else None
                added_labels.add('positive')
                ax[0].scatter(row['date'], price * 1.01, marker = '^', color = 'red', s = 50, zorder = 5, label = label)
            elif row['label'] == 'negative':
                nlabel = 'negative' if 'negative' not in added_labels else None
                added_labels.add('negative')
                ax[0].scatter(row['date'], price * 0.99, marker = 'v', color = 'green', s = 50, zorder = 5, label = nlabel)
                
    ax[0].set_title(f'{stock_id}股價趨勢和新聞情緒判別圖')
    ax[0].set_ylabel('價格')
    ax[0].legend()
    ax[0].grid(alpha = 0.3, linestyle = '--')
    ax[0].tick_params(axis = 'x', rotation = 45)
    
    colors = ['red' if c > o else 'green' for c, o in zip(df['close'], df['open'])]
    ax[1].bar(df['date'], df['volume_K'], color = colors, width = 0.5)
    ax[1].plot(df['date'], df['ma20_volume'], color = 'orange', linewidth = 1.5, label = 'MA20', alpha = 0.5)
    ax[1].set_title(f'{stock_id}成交量柱狀圖')
    ax[1].set_xlabel('日期')
    ax[1].set_ylabel('交易量(張)')
    ax[1].legend()
    ax[1].grid(alpha = 0.3, linestyle = '--')
    ax[1].tick_params(axis = 'x', rotation = 45)

    
    plt.tight_layout()
    plt.show()

