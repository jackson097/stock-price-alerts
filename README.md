# Stock Price Alerts

Automated stock price monitoring system that sends desktop notifications when stocks cross your specified thresholds.

## Features

- ✅ **Real-time monitoring** - Checks stock prices every minute
- ✅ **Visual notifications** - Desktop dialog alerts for new price movements
- ✅ **Smart alerts** - Only notifies on NEW threshold crossings (no spam)
- ✅ **Weekly reminders** - Optional "watch weekly close" messages
- ✅ **Automatic operation** - Runs in background, survives reboots
- ✅ **Clean interface** - Minimal setup, easy to manage

## Setup Instructions

### 1. Install Dependencies
```bash
pip install yfinance
```

### 2. Create Your Watchlist
- Create `watchlist.csv` and fill it out using same format as `example-watchlist.csv`
- Format: `TICKER,>price+,<price`
  - `>340.00` = Alert when price goes above $340
  - `<320.00` = Alert when price goes below $320  
  - `+` suffix = Add "Watch how price closes the week before buying" message

### 3. Install Automation
```bash
# Copy automation config to system
cp com.stockalerts.monitor.plist ~/Library/LaunchAgents/

# Start the automation (runs every minute)
launchctl load ~/Library/LaunchAgents/com.stockalerts.monitor.plist
```

### 4. Test the System
```bash
# Test manually to see if notifications work
python3 stock-alerts-automated.py
```

## Watchlist Format Examples

```csv
CELH,>71.03+,<56.25
MARA,>19.23+,<17.00  
TSLA,<410.00,>444.00+
AAPL,>150.00,<140.00+
```

**Format Rules:**
- `TICKER` = Stock symbol
- `>price` = Alert when stock goes ABOVE this price
- `<price` = Alert when stock goes BELOW this price  
- `+` = Add weekly close reminder to the alert message
- Multiple alerts per stock are supported

## Management Commands

```bash
# Stop automation
launchctl unload ~/Library/LaunchAgents/com.stockalerts.monitor.plist

# Start automation  
launchctl load ~/Library/LaunchAgents/com.stockalerts.monitor.plist

# Check if running
launchctl list | grep stockalerts

# View logs
tail -f logs/stock-alerts.log

# Test manually
python3 stock-alerts-automated.py
```

## How It Works

1. **Every minute**, the script checks current stock prices using Yahoo Finance
2. **Compares prices** against your watchlist thresholds
3. **New alerts only** - Tracks previous alerts to avoid spam
4. **Desktop notifications** - Shows dialog box with alert details
5. **Auto-dismiss** - Dialogs close after 10 seconds if not clicked

## Files

- `stock-alerts-automated.py` - Main automation script
- `watchlist.csv` - Your stock alerts (edit this file)  
- `example-watchlist.csv` - Example format reference
- `previous_alerts.json` - Tracks sent alerts (auto-generated)
- `logs/` - Log files directory

## Troubleshooting

**No notifications appearing?**
- Check System Settings → Notifications → Terminal/VS Code
- Enable notification permissions

**Automation not running?**
- Check: `launchctl list | grep stockalerts`
- Reload: `launchctl unload ~/Library/LaunchAgents/com.stockalerts.monitor.plist && launchctl load ~/Library/LaunchAgents/com.stockalerts.monitor.plist`

**Stock data issues?**
- Verify ticker symbols are correct
- Check internet connection
- Yahoo Finance API may have temporary issues
