# MiniPay System Architecture

## Overview
MiniPay is a minimal payment-processing application consisting of three main tiers:
1. **Frontend UI:** A web interface for searching transactions and submitting payments.
2. **Backend API (REST):** A service that processes UI requests, handles business logic, and interacts with the database.
3. **Database:** A relational database (PostgreSQL) for storing customers, transactions, and callbacks.

## Component Diagram
```mermaid
graph TD
    User([End User]) -->|HTTP/80| UI[MiniPay UI (Nginx)]
    UI -->|REST API Calls| API[MiniPay API (Python/Node)]
    API -->|TCP/5432| DB[(PostgreSQL Database)]
```

## Kubernetes Deployment Strategy
- **Namespace:** `minipay` encapsulates all resources.
- **ConfigMap & Secrets:** Configuration (like `DB_HOST`) is injected via `minipay-config`. Passwords and credentials are injected via `minipay-secrets`.
- **Database (StatefulSet):** PostgreSQL is deployed as a `StatefulSet` with a `PersistentVolumeClaim` to ensure data durability across pod restarts.
- **API (Deployment):** The API layer is stateless and scaled to 2 replicas for high availability. Liveness and Readiness probes ensure traffic is only routed to healthy pods.
- **UI (Deployment):** The UI is served as static assets via Nginx. It is exposed externally (for demonstration) via a `NodePort` Service.
