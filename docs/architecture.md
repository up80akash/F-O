# Architecture

This repository is organized as a modular monorepo with a clear separation between UI, API, market data, analytics, strategy, risk, trading execution, and monitoring.

## Core principles

1. Data is sourced first and never trusted blindly.
2. AI receives structured market context, not raw execution authority.
3. A deterministic risk engine validates every trade before execution.
4. Paper trading is the default operating mode.
5. Live trading is disabled unless explicitly configured.

## System layers

- Frontend: Next.js dashboard and chat interface
- Backend API: FastAPI endpoints and services
- Worker: background processing tasks
- Scheduler: recurring jobs
- Database: PostgreSQL for persistable state
- Cache: Redis for queueing, pub/sub, and temporary state
- Market Data: broker websocket / polling ingestion
- AI: local or remote model wrapper with JSON-only contract
- Risk Engine: deterministic validations and trade gating
- Paper trading: simulated execution with full logging and P&L
- Monitor stack: Prometheus, Grafana, Loki

## Phase roadmap

Refer to the main project specification and follow the required incremental sequence.
