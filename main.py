from db import init_db, insert_stock_data, insert_news_data, query_news_by_date, save_to_excel
from stock_data import stock_data_get
from news_data import news_data_get
import datetime as dt

#建立TABLE
init_db()

while True:
    print('\n====股票資料系統====')
    print('1.抓取股價和新聞資料')
    print('2.查詢股票相關新聞')
    print('3.離開程式')
    
    choice = input('請選擇功能：').strip()
    
    if choice == '1':
        stock_input = input('請輸入股票代號（ex. 2330.TW, 6669.TW）：')
        stock_ids = [s.strip() for s in stock_input.split(',') if s.strip()]

        #確認股票與關鍵字數量一致
        while True:
            keyword_input = input('請輸入相對應數量的新聞關鍵字並用逗號分開：')
            keywords = [k.strip() for k in keyword_input.split(',') if k.strip()]
            
            if len(keywords) == len(stock_ids):
                break
            else:
                print('關鍵字與股票代碼數量不同，請重新輸入')

        for stock_id, keyword in zip(stock_ids, keywords):
            df = stock_data_get(stock_id)
            insert_stock_data(df)
            
            news_list = news_data_get(stock_id, keyword)
            insert_news_data(news_list)
            print('===股價和新聞抓取完成===')
        
    elif choice == '2':
        while True:
            query_stock = input('查詢哪隻股票的新聞（ex.2330.TW）:')
            query_start_date = input('查詢新聞的起始日期（ex.2026-04-28):')
            query_end_date = input('查詢新聞的結束日期（ex.2026-04-28):').strip()
            
            if not query_stock or not query_start_date:
                print('股票代碼和起始日期不能為空，請重新輸入')
                continue
            
            if not query_end_date:
                query_end_date = query_start_date
            
            try:
                result = query_news_by_date(query_stock, query_start_date, query_end_date)
                if result.empty:
                    print('查無資料，請重新輸入')
                else:
                    result['pub_date'] = result['pub_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
                    filename = input('請輸入查詢結果儲存的檔名：').strip()
                    if not filename:
                        filename = 'News_query'
                        
                    save_to_excel(result, f'{filename}.xlsx')
                    print(f'查詢結果已存成{filename}.xlsx')
                    break   
            except Exception as e:
                print(f'查詢發生錯誤：{e}，請重新輸入')

    elif choice == '3':
        print('===程式結束，感謝使用===')
        break
    
    else:
        print('請輸入有效的選項')