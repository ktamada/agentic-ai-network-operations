# Agentic AI Telco — Complete VS Code Project

This folder is the consolidated Phase 1–5 project. There are no separate phase directories.

## Import into VS Code

```powershell
cd agentic_ai_telco_complete_vscode_project
code .
```

## Setup

```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your OpenAI API key to `.env`.

## Start infrastructure

```powershell
docker compose up -d
docker compose ps
```

Create Kafka topics using the commands in `KAFKA_TOPICS.md`.

## Start FastAPI

```powershell
python -m uvicorn app.main:app --reload
```

Swagger: `http://127.0.0.1:8000/docs`

Prometheus: `http://127.0.0.1:9090`

Metrics: `http://127.0.0.1:8000/metrics/`

## Test incident

```json
{
  "customer_id": "CUST-1001",
  "message": "My internet has been slow since yesterday and my bill is higher this month."
}
```

Expected network-change workflow:
`AWAITING_APPROVAL -> approval -> execution -> validation`.

## Project capabilities

- Customer care/account/billing/service tools
- Supervisor, Customer Care, Network Diagnostic and RCA LLM definitions
- Network change simulation
- Human approval gate
- Validation
- Kafka integration scaffolding
- PostgreSQL model scaffolding
- Idempotency/approval hardening files
- Prometheus application metrics
- Prometheus-backed network telemetry adapter

### Integration note

Some files named `*_snippet.py` or `*_phase4.py` are preserved from the incremental build because they are merge/reference implementations from the earlier phases. The base API remains runnable independently, while those files show the advanced integrations to wire in next.
