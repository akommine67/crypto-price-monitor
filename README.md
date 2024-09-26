# Crypto-price-monitor

## Architecture Overview:
This section will describe each stage of the architecture and tools used.

### Source:
CoinGecko API: Fetches real-time cryptocurrency data for BTC, ETH, and ZEC.
Security: Ensure API keys are securely stored and handle rate limits.

### Ingestion:
Python Script: Retrieves data using requests and stores it in PostgreSQL.
Testing: Use unit tests to simulate API responses and validate data ingestion.

### Transformation:
Price Monitoring: Monitors price changes (>2% threshold) and triggers alerts.
Testing: Unit tests for monitoring and alert logic.
Security: Ensure integrity of data during processing and proper error handling.

### Storage:
PostgreSQL: Stores raw ticker data and uses a materialized view for historical OHLCV data.
Testing: Validate data insertions and aggregation queries.
Security: Use encryption for database connections and set appropriate access controls.

### Output:

Alert System: Logs alerts to a file when price changes exceed the threshold.
Testing: Mock the logging system to ensure alerts are properly generated.
![image](https://github.com/user-attachments/assets/9b95be29-8185-4a7d-b55d-830165c707b2)
