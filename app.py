import csv
import os
from flask import Flask, render_template

app = Flask(__name__)

# Use absolute path or fallback to script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'trading_data.csv')

@app.route('/')
def home():
    data = []
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)

    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)