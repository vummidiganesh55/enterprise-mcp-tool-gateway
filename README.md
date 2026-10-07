# Enterprise MCP Tool Gateway & Evaluation Platform

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![MCP](https://img.shields.io/badge/MCP-2.3.0-purple)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![Tests](https://img.shields.io/badge/Tests-167%20Passed-success)
![Security Benchmark](https://img.shields.io/badge/Security%20Accuracy-84%25-orange)

> **Enterprise-grade MCP Tool Gateway for secure, governed, observable, reliable, and evaluated AI tool execution.**

---

## 📌 Description

The **Enterprise MCP Tool Gateway & Evaluation Platform** is a production-oriented platform for managing and securing Model Context Protocol (MCP) tool execution.

The platform provides a centralized governance layer between AI/MCP clients and enterprise tools.

It combines:

- MCP tool discovery
- Tool registry and versioning
- RBAC authorization
- Policy-as-Code
- Risk classification
- Human approval for high-risk operations
- Input/output validation
- Rate limiting
- Idempotency
- Reliability controls
- Security scanning
- RAG knowledge retrieval
- Audit logging
- PostgreSQL persistence
- OpenTelemetry observability
- Tool health monitoring
- Security evaluation
- Benchmark history
- Chaos testing
- Streamlit monitoring dashboard
- Docker-based deployment

The goal is to demonstrate how MCP tools can be operated with **enterprise-grade security, governance, reliability, observability, and evaluation controls**.

---

# 🎯 Problem Statement

Modern AI agents increasingly interact with external tools and enterprise systems.

Without a centralized governance layer, tool execution can introduce risks such as:

- Unauthorized tool access
- Excessive permissions
- High-risk operations without approval
- Prompt injection
- Tool poisoning
- Malicious tool definitions
- Sensitive data exposure
- Repeated execution of the same operation
- Missing audit trails
- Poor observability
- Tool failures and timeouts
- Lack of systematic security evaluation
- No historical benchmark tracking

A production AI system therefore needs more than just an MCP server.

It needs a **governed MCP execution layer**.

---

# 💡 Solution

This project introduces an **Enterprise MCP Tool Gateway** that sits between MCP clients and enterprise services.

```text
AI / MCP Client
       |
       v
+---------------------------+
|     MCP TOOL GATEWAY      |
|---------------------------|
| Authentication            |
| RBAC / ABAC               |
| Policy-as-Code            |
| Risk Classification       |
| Human Approval            |
| Validation                |
| Rate Limiting             |
| Idempotency               |
| Security Scanner          |
| Reliability               |
+-------------+-------------+
              |
              v
        MCP Tools
              |
              v
       Service Layer
              |
       +------+------+
       |             |
       v             v
  PostgreSQL      External APIs
       |
       v
 Enterprise Data
````

The gateway evaluates every tool request before execution and provides observability and evaluation capabilities around the complete execution lifecycle.

---

# 🚀 Features

## MCP Gateway

* MCP Streamable HTTP server
* MCP client integration
* Tool discovery
* Tool registry
* Tool catalog
* Tool version management
* Tool enable/disable status
* Centralized tool execution

## MCP Tools

The platform currently exposes **11 MCP tools**:

| Tool                 | Version | Risk   |
| -------------------- | ------- | ------ |
| `health_check`       | v1.0.0  | LOW    |
| `customer_get`       | v1.0.0  | LOW    |
| `customer_update`    | v1.0.0  | MEDIUM |
| `customer_delete`    | v1.0.0  | HIGH   |
| `knowledge_search`   | v1.0.0  | LOW    |
| `knowledge_retrieve` | v1.0.0  | LOW    |
| `ticket_get`         | v1.0.0  | LOW    |
| `ticket_create`      | v1.0.0  | MEDIUM |
| `order_get`          | v1.0.0  | LOW    |
| `order_status`       | v1.0.0  | LOW    |
| `audit_search`       | v1.0.0  | MEDIUM |

---

# 🔐 Security & Governance

The gateway applies multiple security controls before tool execution.

### Authentication

JWT-based authentication infrastructure is provided for securing API access.

### RBAC

Role-based authorization controls which tools can be accessed by:

* `admin`
* `support`
* `viewer`

### Policy-as-Code

Authorization and risk rules are represented using YAML policies.

Example:

```yaml
policy:
  role: admin
  risk_level: HIGH
  action: REQUIRE_APPROVAL
```

This separates governance rules from application execution logic.

### Risk Classification

Every tool is classified as:

```text
LOW
MEDIUM
HIGH
```

Unknown tools default to a high-risk classification.

### Human Approval

High-risk operations require approval before execution.

For example:

```text
customer_delete
        |
        v
   HIGH RISK
        |
        v
 APPROVAL REQUIRED
        |
        v
 PENDING
```

Example real MCP execution result:

```json
{
  "success": false,
  "error": "APPROVAL_REQUIRED",
  "approval_id": "REQ-MCP-DELETE-001",
  "status": "PENDING"
}
```

### Security Scanner

The platform checks for:

* Prompt injection
* Tool poisoning
* Authorization bypass
* Data exposure
* Malicious tool definitions

---

# 🧠 RAG Knowledge Layer

The platform includes a lightweight RAG knowledge system for enterprise documentation.

It supports:

* Knowledge search
* Document retrieval
* TF-IDF embeddings
* Cosine similarity
* Relevant document ranking

Current example knowledge documents include:

* Customer Support Policy
* Refund Policy
* Security Policy

Example workflow:

```text
User Query
    |
    v
Knowledge Search
    |
    v
TF-IDF Representation
    |
    v
Cosine Similarity
    |
    v
Ranked Documents
    |
    v
Knowledge Retrieval
```

---

# 🛡️ Validation

The gateway validates both incoming requests and outgoing responses.

### Request Validation

Validates:

* Tool name
* Required fields
* Input structure
* Field constraints
* Data types

### Response Validation

Validates:

* Response schema
* Expected data structure
* Pydantic models
* Tool output integrity

Invalid requests and responses are rejected and recorded through the audit system.

---

# ⚡ Reliability

The gateway contains a reliability layer with:

* Retry
* Timeout
* Fallback
* Circuit Breaker
* Typed reliability errors
* Centralized execution handling

Execution flow:

```text
Tool Request
     |
     v
Retry
     |
     v
Timeout
     |
     v
Circuit Breaker
     |
     v
Fallback
     |
     v
Tool Execution
```

This prevents temporary tool failures from unnecessarily propagating through the system.

---

# 🔁 Idempotency

The platform supports idempotent tool execution.

An idempotency key prevents duplicate execution of the same operation.

```text
Request
   |
   v
Idempotency Key
   |
   +---- Existing Result ----> Return Previous Result
   |
   +---- New Request --------> Execute Tool
```

This is especially important for state-changing operations.

---

# 📊 Observability

The platform includes observability through:

* Structured audit logging
* Metrics
* Request tracking
* Tool execution statistics
* OpenTelemetry tracing
* Tool health monitoring
* Performance measurements

Tracked tool metrics include:

* Total requests
* Successful requests
* Failed requests
* Success rate
* Average latency
* Last execution time

---

# ❤️ Tool Health Monitoring

The dashboard provides real-time tool health information.

Current verified dashboard state:

```text
Total Tools      11
Healthy Tools    11
Disabled Tools   0
```

Each tool exposes:

* Version
* Risk level
* Health status
* Execution statistics

---

# 🧪 Evaluation Engine

The project contains a dedicated evaluation engine for testing security and governance behavior.

Evaluation categories include:

* Prompt Injection
* Tool Poisoning
* Authorization Bypass
* Data Exposure
* Malicious Tool Definition

The evaluation system records:

* Total cases
* Passed cases
* Failed cases
* Accuracy
* Category-level accuracy
* Historical benchmark runs

---

# 📊 Evaluation Results

A measured security benchmark contains:

```text
Total Cases       100
Passed             84
Failed             16
Accuracy        84.0%
```

Category-level measured results:

| Category                  | Accuracy |
| ------------------------- | -------: |
| Prompt Injection          |      80% |
| Tool Poisoning            |      80% |
| Authorization Bypass      |     100% |
| Data Exposure             |      80% |
| Malicious Tool Definition |      80% |

These are **measured benchmark results from the implemented evaluation dataset**, not theoretical claims.

---

# 📚 Evaluation History

Benchmark runs are persisted and displayed through the dashboard.

The current dashboard shows:

```text
Historical Benchmark Runs: 226
Latest Accuracy: 84.0%
Latest Passed: 84
Latest Failed: 16
```

Historical runs make it possible to compare evaluation results and identify regressions over time.

---

# 💥 Chaos Testing

The project includes failure simulation for resilience testing.

Current scenarios include:

* Simulated tool failure
* Simulated timeout
* Temporary failure followed by recovery

Example:

```text
Tool
 |
 +--> Failure
 |
 +--> Retry
 |
 +--> Recovery
 |
 +--> Successful Execution
```

This allows reliability behavior to be tested independently of real external failures.

---

# 🧪 Automated Testing

The project contains an automated test suite covering:

* MCP integration
* Tool registry
* Tool catalog
* Authorization
* Governance
* Policy engine
* Security scanner
* Prompt injection
* Tool poisoning
* Data exposure
* Validation
* Rate limiting
* Idempotency
* Reliability
* Retry
* Timeout
* Fallback
* Circuit breaker
* Tool health
* Metrics
* Evaluation
* Evaluation history
* Audit logging
* Tracing
* Chaos scenarios

### Latest verified test result

```text
167 passed in 8.39s
```

```text
167 Tests
0 Failures
```

---

# 🏗️ Architecture

The final architecture is organized into the following layers:

```text
                         USER / AI / MCP CLIENT
                                  |
                                  v
                     +-------------------------+
                     |     MCP TOOL GATEWAY    |
                     +-------------------------+
                     | Tool Discovery          |
                     | Tool Registry           |
                     | Tool Versioning         |
                     | Tool Catalog            |
                     | Authentication          |
                     | RBAC / ABAC             |
                     | Policy Engine           |
                     | Policy-as-Code          |
                     | Rate Limiting           |
                     | Risk Classification     |
                     | Input Validation        |
                     | Idempotency             |
                     | Human Approval          |
                     +------------+------------+
                                  |
                    +-------------+-------------+
                    |             |             |
                    v             v             v
                  TOOLS       RESOURCES      PROMPTS
                    |
                    v
             +--------------+
             | SERVICE LAYER|
             +------+-------+
                    |
             +------+----------------+
             |                       |
             v                       v
        PostgreSQL             External APIs
             |
             v
      ENTERPRISE DATA

             +----------------------+
             |     RAG TOOL          |
             | Knowledge Search      |
             | Document Retrieval    |
             | TF-IDF + Vector       |
             +----------+-----------+
                        |
                        v
                 Enterprise Docs

             +----------------------+
             |    RELIABILITY       |
             | Retry                |
             | Timeout              |
             | Fallback             |
             | Circuit Breaker      |
             +----------+-----------+
                        |
                        v
             +----------------------+
             |    OBSERVABILITY     |
             | Logs                 |
             | Metrics              |
             | OpenTelemetry        |
             | Tool Health          |
             +----------+-----------+
                        |
                        v
             +----------------------+
             |   SECURITY SCANNER   |
             | Prompt Injection     |
             | Tool Poisoning       |
             | Auth Bypass          |
             | Data Exposure        |
             +----------+-----------+
                        |
                        v
             +----------------------+
             |   EVALUATION ENGINE  |
             | Security             |
             | Accuracy             |
             | Validation           |
             | Reliability          |
             | Chaos Testing        |
             +----------+-----------+
                        |
                        v
             +----------------------+
             | EVALUATION HISTORY   |
             | Benchmark Runs       |
             | Historical Results   |
             | Regression Detection |
             +----------+-----------+
                        |
                        v
                  STREAMLIT
                   DASHBOARD
```

---

# 🔄 Workflow

A typical tool execution follows this pipeline:

```text
1. MCP Client
      |
      v
2. MCP Gateway
      |
      v
3. Authentication
      |
      v
4. RBAC Authorization
      |
      v
5. Security Scanner
      |
      v
6. Request Validation
      |
      v
7. Rate Limiting
      |
      v
8. Risk Classification
      |
      v
9. Human Approval
      |
      v
10. Idempotency
      |
      v
11. Reliability Executor
      |
      v
12. Tool Execution
      |
      v
13. Response Validation
      |
      v
14. Metrics + Health
      |
      v
15. Audit Logging
      |
      v
16. Response to MCP Client
```

For high-risk tools:

```text
MCP Request
    |
    v
Authorization
    |
    v
HIGH Risk
    |
    v
Approval Required
    |
    +---- Rejected/Pending ---> Stop
    |
    +---- Approved -----------> Execute
```

---

# 🛠️ Tech Stack

## Backend

* Python 3.14
* FastAPI
* Uvicorn
* Pydantic
* SQLAlchemy

## MCP

* MCP SDK 2.3.0
* MCP Client
* MCP Server
* Streamable HTTP

## Security

* JWT
* RBAC
* Policy-as-Code
* Risk Classification
* Security Scanner
* Human Approval
* Audit Logging

## AI / RAG

* TF-IDF
* Scikit-learn
* Cosine Similarity
* Enterprise Knowledge Retrieval

## Database

* PostgreSQL
* SQLAlchemy
* Repository Pattern

## Reliability

* Retry
* Timeout
* Fallback
* Circuit Breaker

## Observability

* OpenTelemetry
* Structured Logging
* Metrics
* Tool Health Monitoring

## Evaluation

* Python Evaluation Engine
* Security Benchmarking
* Evaluation History
* Chaos Testing
* Automated Tests

## Frontend

* Streamlit

## Infrastructure

* Docker
* Docker Compose

---

# 📂 Project Structure

```text
enterprise-mcp-tool-gateway/
│
├── app/
│   ├── config/
│   │
│   ├── mcp_client/
│   │   ├── client.py
│   │   ├── connection.py
│   │   ├── discovery.py
│   │   └── tool_caller.py
│   │
│   ├── mcp_gateway/
│   │   ├── server.py
│   │   ├── context.py
│   │   ├── registry.py
│   │   ├── discovery.py
│   │   ├── versioning.py
│   │   └── catalog.py
│   │
│   ├── security/
│   │   ├── authentication/
│   │   ├── authorization/
│   │   ├── policy/
│   │   ├── rate_limit/
│   │   ├── risk/
│   │   ├── approval/
│   │   ├── scanner/
│   │   └── audit/
│   │
│   ├── validation/
│   ├── idempotency/
│   ├── tools/
│   ├── resources/
│   ├── prompts/
│   ├── services/
│   ├── repositories/
│   ├── database/
│   ├── integrations/
│   ├── reliability/
│   └── observability/
│
├── evaluation/
│   ├── datasets/
│   ├── runner.py
│   ├── evaluator.py
│   ├── metrics.py
│   ├── benchmark.py
│   └── history.py
│
├── chaos/
│   └── scenarios.py
│
├── dashboard/
│   ├── dashboard.py
│   ├── pages/
│   │   ├── approvals.py
│   │   ├── audit.py
│   │   ├── benchmarks.py
│   │   ├── evaluation.py
│   │   ├── governance.py
│   │   ├── health.py
│   │   ├── metrics.py
│   │   ├── reliability.py
│   │   ├── security.py
│   │   └── tools.py
│   └── components/
│
├── tests/
├── load_tests/
├── docs/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── .env.example
├── .gitignore
└── README.md
```

---

# 📋 Prerequisites

Before running the project locally, install:

* Python 3.14+
* Git
* PostgreSQL
* Docker Desktop
* Docker Compose

Recommended:

```text
Windows 10/11
VS Code
PowerShell
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/vummidiganesh55/enterprise-mcp-tool-gateway.git
```

Navigate into the project:

```bash
cd enterprise-mcp-tool-gateway
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a local `.env` file.

```env
DATABASE_URL=postgresql://username:password@localhost:5432/mcp_gateway
JWT_SECRET_KEY=replace-with-a-strong-secret
```

Never commit `.env` to GitHub.

Use `.env.example` as the template:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/mcp_gateway
JWT_SECRET_KEY=replace-with-a-strong-secret
```

---

# ▶️ Usage

## Start the FastAPI backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

API:

```text
http://localhost:8000
```

Health endpoint:

```text
http://localhost:8000/health
```

---

## Start the MCP Gateway

Open another terminal:

```bash
python -m app.mcp_gateway.server
```

MCP endpoint:

```text
http://127.0.0.1:8001/mcp
```

The gateway registers 11 MCP tools.

---

## Start the MCP Client

```bash
python -m app.mcp_client.client
```

The client connects to the gateway, discovers the tools, and executes:

* Health check
* Customer retrieval
* Knowledge search
* Knowledge retrieval
* High-risk customer deletion

The high-risk deletion request demonstrates the approval mechanism.

---

## Start the Streamlit Dashboard

```bash
python -m streamlit run dashboard/dashboard.py
```

Dashboard:

```text
http://localhost:8501
```

---

# 🐳 Docker

Build and start the complete deployment:

```bash
docker compose build
docker compose up -d
```

Check containers:

```bash
docker compose ps
```

View gateway logs:

```bash
docker compose logs --tail=50 mcp-gateway
```

Stop services:

```bash
docker compose down
```

The Docker deployment contains:

```text
FastAPI API
MCP Gateway
PostgreSQL integration
Streamlit Dashboard
```

---

# 💡 Example

### Example: Low-risk operation

```text
Client
  |
  v
customer_get
  |
  v
RBAC
  |
  v
Policy
  |
  v
Validation
  |
  v
Execution
  |
  v
Customer Data
```

### Example: High-risk operation

```text
Client
  |
  v
customer_delete
  |
  v
RBAC: ALLOWED
  |
  v
Risk: HIGH
  |
  v
Human Approval
  |
  v
APPROVAL_REQUIRED
```

Example response:

```json
{
  "success": false,
  "error": "APPROVAL_REQUIRED",
  "approval_id": "REQ-MCP-DELETE-001",
  "status": "PENDING"
}
```

This prevents a high-risk operation from executing automatically.

---

# 🧪 Testing

Run the complete test suite:

```bash
python -m pytest
```

Latest verified result:

```text
167 passed in 8.39s
```

The test suite covers security, governance, validation, reliability, MCP integration, evaluation, health monitoring, audit logging, tracing, and chaos scenarios.

---

# 📊 Evaluation

Run the evaluation/benchmark workflow through the project's evaluation components and dashboard.

The security benchmark currently contains:

```text
100 evaluation cases
84 passed
16 failed
84.0% accuracy
```

Category results:

```text
Prompt Injection          80%
Tool Poisoning            80%
Authorization Bypass     100%
Data Exposure             80%
Malicious Tool Definition 80%
```

Evaluation history records benchmark runs for comparison and regression analysis.

---

# 📸 Screenshots / Demo

## Final Architecture

![Final Architecture](docs/screenshots/01-final-architecture.png)

---

## Main Dashboard

The main dashboard provides an overview of the MCP gateway and registered tools.

![Main Dashboard](docs/screenshots/02-main-dashboard.png)

---

## MCP Tool Registry

The registry displays all 11 MCP tools, versions, risk levels, and health status.

![MCP Tool Registry](docs/screenshots/03-mcp-tool-registry.png)

---

## High-Risk Approval

The `customer_delete` tool is classified as HIGH risk and requires approval before execution.

![High Risk Approval](docs/screenshots/04-high-risk-approval.png)

---

## Security Evaluation

Measured security benchmark:

* 100 cases
* 84 passed
* 16 failed
* 84% accuracy

![Security Evaluation](docs/screenshots/05-security-evaluation.png)

---

## Metrics

Tool execution metrics include request counts, success rate, failures, and latency.

![Metrics](docs/screenshots/06-metrics.png)

---

## Evaluation History

Historical benchmark runs are persisted and displayed for comparison.

![Evaluation History](docs/screenshots/07-evaluation-history.png)

---

## RAG Knowledge Search

The MCP client demonstrates enterprise knowledge search and document retrieval.

![RAG Knowledge Search](docs/screenshots/08-rag-knowledge-search.png)

---

## Automated Test Suite

Latest verified test run:

```text
167 passed
```

![Test Suite](docs/screenshots/09-test-suite.png)

---

## Tool Health Monitoring

Current verified tool health:

```text
11 Total Tools
11 Healthy
0 Disabled
```

![Tool Health](docs/screenshots/10-tool-health-metrics.png)

---

## MCP Gateway Server

The MCP server registers all 11 tools and exposes the Streamable HTTP endpoint.

![MCP Gateway](docs/screenshots/11-mcp-gateway-server.png)

---

## MCP Client Integration

The MCP client successfully connects to the gateway, discovers tools, executes RAG operations, and receives an approval response for the high-risk deletion operation.

![MCP Client](docs/screenshots/12-mcp-client.png)

---

# ⚡ Performance

The platform tracks tool execution performance through the metrics and observability layer.

Tracked metrics include:

* Request count
* Successful requests
* Failed requests
* Success rate
* Average latency
* Last execution time

Example dashboard measurements are available in the Metrics page.

Performance values shown in the dashboard are runtime measurements from the local environment and should not be interpreted as production infrastructure benchmarks.

---

# 🔐 Security

Security controls implemented in the platform include:

### Authentication

JWT-based authentication infrastructure.

### Authorization

RBAC-based tool permissions for:

```text
admin
support
viewer
```

### Policy Enforcement

Policy-as-Code using YAML configuration.

### Risk Management

```text
LOW
MEDIUM
HIGH
```

### Human Approval

HIGH-risk operations require approval.

### Security Scanning

Detection for:

```text
Prompt Injection
Tool Poisoning
Authorization Bypass
Data Exposure
Malicious Tool Definitions
```

### Auditability

Tool execution decisions and security events are recorded through the audit system.

---

# 🔮 Future Improvements

Potential future enhancements include:

* Distributed rate limiting
* Redis-backed shared state
* Production-grade identity provider integration
* Advanced ABAC policies
* Approval workflow UI
* Real-time alerting
* Distributed tracing backend
* Kubernetes deployment
* Multi-tenant isolation
* Advanced vector database integration
* Larger security evaluation datasets
* Automated regression gates in CI/CD
* Prometheus/Grafana integration

---

# ⚠️ Limitations

This project is a portfolio/engineering implementation and has limitations:

* Security benchmark results are based on the current evaluation dataset.
* The current RAG implementation uses TF-IDF and cosine similarity rather than a production vector database.
* Tool health statistics are primarily runtime application metrics.
* Performance measurements depend on the local execution environment.
* The approval workflow demonstrates governance behavior but is not intended to represent a complete enterprise IAM approval system.
* External enterprise integrations are represented through the implemented service/tool layer.
* Production deployment would require additional infrastructure hardening.

---

# 🤝 Contributing

Contributions are welcome.

### Development workflow

```bash
git clone https://github.com/vummidiganesh55/enterprise-mcp-tool-gateway.git

cd enterprise-mcp-tool-gateway

python -m venv .venv

pip install -r requirements.txt

python -m pytest
```

Create a feature branch:

```bash
git checkout -b feature/your-feature
```

Make your changes, add tests, and submit a pull request.

---

# 📄 License

This project is intended for educational, portfolio, and engineering demonstration purposes.

If you plan to distribute or modify the project publicly, add an appropriate open-source `LICENSE` file to the repository.

---

# 👨‍💻 Author

## Vummidi Naga Sai Ganesh

**AI / Machine Learning Engineer | Python | MCP | LLM | RAG | Agentic AI**

GitHub:

[https://github.com/vummidiganesh55](https://github.com/vummidiganesh55)

Project:

[https://github.com/vummidiganesh55/enterprise-mcp-tool-gateway](https://github.com/vummidiganesh55/enterprise-mcp-tool-gateway)

---

# ⭐ Project Highlights

```text
┌─────────────────────────────────────────────────────────┐
│       ENTERPRISE MCP TOOL GATEWAY & EVALUATION          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  11 MCP Tools                                           │
│  RBAC + Policy-as-Code                                  │
│  Risk Classification                                    │
│  Human Approval                                         │
│  Security Scanner                                       │
│  RAG Knowledge Retrieval                                │
│  Reliability Engineering                                │
│  Idempotency                                            │
│  PostgreSQL Persistence                                 │
│  OpenTelemetry                                          │
│  Tool Health Monitoring                                 │
│  Evaluation History                                     │
│  Security Benchmarking                                  │
│  Chaos Testing                                          │
│  Docker                                                 │
│                                                         │
│  100 Security Cases → 84% Measured Accuracy             │
│  167 Automated Tests → All Passing                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---
