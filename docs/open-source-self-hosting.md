# Open-source and self-hosted deployment

This project can run on an open-source software stack. Hosting itself still needs a
machine or virtual server; open source does not mean that compute, market data, or
broker access is automatically free.

## Recommended stack

| Area | Recommended software | Purpose |
| --- | --- | --- |
| Host OS | Ubuntu 24.04 LTS or Debian 12 | Self-hosted runtime |
| Deployment | Docker Compose or Coolify | Container deployment |
| Reverse proxy | Caddy | HTTPS and routing with automatic Let's Encrypt certificates |
| API | FastAPI | Backend API |
| Database | PostgreSQL | Durable application state |
| Cache and queues | Redis | Temporary state and background jobs |
| Local AI | Ollama | Private model serving |
| Observability | Prometheus, Grafana, Loki | Metrics, dashboards, and logs |
| Frontend | Next.js | Dashboard |

Coolify is an open-source alternative to a managed deployment platform. It can
run on the same server and deploy this repository from GitHub, but Docker Compose
is the simplest path for the current repository.

## Market and broker APIs

There is no reliable, legal, universally free open-source API for real-time Indian
NSE F&O prices and order execution. Use an official broker API for live data and
orders:

- Upstox API: official API, credentials required, adapter already exists in this repo.
- Zerodha Kite Connect: official API, separate integration and account required.
- Angel One SmartAPI: official API, separate integration and account required.

Open-source research tools such as OpenBB can normalize data providers, but they do
not remove exchange licensing or broker authentication requirements. Yahoo Finance
or scraped NSE endpoints must not be treated as production F&O execution feeds.

Keep API keys and broker tokens only in the server-side `.env` or a secret manager.
Never put them in `NEXT_PUBLIC_*` variables or browser code.

## Self-hosting steps

1. Provision an Ubuntu or Debian server with at least 2 vCPU, 4 GB RAM, and 40 GB SSD.
   Ollama models may require substantially more disk and memory.
2. Install Docker Engine and the Docker Compose plugin.
3. Clone this repository on the server.
4. Create `.env` from `.env.example` and set strong production secrets.
5. Start the stack:

   ```bash
   docker compose up -d --build
   docker compose ps
   ```

6. Put Caddy or another open-source reverse proxy in front of the frontend and API.
7. Point DNS records at the server:

   ```text
   app.example.com -> frontend
   api.example.com -> backend:8000
   ```

8. Keep PostgreSQL, Redis, Ollama, Prometheus, Grafana, and Loki private.
9. Verify the safety boundary before connecting any broker account:

   ```bash
   curl -fsS https://api.example.com/health
   curl -fsS https://api.example.com/ready
   curl -fsS https://api.example.com/api/trading/status
   ```

The trading status must show `PAPER` mode and `execution_allowed: false`.

## Production environment baseline

```env
APP_ENV=production
DEBUG=false
TRADING_MODE=PAPER
LIVE_TRADING_ENABLED=false
SECRET_KEY=<random-secret>
JWT_SECRET=<random-secret>
NEXT_PUBLIC_API_URL=https://api.example.com
```

Before production use, replace wildcard CORS in `backend/app/main.py` with the
exact frontend origin, enable firewall rules for only SSH and HTTPS, configure
PostgreSQL backups, and monitor stale market data.

## Existing API endpoints

The current backend exposes:

- `GET /health`
- `GET /ready`
- `GET /`
- `GET /api/market/health`
- `GET /api/market/instruments`
- `GET /api/broker/status`
- `GET /api/trading/status`

The manual REST broker adapter is configurable through server-side `BROKER_API_*`
variables. Paper trading remains the default and AI has no execution authority.
