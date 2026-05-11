import os
import yfinance as yf
from flask import Response, jsonify

SYMBOL = 'SPY'
VIX_SYMBOL = '^VIX'

def get_tf_data(symbol, period, interval, label):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period, interval=interval)
    if len(hist) < 2:
        return None
    curr = hist.iloc[-1]
    prev = hist.iloc[-2]
    return {'label': label, 'price': curr['Close'], 'open': curr['Open'], 'high': prev['High'], 'low': prev['Low'], 'close': prev['Close']}

def calc_pivots(high, low, close):
    pp = (high + low + close) / 3
    return {'pp': pp, 'r1': (2 * pp) - low, 'r2': pp + (high - low), 's1': (2 * pp) - high, 's2': pp - (high - low)}

def handler(request):
    path = request.path
    
    if path == '/' or path == '' or path == '/morning-brief.html':
        try:
            with open('templates/morning-brief.html', 'r') as f:
                html = f.read()
            return Response(html, mimetype='text/html')
        except Exception as e:
            return Response('Error: ' + str(e), mimetype='text/html', status=500)
    
    elif path == '/api/market':
        try:
            daily = get_tf_data(SYMBOL, '2d', '1d', 'Daily')
            weekly = get_tf_data(SYMBOL, '2wk', '1wk', 'Weekly')
            monthly = get_tf_data(SYMBOL, '2mo', '1mo', 'Monthly')
            yearly = get_tf_data(SYMBOL, '2y', '1mo', 'Yearly')
            vix = yf.Ticker(VIX_SYMBOL).history(period='5d', interval='1d')
            vix_current = vix['Close'].iloc[-1]
            gap = daily['open'] - daily['close']
            gap_pct = (gap / daily['close']) * 100
            data = {'daily': daily, 'weekly': weekly, 'monthly': monthly, 'yearly': yearly, 'daily_pivots': calc_pivots(daily['high'], daily['low'], daily['close']), 'weekly_pivots': calc_pivots(weekly['high'], weekly['low'], weekly['close']), 'monthly_pivots': calc_pivots(monthly['high'], monthly['low'], monthly['close']), 'vix': vix_current, 'gap': gap, 'gap_pct': gap_pct, 'bias': 'Flat' if abs(gap_pct) < 0.3 else ('UP' if gap_pct > 0 else 'DOWN'), 'vix_status': 'HIGH' if vix_current > 20 else 'LOW' if vix_current < 14 else 'NORMAL'}
            return Response(json.dumps(data), mimetype='application/json')
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), mimetype='application/json', status=500)
    
    elif path == '/api/weather':
        return Response(json.dumps({'temp': 79, 'feels_like': 76, 'humidity': 16, 'wind': '10 mph W', 'uv': '8 - High', 'desc': 'Sunny', 'icon': 'sunny'}), mimetype='application/json')
    
    elif path == '/api/calendar':
        return Response(json.dumps([{'time': '10:00 ET', 'summary': 'Calendar API not connected', 'location': ''}]), mimetype='application/json')
    
    elif path == '/api/news':
        return Response(json.dumps([{'time': '08:30 ET', 'event': 'Initial Jobless Claims', 'impact': 'HIGH'}]), mimetype='application/json')
    
    else:
        return Response('Not Found', mimetype='text/plain', status=404)

app = handler
