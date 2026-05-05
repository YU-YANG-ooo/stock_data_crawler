import psycopg2
import pandas as pd
from configparser import ConfigParser

parser = ConfigParser()
parser.read('db.ini')

#表格欄位初始化建立
def init_db():
    create_stocks = '''
        CREATE TABLE IF NOT EXISTS stocks_data(
            date        DATE NOT NULL,
            stock_id    VARCHAR(10) NOT NULL,
            open        FLOAT,
            high        FLOAT,
            low         FLOAT,
            close       FLOAT,
            volume      BIGINT,
            PRIMARY KEY(date, stock_id)
        );
    '''
    
    create_news = '''
        CREATE TABLE IF NOT EXISTS news_data(
            link        TEXT PRIMARY KEY,
            stock_id    VARCHAR(10) NOT NULL,
            title       TEXT NOT NULL,
            source      TEXT,
            pub_date    TIMESTAMP
        );
    '''
    
    with psycopg2.connect(**parser['postgres']) as conn:
        with conn.cursor() as cur:
            cur.execute(create_stocks)
            cur.execute(create_news)
        conn.commit()
    print('------資料庫初始化完成-----')

#股價資料寫入postgres
def insert_stock_data(df):
    insert_sql = '''
        INSERT INTO stocks_data(date, stock_id, open, high, low, close, volume)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT(date, stock_id) DO NOTHING;
    '''
    with psycopg2.connect(**parser['postgres']) as conn:
        with conn.cursor() as cur:
            for index, row in df.iterrows():
                cur.execute(insert_sql, (
                    row['Date'].date(),
                    row['stock_id'],
                    row['Open'],
                    row['High'],
                    row['Low'],
                    row['Close'],
                    int(row['Volume'])
                ))
        conn.commit()
    print('----股價寫入完成----')

#新聞寫入postgres
def insert_news_data(news_list):
    insert_sql = '''
        INSERT INTO news_data(link, stock_id, title, source, pub_date)
        VALUES(%s, %s, %s, %s, %s)
        ON CONFLICT(link) DO NOTHING;
    '''
    with psycopg2.connect(**parser['postgres']) as conn:
        with conn.cursor() as cur:
            for news in news_list:
                cur.execute(insert_sql, (
                    news['link'],
                    news['stock_id'],
                    news['title'],
                    news['source'],
                    news['pub_date']
                )) 
        conn.commit()
    print('----新聞寫入完成----')
    

#查詢功能
def query_news_by_date(stock_id, start_date, end_date):
    query_sql = '''
        SELECT pub_date, title, source, link
        FROM news_data
        WHERE stock_id = %s AND DATE(pub_date) BETWEEN %s AND %s
        ORDER BY pub_date DESC;
    '''
    with psycopg2.connect(**parser['postgres']) as conn:
        query_df = pd.read_sql_query(query_sql, conn, params = (stock_id, start_date, end_date))
    return query_df
    
#存檔功能
def save_to_excel(df, filename):
    df.to_excel(filename, index = False, engine = 'openpyxl')