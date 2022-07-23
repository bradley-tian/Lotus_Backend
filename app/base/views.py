from flask import jsonify, render_template, request
from app import db
from app.base import blueprint
from app.base.models import Quotes
from app.base.algorithms import calculate_returns
import json
import yfinance as yf
import pandas as pd
import ta
import numpy as np
import pandas as pd

"""Displays the landing/documentation page."""
@blueprint.route('/', methods = ['GET', 'POST'])
def index():
    return render_template("index.html")

"""Generates historical price data of the given stock."""
@blueprint.route('/api/quote', methods = ['GET','POST'])
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
        entry = Quotes.query.filter_by(username = 'admin').first() 
        if not entry:
            entry = Quotes({
                'username': 'admin',
                'ticker': ticker,
            })
            db.session.add(entry)
        else:
            entry.ticker = ticker
        db.session.commit()
    
    resp = get_history(json.loads(data))
    resp["UnixIdx"] = resp.index.astype(np.int64)
    resp.reset_index()
    resp = resp.set_index(resp["UnixIdx"])

    return jsonify(resp.to_dict())

# Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
# Valid intervals: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
time_hierarchy = {
    "1m":1,
    "2m":2,
    "5m":3,
    "15m":4,
    "30m":5,
    "60m":6,
    "90m":7,
    "1h":8,
    "1d":9,
    "5d":10,
    "1wk":11,
    "1mo":12,
    "3mo":13,
    "6mo":14,
    "1y":15,
    "ytd":16,
    "2y":17,
    "5y":18,
    "10y":19,
    "max":20,
}

"""Generates MACD two-line, historgram, and signal line values, calculating buy and sell points using crossovers."""
@blueprint.route('/api/macdModel', methods = ['GET','POST'])
def macdModel(): 
    data = json.loads(request.get_data(as_text = True))
    history = get_history(data)
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

    # Change timestamps to epoch times
    last_date = None
    last_value = None
    for date, value in hist.items():
        if last_value:
            if value > 0 and last_value < 0:
                triggers[last_date] = [closings[last_date], "buy"]
            elif value < 0 and last_value > 0:
                triggers[last_date] = [closings[last_date], "sell"]
        last_date = date
        last_value = value
    
    net_returns = calculate_returns(
        triggers = triggers,
        shares = int(data['shares']),
        starting_price = int(data['starting_price']),
        cash = int(data['cash']),
        )
    
    formatted_trig = {}
    for key in triggers:
        if type(key) != float:
            formatted_trig[int(key.timestamp())] = triggers[key]

    response = {
        "macd_line": str(line.to_dict()),
        "macd_hist": str(hist.to_dict()),
        "macd_signal": str(signal.to_dict()),
        "triggers": formatted_trig,
        "returns": str(net_returns),
    }
    
    return response

@blueprint.route('/api/rsiModel', methods = ['GET', 'POST'])
def rsiModel():
    data = json.loads(request.get_data(as_text = True))
    history = get_history(data)
    closings = history['Close']
    rsi = ta.momentum.RSIIndicator(
        close = closings,
        window = int(data['window']),
        fillna = True
    ).rsi()

    triggers = {}
    last_value = None

    # Change timestamps to epoch times
    for date, value in rsi.items():
        if last_value:
            # Make customizable
            if last_value < 30 and value > 30:
                triggers[date] = [closings[date], 'buy']
            elif last_value < 70 and value > 70:
                triggers[date] = [closings[date], 'sell']
        last_value = value

    net_returns = calculate_returns(
        triggers = triggers,
        shares = int(data['shares']),
        starting_price = int(data['starting_price']),
        cash = int(data['cash']),
    )

    formatted_trig = {}
    for key in triggers:
        if type(key) != float:
            formatted_trig[int(key.timestamp())] = triggers[key]

    response = {
        "rsi": str(rsi.to_dict()),
        "triggers": formatted_trig,
        "returns": str(net_returns),
    }
    
    return response

def get_history(data):
    # Need to change this hardcoded username later
    quote = yf.Ticker(Quotes.query.filter_by(username="admin").first().ticker)
    history = []
    period = data["period"]

    if period:
        interval = data["interval"]
        if not time_hierarchy[period] or not time_hierarchy[interval]:
            print("Error: invalid period or interval parameters (out of bounds).")
            return jsonify(success = False)
        elif time_hierarchy[period] < time_hierarchy[interval]:
            print("Error: interval is set larger than total period.")
            return jsonify(success = False)
        elif time_hierarchy[period] == 11:
            print("Error: invalid period parameter.")
            return jsonify(success = False)
        elif time_hierarchy[interval] > 13:
            print("Error: invalid interval paramter.")
            return jsonify(success = False)
        history = quote.history(period = period, interval = interval, actions = False)

    else: 
        start_date = data['start_date']
        end_date = data['end_date']
        try:
            history = quote.history(start_date = start_date, end_date = end_date, actions = False)
        except:
            print("Error: invalid start date or end date format.")
    
    return history