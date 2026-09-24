# Local Environment Setup

To reproduce the MiniPay environment and run the test suites locally, follow these instructions.

## Prerequisites
- Docker & Docker Compose (or Minikube/Kind for Kubernetes testing)
- Python 3.10+
- Git

## 1. Kubernetes Setup (Optional for API testing, required for K8s evaluation)
To deploy the mock application into a local cluster:
```bash
# Start Minikube
minikube start

# Apply the manifests
kubectl apply -f kubernetes/minipay.yaml

# Verify pods are running
kubectl get pods -n minipay
```

## 2. Python Environment Setup
Set up the virtual environment to run the support tool and test suites:
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r python/requirements.txt
playwright install --with-deps
```

## 3. Running the Support Tool
You can run the Python diagnostic utility to inspect transactions. Since the mock environment does not contain a populated Postgres instance, the tool defaults to mocked data if it cannot connect:
```bash
python python/support_tool.py --transaction TXN000123
```
To run it against a real database, set the environment variables:
```bash
DB_HOST=localhost DB_PORT=5432 DB_USER=minipay_user DB_PASSWORD=super_secret_password DB_NAME=minipay python python/support_tool.py --transaction TXN000123
```

## 4. Running the Tests
The test suites are designed to hit the local application. 

**API Tests:**
```bash
pytest tests/api/test_api.py -v
```

**UI Tests:**
```bash
pytest tests/ui/test_ui.py -v
```
*(Note: Ensure the target application is running on port 8080 or update `BASE_URL` in the test files).*
