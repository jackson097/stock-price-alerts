#!/usr/bin/env python3
import csv
import yfinance as yf
import json
import os
import subprocess
from datetime import datetime

def load_watchlist():
    watchlist = {}
    with open("watchlist.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row or not row[0]:
                continue
            ticker = row[0]
            targets = []
            for target_str in row[1:]:
                target_str = target_str.strip()
                if not target_str:
                    continue
                
                # + suffix means to add a special message indicating we aren't ready to buy just yet
                watch_weekly = target_str.endswith('+')
                if watch_weekly:
                    target_str = target_str[:-1]  # Remove the +
                
                if target_str.startswith('>'):
                    price = float(target_str[1:])
                    targets.append(('above', price, watch_weekly))
                elif target_str.startswith('<'):
                    price = float(target_str[1:])
                    targets.append(('below', price, watch_weekly))
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
            for alert_type, target_price, watch_weekly in targets:
                alert_message = ""
                alert_id = f"{ticker}_{alert_type}_{target_price}"
                
                if alert_type == 'above' and price > target_price:
                    alert_message = f"{ticker} is above ${target_price:.2f} (current: ${price:.2f})"
                elif alert_type == 'below' and price < target_price:
                    alert_message = f"{ticker} is below ${target_price:.2f} (current: ${price:.2f})"
                
                if alert_message:
                    if watch_weekly:
                        alert_message += " - Watch how price closes the week before buying"
                    
                    alerts.append({
                        'id': alert_id,
                        'message': alert_message,
                        'ticker': ticker,
                        'price': price,
                        'target': target_price,
                        'timestamp': datetime.now().isoformat()
                    })
    return alerts

def load_previous_alerts():
    if os.path.exists("previous_alerts.json"):
        with open("previous_alerts.json", 'r') as f:
            return json.load(f)
    return {}

def save_alerts(alerts):
    alert_dict = {alert['id']: alert for alert in alerts}
    with open("previous_alerts.json", 'w') as f:
        json.dump(alert_dict, f, indent=2)

def send_notification(message):
    """Send visual notification using AppleScript dialog"""
    print(f"New price alert: {message}")
    
    try:
        escaped_message = message.replace('"', '\\"').replace("'", "\\'")
        subprocess.run([
            'osascript', '-e', 
            f'display dialog "New price alert\\n\\n{escaped_message}" with title "Stock Alert" buttons {{"OK"}} default button "OK" giving up after 10'
        ], timeout=15)
    except Exception as e:
        print(f"Notification failed: {e}")
        # Fallback: try regular notification
        try:
            subprocess.run([
                'osascript', '-e', 
                f'display notification "{escaped_message}" with title "Stock Alert"'
            ], timeout=5)
        except:
            print("All notification methods failed")



def main():
    try:
        watchlist = load_watchlist()
        current_alerts = check_prices(watchlist)
        previous_alerts = load_previous_alerts()
        
        new_alerts = [alert for alert in current_alerts if alert['id'] not in previous_alerts]
        
        for alert in new_alerts:
            print(f"New price alert: {alert['message']}")
            send_notification(alert['message'])
        
        save_alerts(current_alerts)
        
        if not new_alerts and current_alerts:
            print(f"Monitoring {len(current_alerts)} active alerts...")
        elif not current_alerts:
            print("No active alerts.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
