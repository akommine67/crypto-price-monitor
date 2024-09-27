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

## Architecture Diagram
![Untitled Diagram drawio](https://github.com/user-attachments/assets/1157de4e-9890-4cb2-8df4-a07b3e8273bf)


## Monitoring
The system implements real-time monitoring of cryptocurrency prices (BTC, ETH, ZEC) and triggers an alert when price changes exceed 2% over a 5-minute moving average. Alerts are logged to a .txt file using a push-based mechanism for immediate action.

**Alert System**:
Logs alerts directly to a file and can be extended to support more sophisticated messaging services such as Kafka, RabbitMQ, or AWS SNS.
Modularized to allow adding more thresholds (e.g., volume changes) or other asset classes with minimal code changes.
 

**Push-Based Monitoring**:
The system operates without querying historical data from the database. Alerts are raised in real time, ensuring minimum latency by processing data as it is ingested.

**Scalability**:
With a modular design, the system can handle additional tickers, metrics, or larger data streams by integrating message queues (e.g., Kafka) to decouple data ingestion and alert generation, providing resilience and horizontal scalability.
As the data volume grows, the system can evolve to store historical alerts in a more distributed storage system (e.g., Amazon S3 or Hadoop) to preserve file I/O efficiency.

### Extending the System:
**Additional Metrics**: Can easily be extended to monitor more metrics (e.g., volume, volatility) by adding new monitoring functions for these metrics.

**Distributed Alerting**: Integrating with cloud-based message brokers like Kafka, RabbitMQ, or AWS SNS will allow real-time alerts to be broadcast to multiple consumers, improving responsiveness and flexibility in how alerts are handled.

**Advanced Analytics**: Historical data stored in PostgreSQL (or a data warehouse like Redshift) could be used to feed machine learning models for predictive analytics and forecasting.

**Error Handling and Resilience**: Introducing retries and fallbacks when API limits are reached or network failures occur can make the system more resilient.


## Scalability

Handling large datasets is critical in this application, especially when each new asset adds millions of records per month. Here's how scalability and retrieval speed can be addressed:

**Addressing Scalability Without Losing Information**:
**Table Partitioning**: Partition the PostgreSQL table by time (daily, monthly) or asset. This will help distribute data across smaller tables, allowing efficient querying and reducing table size. Old partitions can be archived without affecting the real-time performance.

**Data Archival**: Move older data to a long-term storage solution, like AWS S3 or Hadoop HDFS. This maintains historical data without affecting the performance of the main database.

**Compression**: Use PostgreSQL's native compression techniques like pg_dump or columnar storage solutions (like Apache Parquet) to reduce storage size while maintaining fast retrieval. This can also be combined with storage engines like TimescaleDB, which offers better compression for time-series data.

**Streaming Architecture**: For extreme scalability, integrate real-time data streaming platforms like Apache Kafka or AWS Kinesis to decouple ingestion from storage, allowing parallel processing and elastic scalability.

### Optimizing Retrieval Speed:

**Indexing**: Create composite indexes on frequently queried fields, such as timestamp, ticker, and price. Ensure optimal index usage by analyzing query patterns.

**Materialized Views for Aggregation**: Materialized views can precompute common queries (like OHLCV data). Refresh views periodically or incrementally to speed up retrieval.

**Caching**: Implement in-memory caching solutions like Redis for frequently accessed or computed data, reducing load on the database and speeding up response times for real-time dashboards and alerts.

**Sharding**: If necessary, shard the database horizontally across multiple nodes. This distributes the load and reduces the size of individual databases, ensuring faster retrieval even as the dataset grows.

**Data Lakes for Analytics**: Offload historical analytics to a data lake (like AWS S3 + AWS Athena ) for distributed querying of large historical datasets, while maintaining recent or real-time data in PostgreSQL for fast access.

## Conclusion:
Combining table partitioning, compression, sharding, and optimized indexing ensures scalability without data loss, while caching and materialized views improve retrieval speed. Long-term, transitioning to streaming and distributed storage architectures will allow the system to handle massive growth and high-speed data retrieval efficiently.


## How to Run the Application

Prerequisites:
1. python 3.x installed
2.PostgreSQL installed and running
3. Install required Python pacakages
   
**Steps**
1. Clone the Repository
   
    `git clone https://github.com/akommine67/crypto-price-monitor`
   
    `cd crypto-price-monitor`

3. Set Up PostgreSQL:
    create a database named `luxor_db`
   
    create the required table which is in the luxor_db.sql file.
   
5. Run the Python Script:
   `python data_fetcher.py`
   
7. Check Alerts:
    Alerts will be logged in `alerts.txt` when price changes exceed 2% over a 5-minute period.
   
Running Tests:
  `python test_script.py`

**The below shows all the three test cases were passed**

![
](https://github.com/akommine67/crypto-price-monitor/blob/main/WhatsApp%20Image%202024-09-27%20at%203.27.29%20AM.jpeg)
