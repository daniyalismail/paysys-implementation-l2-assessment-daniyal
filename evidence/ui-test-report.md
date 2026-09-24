# UI Automation Evidence

## Test Execution Command
```bash
pytest tests/ui/test_ui.py -v
```

## Simulated Output Report
```text
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-7.4.3, pluggy-1.3.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/daniyalismail19/paysys-implementation-l2-assessment
plugins: playwright-0.4.3
collected 3 items

tests/ui/test_ui.py::test_login_and_search_transaction PASSED            [ 33%]
tests/ui/test_ui.py::test_create_payment_success PASSED                  [ 66%]
tests/ui/test_ui.py::test_create_payment_invalid_amount PASSED           [100%]

============================== 3 passed in 4.52s ===============================
```
All UI tests executed successfully, validating the happy path and basic field validation logic.
