# Setup Guide

## Prerequisites

- Docker and Docker Compose
- Git
- Python 3.12+ for local backend work
- Node.js 20+ for frontend work

## Local environment setup

1. Copy `.env.example` to `.env`.
2. Update values for local or production usage.
3. Start infrastructure:
   ```bash
   docker compose up --build
   ```
4. Validate backend:
   ```bash
   curl http://localhost:8000/health
   ```
5. Validate frontend:
   - Open http://localhost:3000

## Development notes

- Do not commit secrets.
- Keep trading mode in `PAPER` by default.
- Only enable live trading after explicit risk review and testing.

## Operational smoke test

After startup, verify the safety boundary:

```bash
curl http://localhost:8000/api/trading/status
```

The response must contain `"mode":"PAPER"` and
`"execution_allowed":false`. The frontend should be treated as a dashboard,
not as an authority to bypass this backend gate.
