# INCIDENT-001 Root Cause Analysis

## Incident Summary
**Issue:** Intermittent Transaction Search Failure (HTTP 500)
**Priority:** P2

## Observations and Reproduction Steps
1. The operations team provided a list of failing `transaction_ref` values (e.g., `TXN10029`) and successful ones (`TXN10030`).
2. Sending a GET request to `/api/payments/TXN10029` resulted in a `500 Internal Server Error`.
3. Sending a GET request to `/api/payments/TXN10030` returned a `200 OK` with the transaction JSON payload.

## Evidence Gathered
By inspecting the application logs via `kubectl logs deployment/minipay-api`:
```text
[ERROR] 2023-10-26 14:30:12 - Exception processing request for TXN10029
Traceback (most recent call last):
  File "api.py", line 45, in get_transaction
    "completed_at": row["completed_at"].isoformat()
AttributeError: 'NoneType' object has no attribute 'isoformat'
```

## Hypotheses Considered
- Database connection failure for specific IDs (rejected due to 500 error only on certain valid IDs).
- Application failing to handle `null` values for optional fields (Accepted). 

## Root Cause
The database schema allows `completed_at` to be `NULL` (e.g., when a transaction is still in `PROCESSING`). The API code blindly attempted to call `.isoformat()` on the `completed_at` field without checking if it was `None`. Transactions that were already `SUCCESS` or `FAILED` had a valid timestamp and succeeded. Transactions in `PROCESSING` threw an `AttributeError`.

## Immediate Corrective Action
Rolled out a hotfix to the API code to add a null check:
```python
"completed_at": row["completed_at"].isoformat() if row["completed_at"] else None
```
Restarted the deployment to apply the patch.

## Permanent Corrective/Preventive Action
- **Code Review:** Ensure all nullable database columns are checked before method invocation.
- **Testing:** Added a unit test specifically verifying that querying a `PROCESSING` transaction (with a null `completed_at`) returns a `200 OK`.
- **Validation Schema:** Implement a serialization library (like Pydantic or Marshmallow) that safely handles `Optional` fields automatically.

## Validation Performed
Executed `GET /api/payments/TXN10029` (a PROCESSING transaction) and received a `200 OK` with `"completed_at": null`.
