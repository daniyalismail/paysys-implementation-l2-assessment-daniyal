-- 1. Transaction count and total value by status and day.
SELECT 
    DATE(created_at) AS transaction_date, 
    status, 
    COUNT(*) AS total_count, 
    SUM(amount) AS total_value
FROM transactions
GROUP BY DATE(created_at), status
ORDER BY transaction_date, status;

-- 2. Top 10 customers by successful transaction value.
SELECT 
    c.id,
    c.name,
    SUM(t.amount) AS total_success_value
FROM customers c
JOIN transactions t ON c.id = t.customer_id
WHERE t.status = 'SUCCESS'
GROUP BY c.id, c.name
ORDER BY total_success_value DESC
LIMIT 10;

-- 3. Transactions that have remained in PROCESSING for more than 15 minutes.
SELECT *
FROM transactions
WHERE status = 'PROCESSING' 
  AND created_at < NOW() - INTERVAL '15 minutes';

-- 4. Duplicate transaction references.
SELECT 
    transaction_ref, 
    COUNT(*) AS occurrence_count
FROM transactions
GROUP BY transaction_ref
HAVING COUNT(*) > 1;

-- 5. Daily success rate as a percentage.
SELECT 
    DATE(created_at) AS transaction_date,
    ROUND((SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) AS success_rate_percentage
FROM transactions
GROUP BY DATE(created_at)
ORDER BY transaction_date;

-- 6. Reconciliation: successful transaction count/value versus callback-success count/value.
WITH CallbackSuccess AS (
    SELECT DISTINCT transaction_id
    FROM callbacks
    WHERE callback_status = 'SUCCESS'
)
SELECT 
    DATE(t.created_at) AS transaction_date,
    COUNT(t.id) AS success_tx_count,
    SUM(t.amount) AS success_tx_value,
    COUNT(cs.transaction_id) AS callback_success_count,
    SUM(CASE WHEN cs.transaction_id IS NOT NULL THEN t.amount ELSE 0 END) AS callback_success_value
FROM transactions t
LEFT JOIN CallbackSuccess cs ON t.id = cs.transaction_id
WHERE t.status = 'SUCCESS'
GROUP BY DATE(t.created_at)
ORDER BY transaction_date;

-- 7. Average and p95 processing time where timestamps permit calculation.
SELECT 
    AVG(EXTRACT(EPOCH FROM (completed_at - created_at))) AS avg_processing_seconds,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (completed_at - created_at))) AS p95_processing_seconds
FROM transactions
WHERE completed_at IS NOT NULL AND status IN ('SUCCESS', 'FAILED');
