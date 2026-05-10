import json
from flask import Response
import yfinance as yf

SYMBOL = "SPY"
VIX_SYMBOL = "^VIX"

def get_tf_data(symbol, period, interval, label):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period, interval=interval)
    if len(hist) < 2:
        return None
    curr = hist.iloc[-1]
    prev = hist.iloc[-2]
    return {"label": label, "price": curr["Close"], "open": curr["Open"], "high": prev["High"], "low": prev["Low"], "close": prev["Close"]}

def calc_pivots(high, low, close):
    pp = (high + low + close) / 3
    return {"pp": pp, "r1": (2 * pp) - low, "r2": pp + (high - low), "s1": (2 * pp) - high, "s2": pp - (high - low)}

def handler(request):
    try:
        daily = get_tf_data(SYMBOL, "2d", "1d", "Daily")
        weekly = get_tf_data(SYMBOL, "2wk", "1wk", "Weekly")
        monthly = get_tf_data(SYMBOL, "2mo", "1mo", "Monthly")
        yearly = get_tf_data(SYMBOL, "2y", "1mo", "Yearly")
        vix = yf.Ticker(VIX_SYMBOL).history(period="5d", interval="1d")
        vix_current = vix["Close"].iloc[-1]
        gap = daily["open"] - daily["close"]
        gap_pct = (gap / daily["close"]) * 100
        data = {"daily": daily, "weekly": weekly, "monthly": monthly, "yearly": yearly, "daily_pivots": calc_pivots(daily["high"], daily["low"], daily["close"]), "weekly_pivots": calc_pivots(weekly["high"], weekly["low"], weekly["close"]), "monthly_pivots": calc_pivots(monthly["high"], monthly["low"], monthly["close"]), "vix": vix_current, "gap": gap, "gap_pct": gap_pct, "bias": "Flat" if abs(gap_pct) < 0.3 else ("UP" if gap_pct > 0 else "DOWN"), "vix_status": "HIGH" if vix_current > 20 else "LOW" if vix_current < 14 else "NORMAL"}
    except Exception as e:
        data = {"error": str(e)}
    return Response(json.dumps(data), mimetype="application/json")