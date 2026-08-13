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


def get_historical_signals(watchlist=WATCHLIST, days=30):
    all_rows = []
    for ticker in watchlist:
        try:
            df = yf.download(ticker, period=f"{LOOKBACK_DAYS}d", progress=False)
            if df.empty or len(df) < LONG_WINDOW + 5:
                continue
            df = df[["Close"]].copy()
            df.columns = ["Close"]
            df["SMA_short"] = df["Close"].rolling(SHORT_WINDOW).mean()
            df["SMA_long"] = df["Close"].rolling(LONG_WINDOW).mean()
            
            recent_df = df.iloc[-days:]
            for idx in range(len(recent_df)):
                row_idx = len(df) - days + idx
                if row_idx < 1:
                    continue
                curr = df.iloc[row_idx]
                prev = df.iloc[row_idx - 1]
                
                curr_above = curr["SMA_short"] > curr["SMA_long"]
                prev_above = prev["SMA_short"] > prev["SMA_long"]
                
                sig = None
                if curr_above and not prev_above:
                    sig = "BUY"
                elif not curr_above and prev_above:
                    sig = "SELL"
                
                # Handle pandas Series float conversion
                c_val = curr["Close"].item() if hasattr(curr["Close"], 'item') else float(curr["Close"])
                s20 = curr["SMA_short"].item() if hasattr(curr["SMA_short"], 'item') else float(curr["SMA_short"])
                s50 = curr["SMA_long"].item() if hasattr(curr["SMA_long"], 'item') else float(curr["SMA_long"])

                all_rows.append({
                    "Ticker": ticker,
                    "Date": df.index[row_idx].strftime("%Y-%m-%d"),
                    "Close Price": round(c_val, 2),
                    "SMA_20": round(s20, 2),
                    "SMA_50": round(s50, 2),
                    "Currently In Position?": "YES (SMA20 > SMA50)" if curr_above else "NO",
                    "New Signal Today": sig if sig else "-- no change --",
                })
        except Exception as e:
            print(f"Error fetching history for {ticker}: {e}")
    
    # Sort history by Date descending
    all_rows.sort(key=lambda x: x["Date"], reverse=True)
    return all_rows




def run_trading():
    print(f"\nSignal Check - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    finals = []
    for ticker in WATCHLIST:
        r = check_signal(ticker)
        if r:
            finals.append(r)
            marker = ""
            if r["New Signal Today"] == "BUY":
                marker = "  [BUY] NEW BUY SIGNAL - spreadsheet mein note karo!"
            elif r["New Signal Today"] == "SELL":
                marker = "  [SELL] NEW SELL SIGNAL - spreadsheet mein note karo!"
            print(f"\n{r['Ticker']}{marker}")
            print(f"  Close: Rs.{r['Close Price']}  |  SMA20: Rs.{r['SMA_20']}  |  SMA50: Rs.{r['SMA_50']}")
            print(f"  Position status: {r['Currently In Position?']}")

    print("\n" + "=" * 70)
    new_signals = [r for r in finals if r["New Signal Today"] != "-- no change --"]
    if new_signals:
        print(f"\n{len(new_signals)} naya signal mila aaj! Upar BUY/SELL wale dekho.")
    else:
        print("\nAaj koi naya signal nahi aaya kisi bhi stock mein.")

    print("\nReminder: Ye sirf paper trading / learning ke liye hai.")
    print("Har signal ko apni spreadsheet mein Date, Ticker, Price ke saath note karo.")
    csv_res = make_csv(finals)
    print('dataset function is called:', csv_res)
    return finals


if __name__ == '__main__':
    run_trading()

