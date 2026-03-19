import gspread
import requests
from bs4 import BeautifulSoup
from google.oauth2.service_account import Credentials

# ---------------- CONFIG ----------------
SERVICE_ACCOUNT_FILE = 'etf_portfolio_123456.json'  # il tuo file JSON corretto
SPREADSHEET_ID = '1Q0N4f5rY55FgLNLQnpHJKuPjxZshFLOH4PilTa45DPA'  # ID del tuo Google Sheet

ETF_LIST = [
    {"ticker": "DFE", "url": "https://it.investing.com/etfs/wisdomtree-europe-smallcap"},
    {"ticker": "XD3E", "url": "https://it.investing.com/etfs/db-xtrackers-dj-euro-stoxx-div30?cid=46970"},
    {"ticker": "DJE", "url": "https://it.investing.com/etfs/lyxor-dj-industrial-average?cid=47176"},
    {"ticker": "QDVE", "url": "https://it.investing.com/etfs/ishares-s-p-500-usd-info-tech"},
    {"ticker": "UST", "url": "https://it.investing.com/etfs/lyxor-nasdaq-100?cid=47239"},
    {"ticker": "TDIV", "url": "https://it.investing.com/etfs/think-morningstar-high-dividend?cid=1162915"},
    {"ticker": "XGSD", "url": "https://it.investing.com/etfs/db-xtrackers-stoxx-glbl-div-100?cid=47125"},
    {"ticker": "EUHD", "url": "https://it.investing.com/etfs/powshr-euro-stoxx-highdiv-lowvol-f?cid=1009159"},
    {"ticker": "VHYL", "url": "https://it.investing.com/etfs/vanguard-ftse-all-wld-high-div-yd-l?cid=1120081"},
    {"ticker": "PSRW", "url": "https://it.investing.com/etfs/powershares-dynamic-uk-fund?cid=1171405"},
    {"ticker": "HDLV", "url": "https://it.investing.com/etfs/powershares-sp-500-high-dividend-fr?cid=1164295"},
    {"ticker": "MLPD", "url": "https://it.investing.com/etfs/source-morningstar-us-energy-inf-ml"},
    {"ticker": "IAPD", "url": "https://it.investing.com/etfs/ishares-dj-asia-pacific-div.-30?cid=46899"},
    {"ticker": "LTAM", "url": "https://it.investing.com/etfs/ishares-msci-latin-america---gbp?cid=46941"},
    {"ticker": "EMHD", "url": "https://it.investing.com/etfs/invesco-ftse-em-high-div-low-vol?cid=1156298"},
    {"ticker": "EUNY", "url": "https://it.investing.com/etfs/ishares-dj-em-select-dividend-%C2%A3?cid=46600"},
    {"ticker": "WBIT", "url": "https://it.investing.com/etfs/btcw?cid=1173302"},
    {"ticker": "SGLD", "url": "https://it.investing.com/etfs/source-physical-gold-p-etc-certs?cid=951554"},
    {"ticker": "XAT1", "url": "https://it.investing.com/etfs/invesco-at1-cap-bnd-eur-hdg-dist"},
    {"ticker": "DTLE", "url": "https://it.investing.com/etfs/dtle?cid=1190530"},
    {"ticker": "SXRH", "url": "https://it.investing.com/etfs/ishares-tips-05-dist-share-class?cid=1145836"},
    {"ticker": "TREI", "url": "https://it.investing.com/etfs/trd1?cid=1188356"},
    {"ticker": "TIGR", "url": "https://it.investing.com/etfs/tigr-milan"},
    {"ticker": "XUHY", "url": "https://it.investing.com/etfs/xtrackers-usd-hiyld-corporate-bond?cid=1164504"},
    {"ticker": "IGLT", "url": "https://it.investing.com/etfs/ishares-ftse-uk-all-stks-gilt?cid=46914"},
    {"ticker": "VAGE", "url": "https://it.investing.com/etfs/vage"}
]

# ---------------- GOOGLE SHEETS (NUOVA VERSIONE) ----------------
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

# ---------------- FUNZIONE PREZZO ROBUSTA ----------------
def get_price_and_change(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        price_tag = soup.find('span', {'data-test': 'instrument-price-last'})
        var_tag = soup.find('span', {'data-test': 'instrument-price-change-percent'})
        
        if not price_tag:
            price_tag = soup.select_one('.top.bold.inlineblock')
        if not var_tag:
            var_tag = soup.select_one('.arial_20.greenFont, .arial_20.redFont')
        
        price = price_tag.text.strip() if price_tag else 'N/A'
        var_pct = var_tag.text.strip() if var_tag else 'N/A'
        
        return price, var_pct
    except:
        return 'N/A', 'N/A'

# ---------------- CICLO PRINCIPALE ----------------
for i, etf in enumerate(ETF_LIST, start=2):
    ticker = etf['ticker']
    url = etf['url']
    price, var_pct = get_price_and_change(url)
    
    sheet.update(range_name=f"A{i}", values=[[ticker]])
    sheet.update(range_name=f"B{i}", values=[[price]])
    sheet.update(range_name=f"C{i}", values=[[var_pct]])
    
    print(f"{ticker}: {price} ({var_pct})")

