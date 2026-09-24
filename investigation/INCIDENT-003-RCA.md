# INCIDENT-003 Root Cause Analysis

## Incident Summary
**Issue:** Transaction Search Performance Degradation
**Priority:** P2

## Observations and Reproduction Steps
1. Operations reported that searching for a transaction by `transaction_ref` or filtering transactions by `status` (e.g., finding stuck `PROCESSING` transactions) takes several seconds during peak hours.
2. We generated 50,000 synthetic transactions in the database to replicate the volume.
3. Running `SELECT * FROM transactions WHERE status = 'PROCESSING' AND created_at < NOW() - INTERVAL '15 minutes';` took over 300ms locally, which extrapolates to multiple seconds under heavy production load.

## Evidence Gathered
Running `EXPLAIN ANALYZE` on the problematic query revealed a **Sequential Scan** (Seq Scan) across the entire `transactions` table:
```text
Seq Scan on transactions (cost=0.00..345.12 rows=500 width=128)
Filter: ((status = 'PROCESSING') AND (created_at < (now() - '00:15:00'::interval)))
```
This indicates that the database is reading every single row to find the matching records because there is no index guiding it.

## Root Cause
The `transactions` table schema (`database/schema.sql`) lacked indexing for frequently queried columns like `transaction_ref`, `customer_id`, and `status`. As the data volume grows, sequential scans become exponentially slower and consume significant CPU and I/O resources, locking up the database.

## Immediate Corrective Action
Applied composite and single-column indexes concurrently (to avoid locking the table in production) to the most queried fields:
```sql
CREATE INDEX CONCURRENTLY idx_transactions_status_created_at ON transactions(status, created_at);
CREATE INDEX CONCURRENTLY idx_transactions_ref ON transactions(transaction_ref);
CREATE INDEX CONCURRENTLY idx_transactions_customer_id ON transactions(customer_id);
```

## Permanent Corrective/Preventive Action
- **Schema Migration Reviews:** Require all new database migrations or schema additions to be reviewed by a DBA or Senior Engineer to ensure query access patterns are matched with appropriate indexing.
- **Slow Query Logging:** Enable PostgreSQL's `log_min_duration_statement` to log queries taking longer than 100ms. Set up an alert (e.g., via Datadog or Prometheus/Grafana) when the rate of slow queries spikes.

## Validation Performed
Re-ran `EXPLAIN ANALYZE` after applying the indexes. The plan shifted to an **Index Scan**, taking <1ms:
```text
Index Scan using idx_transactions_status_created_at on transactions (cost=0.29..8.34 rows=500 width=128)
```
UI search responsiveness returned to normal sub-second latencies.
