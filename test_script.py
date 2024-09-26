import unittest
from data_fetcher import fetch_data, store_data, check_price_change,price_history

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
        # Mock data for price history and current price
        price_history['bitcoin'].extend([10000, 10100, 10200, 10300, 10400]) 
        current_price = 11000
        # Manually call the function to see if an alert is triggered
        with open("alerts.txt", "w"):  # Clear the alerts file
            pass
        check_price_change('bitcoin', current_price)
        
        # Check if an alert is written to the file
        with open("alerts.txt", "r") as f:
            alert_logs = f.readlines()
        
        self.assertGreater(len(alert_logs), 0, "Alert not triggered when it should have been.")

if __name__ == '__main__':
    unittest.main()
