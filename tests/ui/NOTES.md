# UI Test Automation & CI Integration

## Continuous Integration (CI) Strategy

Integrating UI tests into CI/CD pipelines (like GitHub Actions, GitLab CI, or Jenkins) ensures that visual regressions and core broken flows are caught before reaching production.

### Pipeline Configuration
1. **Environment Setup:** The CI pipeline must install dependencies (`pip install -r requirements.txt`) and install the browsers (`playwright install --with-deps`).
2. **Application Startup:** The CI pipeline should spin up the application stack (e.g., using `docker-compose up -d`) and wait for the services to be healthy before executing tests.
3. **Execution Command:** `pytest tests/ui/ --tb=short -v`
4. **Artifacts:** Configure the pipeline to save Playwright trace files or screenshots on test failure so engineers can debug issues easily.

### Test Segregation (Smoke vs. Regression)
UI tests are notoriously slower and more brittle than unit or API tests.
- **Smoke Tests (Run on Every Commit/PR):** We should tag the absolute critical paths (e.g., Login, Create Payment) with `@pytest.mark.smoke`. These run on every push to ensure the application isn't fundamentally broken.
- **Regression Suite (Run Nightly / Before Release):** The full UI suite (including negative tests, edge cases, sorting/filtering validations) should be scheduled nightly or executed manually before a major release to save CI time and compute resources.
