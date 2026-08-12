
from fundamentals import results
from spreadsheet import make_csv
import csv
import os
# pyrefly: ignore [missing-import]
from flask import Flask, render_template
from trading import *
from spreadsheet import * 
app = Flask(__name__)

# Use absolute path or fallback to script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'trading_data.csv')

@app.route('/')
def home():
    current = []
    make_csv(finals)
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            current = list(reader)
    
    # Fallback: compute last 30 days of historical signals live if CSV is missing/empty
    if not current:
        current = get_historical_signals(WATCHLIST, days=30)

    return render_template('index.html', data=current)


if __name__ == '__main__':
    app.run(debug=True, port=5000)


