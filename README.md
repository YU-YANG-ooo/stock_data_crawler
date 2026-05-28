# Stock Data Crawler（股票新聞爬蟲與資料庫整合）

以 Python 建立的股票資料自動化系統，整合股價抓取，財經新聞 Google News RSS 爬蟲與 PostgreSQL資料庫，支援資料查詢與匯出Excel。

---
## 功能特色
- 股價自動抓取：透過 `yfinance` 抓取指定股票近一年歷史股價
- 財經新聞爬蟲：透過 Google News RSS Feed 抓取指定關鍵字的新聞
- 資料庫整合：所有資料自動寫入 PostgreSQL，避免重複寫入
- 新聞查詢：支援依股票代號與日期區間查詢新聞
- 匯出 Excel：查詢結果自動匯出為格式化 Excel 檔案
- 股價查詢並繪製均線與成交量圖表
- 新聞情緒分析（正向/負向/中性分類）
## 專案結構
```
stock_data_crawler/
|--main.py
|--stock_data.py
|--news_data.py
|--db.py
|--db.ini.example
|--pyproject.toml
|--chart.py
|--sentiment.py
```
## 環境需求
- Python 3.x
- PostgreSQL 16
- 套件管理工具(Poetry 或 pip 擇一)

### 已使用套件
|套件|用途|
|-|-|
|`requests`|HTTP請求|
|`beautifulsoup4`|HTML/XML解析|
|`lxml`|RSS XML解析器|
|`yfinance`|股價資料抓取|
|`psycopg2-binary`|PostgreSQL連線|
|`pandas`|資料處理與格式建立|
|`openpyxl`|Excel匯出|
|`matploylib`|股價成交量整合圖表繪製|
## 安裝與設定

**1. 安裝套件**

使用 Poetry：
```bash
poetry install
```

或使用 pip：
```bash
pip install requests beautifulsoup4 lxml yfinance psycopg2-binary pandas openpyxl matplotlib
```

**2. 進入虛擬環境**

使用 Poetry：
```bash
eval $(poetry env activate)
```

使用 venv：
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. 設定資料庫連線**

複製範本並填入你的設定：
```bash
cp db.ini.example db.ini
```
## 使用方式
```bash
python3 main.py
```
啟動後會出現選單：
```
=====股票資料系統=====
1.抓取股價與新聞資料
2.查詢股票相關新聞
3.查詢股價與新聞並繪製成圖表
4.離開程式
```
- **選項 1** : 輸入股票代號（如`2330.TW`）與關鍵字，自動抓取股價與新聞並寫入資料庫
- **選項 2** : 輸入股票代號與日期區間，查詢新聞並匯出Excel檔案
- **選項 3** : 輸入股票代號與日期區間，繪製股價交易量整合新聞情緒圖表
- **選項 4** : 離開程式
## 資料庫結構

### stocks_data

| 欄位 | 型別 | 說明 |
|-|-|-|
| date | DATE | 日期（主鍵） |
| stock_id | VARCHAR(10) | 股票代號（主鍵） |
| open | FLOAT | 開盤價 |
| high | FLOAT | 最高價 |
| low | FLOAT | 最低價 |
| close | FLOAT | 收盤價 |
| volume | BIGINT | 成交量 |

### news_data

| 欄位 | 型別 | 說明 |
|-|-|-|
| link | TEXT | 新聞連結（主鍵） |
| stock_id | VARCHAR(10) | 股票代號 |
| title | TEXT | 新聞標題 |
| source | TEXT | 媒體來源 |
| pub_date | TIMESTAMP | 發布時間 |

---

## 開發者

許瑀洋 （Kenny Hsu）

## 開發心得
- 處理 yfinance MultiIndex 欄位攤平問題
- 成交量柱狀圖顏色依漲跌判斷以當日收盤價與開盤價比較，收盤高於開盤顯示紅色（上漲），反之顯示綠色（下跌），透過 `list comprehension` 對每筆資料逐行判斷後產生顏色清單傳入 bar() 的 color 參數。
- 圖例 label 重複出現問題情緒標示在迴圈中每次 scatter() 都會加一個 label，導致圖例出現大量重複項目。解法是建立一個 set() 記錄已加入的 label，第一次加入後後續設為 None，避免重複顯示。
- 選單輸入保護（try/except）選單中若使用者輸入空白、錯誤格式或查無資料，程式會報錯中斷。透過空值檢查、預設值設定與 try/except 三層保護，確保程式不會因輸入問題崩潰。
- 新聞 pub_date 與股價 date 格式不相容，新聞的 pub_date 從資料庫取出後為 Timestamp 格式，股價的 date 為 datetime.date 格式，兩者無法直接比對。透過 pd.to_datetime().dt.date 統一轉換後才能正確對應。
- Excel 匯出找不到 engine，使用 df.to_excel() 匯出時需要指定 engine='openpyxl'，否則會報錯找不到可用的寫入引擎，需要額外安裝 `openpyxl` 套件。
- 標題清理全半形符號無法篩除，在 VS Code 中複製貼上 regex 符號時，全形符號會因編碼問題變成亂碼導致無法正確匹配，需要直接手動輸入全形符號或使用 Unicode 編碼（如 \u2013）才能正確篩除。
- 情緒判別關鍵字設計與每日情緒彙總。單純關鍵字比對無法理解語境，同一天可能同時有多篇正向與負向新聞。解法是將每篇新聞的情緒轉換為數值（正向 +1、負向 -1、中性 0），以日期 groupby 加總後判斷當日整體情緒傾向，避免單篇新聞主導結果。
- Google News RSS 無法取得歷史新聞
- 關鍵字比對無法理解語境，有時會產生誤判（例：利多出盡）
- 特定股票新聞量過大因此新聞日期涵蓋量很短