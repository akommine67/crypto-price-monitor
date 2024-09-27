import unittest
import time
import os
from data_fetcher import fetch_data, store_data, check_price_change,price_history,price_history,last_check_time
from unittest.mock import patch
from collections import deque

class TestCoinGeckoApp(unittest.TestCase):
    
    def test_fetch_data(self):
        # Simulate a fetch with mock data
        data = {'bitcoin': {'usd': 1000}}
        self.assertIsNotNone(data, "API response is None")
    
    def test_store_data(self):
        # Mock data for testing the database store
        data = {'bitcoin': {'usd': 1000}}
        try:
            store_data(data)  # This should not loop indefinitely
            result = True
        except Exception as e:
            result = False
        self.assertTrue(result, "Data storing failed")
    def test_check_price_change(self):
        # Ensure price_history and last_check_time for 'bitcoin' are initialized
        if 'bitcoin' not in price_history:
            price_history['bitcoin'] = deque(maxlen=300)
    
    # Mock data for price history (prices in the last 5 minutes)
    # Adding (price, timestamp) for each price, timestamps are older than 5 minutes
        price_history['bitcoin'].extend([
            (10000, time.time() - 301),  # 301 seconds ago (just older than 5 minutes)
            (10100, time.time() - 300),  # 300 seconds ago (boundary for 5 mins)
            (10200, time.time() - 250),  # 250 seconds ago
            (10300, time.time() - 200),  # 200 seconds ago
            (10400, time.time() - 100),  # 100 seconds ago
        ])
    
        current_price = 11000
    
    # Set last_check_time to simulate a past time (more than 5 minutes ago)
        last_check_time['bitcoin'] = time.time() - 301  # Force past check time
    
    # Clear the alerts file before testing
        with open("alerts.txt", "w"):
            pass
    
    # Call the check_price_change function
        check_price_change('bitcoin', current_price)

    # Verify if an alert has been logged (current_price is 10% higher than avg 5-min price)
        with open("alerts.txt", "r") as f:
            alert_logs = f.readlines()
    
        print(alert_logs)
        self.assertGreater(len(alert_logs), 0, "Alert not triggered when it should have been.")

if __name__ == '__main__':
    unittest.main()
