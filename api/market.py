import json
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
    return {
        "label": label,
        "price": round(float(curr["Close"]), 2),
        "open": round(float(curr["Open"]), 2),
        "high": round(float(prev["High"]), 2),
        "low": round(float(prev["Low"]), 2),
        "close": round(float(prev["Close"]), 2)
    }

def calc_pivots(high, low, close):
    pp = (high + low + close) / 3
    return {
        "pp": round(pp, 2),
        "r1": round((2 * pp) - low, 2),
        "r2": round(pp + (high - low), 2),
        "s1": round((2 * pp) - high, 2),
        "s2": round(pp - (high - low), 2)
    }

def handler(event, context):
    try:
        daily   = get_tf_data(SYMBOL, "2d",  "1d",  "Daily")
        weekly  = get_tf_data(SYMBOL, "2wk", "1wk", "Weekly")
        monthly = get_tf_data(SYMBOL, "2mo", "1mo", "Monthly")
        yearly  = get_tf_data(SYMBOL, "2y",  "1mo", "Yearly")

        vix_hist    = yf.Ticker(VIX_SYMBOL).history(period="5d", interval="1d")
        vix_current = round(float(vix_hist["Close"].iloc[-1]), 2)

        gap     = daily["open"] - daily["close"]
        gap_pct = round((gap / daily["close"]) * 100, 2)

        data = {
            "daily":          daily,
            "weekly":         weekly,
            "monthly":        monthly,
            "yearly":         yearly,
            "daily_pivots":   calc_pivots(daily["high"],   daily["low"],   daily["close"]),
            "weekly_pivots":  calc_pivots(weekly["high"],  weekly["low"],  weekly["close"]),
            "monthly_pivots": calc_pivots(monthly["high"], monthly["low"], monthly["close"]),
            "vix":            vix_current,
            "gap":            round(gap, 2),
            "gap_pct":        gap_pct,
            "bias":           "Flat" if abs(gap_pct) < 0.3 else ("UP" if gap_pct > 0 else "DOWN"),
            "vix_status":     "HIGH" if vix_current > 20 else ("LOW" if vix_current < 14 else "NORMAL")
        }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps(data)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }