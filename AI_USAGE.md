# AI Usage Documentation

As permitted and encouraged by the assessment instructions, AI tools were utilized to accelerate development and ensure best practices.

## Tools Used
- **Gemini 3.1 Pro (via Antigravity IDE Agent)**

## Tasks for Which AI Was Used
1. **Repository Structure:** Generating the directory structure and required markdown templates.
2. **Linux & Git:** Formulating bash commands to collect system metrics (`top`, `ss`, `df`, etc.) and writing the `health-check.sh` script.
3. **Database:** Writing optimized SQL queries and the `PERFORMANCE.md` explanation of indexing benefits.
4. **Kubernetes:** Identifying bugs in `broken-api.yaml` and creating a complete standard Kubernetes manifest set (`minipay.yaml`) incorporating ConfigMaps, Secrets, Deployments, and StatefulSets.
5. **Python Support Tool:** Generating the `support_tool.py` script and the associated `pytest` unit tests.
6. **Testing & Automation:** Writing `pytest-playwright` and `requests` API test suites.
7. **Incident RCA Documentation:** Structuring the RCA reports for incidents 001, 002, and 003 into a professional format.

## Interaction Summaries
1. **Prompt:** "Write a bash script for a basic system health check that checks CPU, memory, disk, and network."
   **Summary:** The AI generated a script using `uptime`, `free`, `df`, and `ping`. I reviewed it to ensure it was lightweight and portable across Linux distros.
2. **Prompt:** "What is wrong with this kubernetes deployment yaml? (pasted broken-api.yaml)"
   **Summary:** The AI identified 6 distinct issues, including the selector mismatch, port mismatch, and missing image. I validated these against standard Kubernetes documentation.
3. **Prompt:** "Write a pytest API test suite for a /payments and /customers endpoint testing idempotency and invalid fields."
   **Summary:** The AI generated `test_api.py`. I requested modifications to ensure it ignored 502 errors if the backend was completely unreachable during local testing.

## Validation of Generated Output
Every piece of generated code (Python scripts, bash scripts, SQL queries) was reviewed manually. The Python code was structurally checked to ensure it wouldn't throw syntax errors and properly utilized standard libraries like `argparse` and `logging`. The SQL queries were read to ensure they answered the exact business questions asked in the assessment (e.g., handling the `callback_success_value` correctly without duplicating amounts on multiple successful callbacks).

## Example of Corrected Output
During the generation of the SQL query for "Reconciliation: successful transaction count/value versus callback-success count/value," the AI initially used a standard `LEFT JOIN callbacks`. I realized that if a transaction had multiple successful callbacks (which shouldn't happen, but could in a buggy system), it would multiply the `SUM(t.amount)`. I corrected the AI by suggesting the use of a CTE (`WITH CallbackSuccess AS ... SELECT DISTINCT transaction_id`) to ensure each transaction is only counted once for the success value.
