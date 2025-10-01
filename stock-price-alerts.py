import csv
import yfinance as yf

def load_watchlist(filename="watchlist.csv"):
    watchlist = {}
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            ticker = row[0]
            targets = []
            for target_str in row[1:]:
                target_str = target_str.strip()
                if target_str.startswith('>'):
                    # Above threshold
                    price = float(target_str[1:])
                    targets.append(('above', price))
                elif target_str.startswith('<'):
                    # Below threshold
                    price = float(target_str[1:])
                    targets.append(('below', price))
                else:
                    raise ValueError(f"Invalid target format '{target_str}' for {ticker}. Use >price for above alerts or <price for below alerts.")
            watchlist[ticker] = targets
    return watchlist

def check_prices(watchlist):
    alerts = []
    for ticker, targets in watchlist.items():
        stock = yf.Ticker(ticker)
        try:
            price = stock.fast_info["last_price"]
        except:
            price = None
        
        if price:
            for alert_type, target_price in targets:
                if alert_type == 'above' and price > target_price:
                    alerts.append(f"{ticker} is above ${target_price:.2f} (current: ${price:.2f})")
                elif alert_type == 'below' and price < target_price:
                    alerts.append(f"{ticker} is below ${target_price:.2f} (current: ${price:.2f})")

    return alerts

if __name__ == "__main__":
    watchlist = load_watchlist("watchlist.csv")
    alerts = check_prices(watchlist)
    if alerts:
        print("Alerts:")
        for alert in alerts:
            print(" -", alert)
    else:
        print("No alerts right now.")
