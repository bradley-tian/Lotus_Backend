from flask import Flask, jsonify, render_template, request, redirect, url_for
from app import app, db
from app.models import Quotes
import json
import yfinance as yf
import pandas as pd
import ta

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"

@app.route('/')
def index():
    return render_template("index.html")

@app.before_first_request
def initialize_database():
    db.init_app(app=app)
    db.create_all(app=app)

"""Generates historical price data of the given stock."""
@app.route('/quote', methods = ['POST'])
def quote():
    if request.method == 'POST':
        data = request.get_data(as_text = True)
        ticker = (json.loads(data))["ticker"]
        try:
            yf.Ticker(ticker)
        except:
            print("Error: ticker not found.")
            print(ticker)
            return jsonify(success = False)
        
        # Need to change this hardcoded username later
        entry = Quotes({
            'username': 'admin',
            'ticker': ticker,
        })
        db.session.add(entry)
        db.session.commit()

    return jsonify(success = True)

"""Calculates MACD signal line values."""
@app.route('/macdModel', methods = ['GET','POST'])
def macdModel(): 

    # Need to change this hardcoded username later
    quote = yf.Ticker(Quotes.query.filter_by(username="admin").first().ticker)
    # Need to implement error checking for periods and intervals
    history = []
    data = json.loads(request.get_data(as_text = True))
    period = data["period"]
    if period:
        interval = data["interval"]
        history = quote.history(period = period, interval = interval, actions = False)
    else: 
        start_date = data['start_date']
        end_date = data['end_date']
        history = quote.history(start_date = start_date, end_date = end_date, actions = False)
    
    closings = history['Close']
    macd = ta.trend.MACD(
        close = closings,
        window_slow = int(data['slow']),
        window_fast = int(data['fast']),
        window_sign = int(data['signal']),
        fillna = True )

    line = macd.macd()
    hist = macd.macd_diff()
    signal = macd.macd_signal()
    triggers = {}

    last_date = None
    last_value = None
    for date, value in hist.items():
        if last_value:
            if value > 0 and last_value < 0:
                triggers[last_date] = [last_value, "buy"]
            elif value < 0 and last_value > 0:
                triggers[last_date] = [last_value, "sell"]
        last_date = date
        last_value = value
    
    response = {
        "macd_line": str(line.to_dict()),
        "macd_hist": str(hist.to_dict()),
        "macd_signal": str(signal.to_dict()),
        "triggers": str(triggers),
    }
    return response

# args: fast, slow, signal, interval, period = None, start_date = None, end_date = None

# Import python ta lib
# Get quote data from yahoo
# Transform input backtrack to date range
# pandas splice price history
# get macd values from ta lib using split series
# transform data into time, price tuple array
# return as dictionary
