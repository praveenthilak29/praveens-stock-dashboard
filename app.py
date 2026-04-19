import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Stock LTP Dashboard", layout="wide")

# 🎨 DARK UI STYLE
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.main-title {
    font-size: 28px;
    font-weight: 600;
}
[data-testid="stDataFrame"] {
    border-radius: 10px;
    border: 1px solid #333;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Stock LTP Dashboard (200+ Stocks)</div>', unsafe_allow_html=True)

# 🔥 FULL STOCK LIST (200+)
base_stocks = [
"RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","SBIN","LT","HCLTECH",
"AXISBANK","WIPRO","MARUTI","BAJFINANCE","KOTAKBANK","ASIANPAINT",
"SUNPHARMA","TITAN","ULTRACEMCO","NESTLEIND","POWERGRID","NTPC",
"ONGC","ADANIENT","ADANIPORTS","COALINDIA","JSWSTEEL","TATASTEEL",
"HINDALCO","GRASIM","BPCL","BRITANNIA","CIPLA","DIVISLAB",
"EICHERMOT","HEROMOTOCO","HINDUNILVR","INDUSINDBK","BAJAJFINSV",
"DRREDDY","TECHM","UPL","SHREECEM","ITC","DLF","PIDILITIND",
"HDFCLIFE","SBILIFE","GODREJCP","AMBUJACEM","ACC","TORNTPHARM",
"MPHASIS","BANKBARODA","SIEMENS","ABB","BHEL","INDIGO",
"PAGEIND","COLPAL","VEDL","PEL","SAIL","CANBK","PNB","IDFCFIRSTB",

"ASHOKLEY","AUROPHARMA","BANDHANBNK","BERGEPAINT","BIOCON","BOSCHLTD",
"CADILAHC","CHOLAFIN","CONCOR","CROMPTON","DABUR","DALBHARAT",
"DEEPAKNTR","ESCORTS","EXIDEIND","FEDERALBNK","GAIL","GLENMARK",
"GMRINFRA","GNFC","GODREJPROP","HAL","HAVELLS","IBULHSGFIN",
"IDEA","IGL","INDHOTEL","IOC","IRCTC","JINDALSTEL",
"JKCEMENT","JSWENERGY","JUBLFOOD","L&TFH","LICHSGFIN",
"LUPIN","M&M","MCDOWELL-N","MFSL","MGL","MOTHERSUMI",
"MRF","NMDC","OBEROIRLTY","OFSS","PETRONET","PFC",
"PIIND","PNBHOUSING","POLYCAB","RAMCOCEM","RECLTD",
"SAIL","SRF","SUNTV","TATACHEM","TATACOMM",
"TATACONSUM","TATAMOTORS","TORNTPOWER","TRENT",
"TVSMOTOR","UBL","VOLTAS","ZEEL",

"AARTIIND","ALKEM","APOLLOHOSP","APOLLOTYRE","BATAIND",
"BEL","BHARATFORG","BALKRISIND","BANKINDIA","COFORGE",
"DELTACORP","EDELWEISS","GICRE",
"HDFCAMC","ICICIPRULI","IDBI","INDIAMART","INDUSTOWER",
"INTELLECT","IRB","JBCHEPHARM","JSL","KAJARIACER",
"KPITTECH","LAURUSLABS","MAHABANK","MANAPPURAM","METROPOLIS",
"MINDTREE","NATIONALUM","NAVINFLUOR","NHPC",
"OIL","PERSISTENT","PFIZER","PHOENIXLTD",
"RBLBANK","SBICARD","SCHAEFFLER","SOLARINDS","SONACOMS",
"SYNGENE","TATAELXSI","THERMAX","TRIDENT",
"UCOBANK","UNIONBANK","VARROC","VGUARD","VINATIORGA",
"WESTLIFE","ZENSARTECH"
]

stocks = [s + ".NS" for s in base_stocks]

# ⚡ DATA FETCH
@st.cache_data
def get_data(stock_list):
    data = yf.download(
        tickers=stock_list,
        period="2d",
        interval="1d",
        group_by='ticker',
        threads=True
    )

    rows = []

    for s in stock_list:
        try:
            close = data[s]["Close"].dropna()
            ltp = close.iloc[-1]
            prev = close.iloc[-2]

            change = round(ltp - prev, 2)
            percent = round((change / prev) * 100, 2)

            rows.append([s.replace(".NS",""), ltp, change, percent])
        except:
            rows.append([s.replace(".NS",""), "N/A", "N/A", "N/A"])

    return pd.DataFrame(rows, columns=["Stock", "LTP", "Change", "%"])

df = get_data(stocks)

# 🔍 SEARCH + REFRESH
col1, col2 = st.columns([3,1])

search = col1.text_input("🔍 Search Stock")

if search:
    df = df[df["Stock"].str.contains(search.upper())]

if col2.button("🔄 Refresh"):
    st.cache_data.clear()
    st.rerun()

# 📊 SUMMARY
c1, c2, c3 = st.columns(3)
c1.metric("Total Stocks", len(df))
c2.metric("Gainers", int((df["Change"] > 0).sum()))
c3.metric("Losers", int((df["Change"] < 0).sum()))

# 🎨 COLOR STYLE
def color(val):
    try:
        val = float(val)
        if val > 0:
            return "color: #00ff9f"
        elif val < 0:
            return "color: #ff4d4d"
    except:
        return ""

st.dataframe(
    df.style.map(color, subset=["Change", "%"]),
    height=500,
    use_container_width=True
)

# 📈 CHART
st.subheader("📈 Stock Chart")

selected = st.selectbox("Select Stock", df["Stock"])

if selected:
    chart = yf.download(selected + ".NS", period="1mo", interval="1d")
    st.line_chart(chart["Close"])

# 📥 EXPORT
if st.button("📥 Export to Excel"):
    df.to_excel("ltp_data.xlsx", index=False)
    st.success("Downloaded successfully!")