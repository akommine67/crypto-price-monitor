CREATE TABLE tickers_data (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    price NUMERIC,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from tickers_data;


CREATE MATERIALIZED VIEW ohlcv_view AS
SELECT
    ticker,
    DATE_TRUNC('day', timestamp) AS day,
    MIN(price) AS open_price,
    MAX(price) AS high_price,
    MIN(price) AS low_price,
    MAX(price) AS close_price
FROM tickers_data
GROUP BY ticker, DATE_TRUNC('day', timestamp);

select * from ohlcv_view

REFRESH MATERIALIZED VIEW ohlcv_view;

