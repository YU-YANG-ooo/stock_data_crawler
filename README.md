# Stock Data Crawler（股票新聞爬蟲與資料庫整合）

以Python建立的股票資料自動化系統，整盒股價抓取，財經新聞爬蟲與PostgreSQL資料庫，支援資料查詢與匯出Excel。

---
## 功能特色
- 股價自動抓取：透過 `yfinance` 抓取指定股票近一年歷史股價
- 財經新聞爬蟲：透過 Google News RSS Feed 抓取指定關鍵字的新聞
- 資料庫整合：所有資料自動寫入 PostgreSQL，避免重複寫入
- 新聞查詢：支援依股票代號與日期區間查詢新聞
- 匯出 Excel：查詢結果自動匯出為格式化 Excel 檔案
## 專案結構
```
stock_data_crawler/
|--main.py
|--stock_data.py
|--news_data.py
|--db.py
|--db.ini.example
|--pyproject.toml
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
## 安裝與設定

**1. 安裝套件**

使用 Poetry：
```bash
poetry install
```

或使用 pip：
```bash
pip install requests beautifulsoup4 lxml yfinance psycopg2-binary pandas openpyxl
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
3.離開程式 
```
- **選項 1** : 輸入股票代號（如`2330.TW`）與關鍵字，自動抓取股價與新聞並寫入資料庫
- **選項 2** : 輸入股票代號與日期區間，查詢新聞並匯出Excel檔案
- **選項 3** : 離開程式
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

許瑀洋 