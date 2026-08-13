import csv
import os
from flask import Flask, render_template
from trading import run_trading

app = Flask(__name__)

# Use absolute path or fallback to script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'trading_data.csv')

@app.route('/')
def home():
    # Execute trading logic automatically to fetch fresh signals and update CSV
    run_trading()

    current = []
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            current = list(reader)

    return render_template('index.html', data=current)


if __name__ == '__main__':
    app.run(debug=True, port=5000)



