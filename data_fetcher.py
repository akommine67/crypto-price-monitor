import requests
import time
import psycopg2
from datetime import datetime
from collections import deque

def fetch_data():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,zcash&vs_currencies=usd'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        print("Rate limit exceeded. Waiting for 1 minute.")
        time.sleep(60)  # Wait 1 minute before retrying
        return None
    else:
        print(f"Error: {response.status_code}")
        return None

def store_data(data):
    if not data:
        return  # Skip if no data

    conn = psycopg2.connect(database="luxor_db", user="postgres", password="123456", host="localhost", port="5433")
    cursor = conn.cursor()

    for ticker, values in data.items():
        try:
            cursor.execute("""
                INSERT INTO tickers_data (ticker, price, timestamp) VALUES (%s, %s, %s)
            """, (ticker, values['usd'], datetime.now()))
        except KeyError:
            print(f"KeyError: 'usd' not found for {ticker}")
    
    conn.commit()
    cursor.close()
    conn.close()



# A dictionary to store price history for each ticker
price_history = {
    'bitcoin': deque(maxlen=300),  # Store the last 300 seconds (5 minutes)
    'ethereum': deque(maxlen=300),
    'zcash': deque(maxlen=300)
}

# Function to calculate the moving average
def moving_average(prices):
    return sum(prices) / len(prices) if prices else 0

# Function to check if the price exceeds the threshold
def check_price_change(ticker, current_price):
    if ticker in price_history:
        prices = price_history[ticker]
        avg_price = moving_average(prices)
        if avg_price > 0:
            change = abs(current_price - avg_price) / avg_price
            if change > 0.02:  # 2% threshold
                alert_message = f"Alert: {ticker} price changed by more than 2% from the 5-min average."
                print(alert_message)
                with open("alerts.txt", "a") as log_file:
                    log_file.write(f"{time.ctime()} - {alert_message}\n")
        prices.append(current_price)



while True:
    data = fetch_data()
    if data:
        for ticker, values in data.items():
            current_price = values['usd']
            check_price_change(ticker, current_price)
    store_data(data)
    time.sleep(10)  # Adjust the delay (e.g., 10 seconds)
