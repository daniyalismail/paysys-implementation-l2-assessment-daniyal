# Paysys Labs – Implementation & L2 Support Engineer Assessment

**Candidate:** M. Daniyal Ismail  
**Email:** daniyalismail19@gmail.com  
**Repository:** [daniyalismail/paysys-implementation-l2-assessment-daniyal](https://github.com/daniyalismail/paysys-implementation-l2-assessment-daniyal)  
**Submission Tag:** `submission-v1.0`  

---

## 📌 Executive Summary

This repository contains the complete solution for the **Paysys Labs Implementation & L2 Support Engineer Technical Assessment**. 

The solution covers the end-to-end operation, deployment, database analysis, automation, testing, and L2 incident troubleshooting for **MiniPay**—a payment-processing application consisting of a Web UI, REST APIs, and a relational database.

### Key Deliverables Included
- **Linux & Operations:** System performance evidence and a standalone health check script (`investigation/health-check.sh`).
- **SQL Data Analysis & Performance Tuning:** 7 safe, analytical SQL queries and query optimization with indexing (`sql/queries.sql`, `sql/PERFORMANCE.md`).
- **Kubernetes & Rancher Deployment:** Production-grade Kubernetes manifests (`kubernetes/minipay.yaml`) and operational guide (`evidence/rancher.md`).
- **Python L2 Support Tool:** CLI diagnostic tool for L2 support engineers with unit tests (`python/support_tool.py`, `python/test_support_tool.py`).
- **API & UI Test Automation:** Pytest REST API test suite and Playwright UI test suite (`tests/api/`, `tests/ui/`).
- **L2 Incident Root Cause Analyses (RCAs):** Detailed investigations for 3 critical production incidents (`investigation/INCIDENT-00*-RCA.md`).
- **AI Tooling Disclosure:** Detailed logging of AI tool usage, prompts, and verification in `AI_USAGE.md`.

---

## 📁 Repository Structure

```text
├── README.md                          # Main documentation & verification guide (This file)
├── SETUP.md                           # Quick environment setup guide
├── ARCHITECTURE.md                    # MiniPay system architecture & component breakdown
├── AI_USAGE.md                        # AI usage logs, prompts, and validation examples
├── .gitignore                         # Configured Git ignore rules
│
├── database/                          # Database schema and dummy data generator
│   ├── schema.sql                     # Table schemas (customers, transactions, callbacks, logs)
│   └── generate_data.py               # Python generator producing 50,000+ realistic rows
│
├── sql/                               # SQL queries & optimization
│   ├── queries.sql                    # 7 analytical queries required by assessment
│   └── PERFORMANCE.md                 # EXPLAIN query plan analysis & index optimization
│
├── kubernetes/                        # Container orchestration
│   └── minipay.yaml                   # Complete K8s manifests (Namespace, ConfigMap, Secrets, Deployments, Services)
│
├── python/                            # L2 Support Diagnostic Tool
│   ├── support_tool.py                # CLI diagnostic tool for inspecting transaction states
│   ├── test_support_tool.py           # Unit tests for support tool
│   └── requirements.txt               # Dependencies (pytest, playwright, psycopg2-binary, etc.)
│
├── tests/                             # Automated Test Suites
│   ├── api/
│   │   ├── test_api.py                # Pytest REST API test suite
│   │   └── NOTES.md                   # API test strategy & architecture
│   └── ui/
│       ├── test_ui.py                 # Playwright GUI automation test suite
│       └── NOTES.md                   # UI test strategy & selectors documentation
│
├── investigation/                     # Incident RCA Reports & Scripts
│   ├── INCIDENT-001-RCA.md            # RCA: DB Connection Pool Exhaustion (HTTP 500)
│   ├── INCIDENT-002-RCA.md            # RCA: Callback Webhook Timeouts / Egress Firewall Drops
│   ├── INCIDENT-003-RCA.md            # RCA: Memory Leak & Kubernetes OOMKilled Crashes
│   ├── health-check.sh                # Linux system & service health monitor script
│   └── kubernetes-findings.md         # Deployment verification and cluster findings
│
└── evidence/                          # Operational & Execution Evidence
    ├── linux.md                       # OS, CPU, RAM, Disk, process & network audit logs
    ├── rancher.md                     # Rancher cluster management & operational guide
    └── ui-test-report.md              # UI test execution summary & report
```

---

## 🚀 Tasks Overview & How to Cross-Check

Below is the detailed list of tasks completed and exact step-by-step commands to reproduce and cross-check each deliverable.

### 1. Task 01: Linux Operations & Git Workflow
- **Deliverables:** `evidence/linux.md`, `investigation/health-check.sh`, Git commit history.
- **What was done:**
  - Audited OS kernel, memory, CPU, disk usage, listening ports, network connectivity, and top memory-consuming processes.
  - Developed an executable Bash health-check script (`investigation/health-check.sh`) that tests CPU load, memory thresholds, disk space, and service endpoints.
  - Maintained clean, atomic incremental Git commits tagged as `submission-v1.0`.
- **How to Cross-Check:**
  ```bash
  # 1. View Linux environment audit evidence
  cat evidence/linux.md

  # 2. Run the automated health check script
  chmod +x investigation/health-check.sh
  ./investigation/health-check.sh
  ```

---

### 2. Task 02: Database & SQL Data Investigation
- **Deliverables:** `sql/queries.sql`, `sql/PERFORMANCE.md`, `database/schema.sql`, `database/generate_data.py`.
- **What was done:**
  - Designed 7 production SQL queries covering:
    1. Transaction count & total value by status and day.
    2. Top 10 customers by successful transaction value.
    3. Transactions stuck in `PROCESSING` status for over 15 minutes.
    4. Duplicate transaction reference identification.
    5. Daily success rate calculation (as percentage).
    6. Reconciliation of successful transactions vs. callback-success count & amount.
    7. Average and 95th-percentile (P95) transaction processing times.
  - Analyzed query execution plans using `EXPLAIN ANALYZE` in `sql/PERFORMANCE.md` and added B-Tree indexing on `(created_at, status)` to resolve sequential scans.
  - Verified queries against a live PostgreSQL database populated with 50,000 transactions.
- **How to Cross-Check:**
  ```bash
  # 1. Start a local PostgreSQL container
  docker run --name minipay-db -e POSTGRES_PASSWORD=secret -d -p 5432:5432 postgres:15-alpine
  sleep 5

  # 2. Generate schema and 50,000 sample transactions
  python3 database/generate_data.py > data.sql
  docker exec -i minipay-db psql -U postgres -c "CREATE DATABASE minipay;"
  docker exec -i minipay-db psql -U postgres -d minipay < database/schema.sql
  docker exec -i minipay-db psql -U postgres -d minipay < data.sql

  # 3. Execute all 7 analytical queries
  docker exec -i minipay-db psql -U postgres -d minipay < sql/queries.sql

  # Cleanup container when done
  docker rm -f minipay-db
  ```

---

### 3. Task 03: Kubernetes & Rancher Deployment
- **Deliverables:** `kubernetes/minipay.yaml`, `evidence/rancher.md`, `investigation/kubernetes-findings.md`.
- **What was done:**
  - Created a complete manifest (`kubernetes/minipay.yaml`) containing `Namespace` (`minipay`), `ConfigMap`, `Secret`, PostgreSQL `StatefulSet` & `Service`, API `Deployment` & `Service`, and UI `Deployment` & `Service`.
  - Fixed standard configuration errors (corrected image tag typos, container target ports, label selectors, Liveness/Readiness probes, and secret references).
  - Authored a step-by-step Rancher cluster management guide (`evidence/rancher.md`) detailing deployment, pod monitoring, log streaming, secret management, and ingress configuration.
- **How to Cross-Check:**
  ```bash
  # 1. Start local Kubernetes cluster (Minikube / Kind)
  TMPDIR=/tmp minikube start --driver=docker

  # 2. Apply the complete MiniPay Kubernetes manifest
  kubectl apply -f kubernetes/minipay.yaml

  # 3. Verify namespace objects, pods, services, and statefulsets
  kubectl get all -n minipay
  ```

---

### 4. Task 04: Python L2 Support Diagnostic Tool
- **Deliverables:** `python/support_tool.py`, `python/test_support_tool.py`, `python/requirements.txt`.
- **What was done:**
  - Built a command-line diagnostic tool (`python/support_tool.py`) for L2 support engineers to quickly investigate transaction issues.
  - Features include: transaction lookup by ID, status inspection, callback verification, associated system log analysis, actionable L2 support recommendations, `--json` formatted output for pipeline integration, and graceful offline fallback mode.
  - Implemented unit tests using Python's `unittest` module.
- **How to Cross-Check:**
  ```bash
  # 1. Install dependencies
  pip install -r python/requirements.txt

  # 2. Run unit tests
  python3 -m unittest python/test_support_tool.py -v

  # 3. Test CLI support tool in fallback/mock mode
  python3 python/support_tool.py --transaction TXN000123
  python3 python/support_tool.py --transaction TXN000123 --json
  ```

---

### 5. Task 05: Web Services & API Test Automation
- **Deliverables:** `tests/api/test_api.py`, `tests/api/NOTES.md`.
- **What was done:**
  - Automated REST API testing using `pytest` and `requests`.
  - Test coverage includes: API health check endpoint (`/health`), transaction creation (`POST /api/v1/payments`), transaction status query (`GET /api/v1/payments/{id}`), invalid payload validation (400 Bad Request), non-existent ID lookup (404 Not Found), and response headers validation.
- **How to Cross-Check:**
  ```bash
  # Run API test suite
  pytest tests/api/test_api.py -v
  ```

---

### 6. Task 06: GUI / UI Test Automation
- **Deliverables:** `tests/ui/test_ui.py`, `tests/ui/NOTES.md`, `evidence/ui-test-report.md`.
- **What was done:**
  - Built an end-to-end browser automation suite using **Playwright**.
  - Covered key user interactions: login flow, navigating to payment submission form, filling transaction details, submitting payment, verifying success alert banners, and confirming transaction table entry updates.
- **How to Cross-Check:**
  ```bash
  # Install Playwright browser binaries
  playwright install chromium

  # Run UI test suite (headless mode)
  pytest tests/ui/test_ui.py -v
  ```

---

### 7. Incidents & L2 Troubleshooting
- **Deliverables:** `investigation/INCIDENT-001-RCA.md`, `investigation/INCIDENT-002-RCA.md`, `investigation/INCIDENT-003-RCA.md`.
- **What was done:**
  - **INCIDENT-001:** Investigated database connection pool exhaustion resulting in HTTP 500 errors. Provided root cause, immediate mitigation (pool sizing & connection recycling), and long-term fix.
  - **INCIDENT-002:** Investigated callback delivery failures. Identified webhook timeout and egress network/firewall drops. Proposed exponential backoff retry mechanisms and firewall rules update.
  - **INCIDENT-003:** Investigated container crash loop (`OOMKilled`). Identified memory leaks in node process due to unclosed event listeners. Documented heap dump profiling, K8s memory limit adjustments, and fix.
- **How to Cross-Check:**
  ```bash
  # Read individual Incident RCA documents
  cat investigation/INCIDENT-001-RCA.md
  cat investigation/INCIDENT-002-RCA.md
  cat investigation/INCIDENT-003-RCA.md
  ```

---

## 🛠️ Complete Quick Start Command Log

To clone, set up the environment, and execute all checks sequentially, run the following commands:

```bash
# 1. Clone the repository
git clone https://github.com/daniyalismail/paysys-implementation-l2-assessment-daniyal.git
cd paysys-implementation-l2-assessment-daniyal

# 2. Verify git submission tag
git tag -l

# 3. Set up Python Virtual Environment & Install Dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r python/requirements.txt
playwright install chromium

# 4. Run Linux Health Check Script
chmod +x investigation/health-check.sh
./investigation/health-check.sh

# 5. Run Python Support Tool Unit Tests
python3 -m unittest python/test_support_tool.py -v

# 6. Run API Test Suite
pytest tests/api/test_api.py -v

# 7. Run UI Test Suite
pytest tests/ui/test_ui.py -v
```

---

## 🤖 AI Usage Disclosure & Ownership

As permitted and encouraged by the assessment guidelines, AI assistance (Gemini 3.1 Pro & Gemini 3.6 Flash) was utilized for brainstorming, drafting shell scripts, generating realistic test dataset generation scripts, and framing incident RCA structures.

All generated code, SQL queries, Kubernetes manifests, and test suites were manually reviewed, validated against live Docker/PostgreSQL containers, tested locally, and adjusted for production accuracy. Full details and prompt logs are recorded in [`AI_USAGE.md`](file:///media/daniyalismail19/backup1/paysys-implementation-l2-assessment/AI_USAGE.md).

---

## 📧 Contact
For any queries or follow-up technical discussions regarding this submission:
- **Name:** M. Daniyal Ismail
- **Email:** daniyalismail19@gmail.com
- **Phone:** +92 335-5577990
