"""
Daily Signal Checker — Paper Trading Helper
------------------------------------------------
Isse roz market band hone ke baad chalao (evening ko).
Ye batayega: kya aaj koi naya BUY ya SELL signal aaya hai
(20-din/50-din moving average crossover ke hisaab se).

Har baar signal aaye, note kar lo apni spreadsheet mein:
Date | Ticker | Signal | Price
Isse 3-6 mahine track karne ke baad, dekh sakte ho ki
strategy real conditions mein kaisi perform karti.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
from spreadsheet import *

# ----------------------------
# Apni watchlist yahan daalo
# ----------------------------
WATCHLIST = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ITC.NS" , 'MOTHERSON.NS'
]
SHORT_WINDOW = 20
LONG_WINDOW = 50
LOOKBACK_DAYS = 200   # itna purana data lo taaki 50-din average sahi se calculate ho


def check_signal(ticker):
    data = yf.download(ticker, period=f"{LOOKBACK_DAYS}d", progress=False)
    if data.empty or len(data) < LONG_WINDOW + 5:
        return None

    data = data[["Close"]].copy()
    data.columns = ["Close"]
    data["SMA_short"] = data["Close"].rolling(SHORT_WINDOW).mean()
    data["SMA_long"] = data["Close"].rolling(LONG_WINDOW).mean()

    # Aaj aur kal ki values compare karo — crossover hua ya nahi
    today = data.iloc[-1]
    yesterday = data.iloc[-2]

    today_above = today["SMA_short"] > today["SMA_long"]
    yesterday_above = yesterday["SMA_short"] > yesterday["SMA_long"]

    signal = None
    if today_above and not yesterday_above:
        signal = "BUY"
    elif not today_above and yesterday_above:
        signal = "SELL"

    return {
        "Ticker": ticker,
        "Date": data.index[-1].strftime("%Y-%m-%d"),
        "Close Price": round(today["Close"], 2),
        "SMA_20": round(today["SMA_short"], 2),
        "SMA_50": round(today["SMA_long"], 2),
        "Currently In Position?": "YES (SMA20 > SMA50)" if today_above else "NO",
        "New Signal Today": signal if signal else "-- no change --",
    }


print(f"Signal Check — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 70)

results = []
for ticker in WATCHLIST:
    r = check_signal(ticker)
    if r:
        make_data(r)
        results.append(r)
        marker = ""
        if r["New Signal Today"] == "BUY":
            marker = "  🟢 NEW BUY SIGNAL — spreadsheet mein note karo!"
        elif r["New Signal Today"] == "SELL":
            marker = "  🔴 NEW SELL SIGNAL — spreadsheet mein note karo!"
        print(f"\n{r['Ticker']}{marker}")
        print(f"  Close: ₹{r['Close Price']}  |  SMA20: ₹{r['SMA_20']}  |  SMA50: ₹{r['SMA_50']}")
        print(f"  Position status: {r['Currently In Position?']}")

print("\n" + "=" * 70)
new_signals = [r for r in results if r["New Signal Today"] != "-- no change --"]
if new_signals:
    print(f"\n{len(new_signals)} naya signal mila aaj! Upar 🟢/🔴 wale dekho.")
else:
    print("\nAaj koi naya signal nahi aaya kisi bhi stock mein.")

print("\nReminder: Ye sirf paper trading / learning ke liye hai.")
print("Har signal ko apni spreadsheet mein Date, Ticker, Price ke saath note karo.")
print('dataset function is called' , make_csv(data))