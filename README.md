# F&O Trading Platform

Safety-first Indian F&O research and paper-trading platform.

The execution flow is deliberately constrained:

`DATA -> ANALYSIS -> STRATEGY -> AI INTERPRETATION -> RISK VALIDATION -> PAPER TRADE -> PERFORMANCE REVIEW`

Paper trading is the default. Live execution requires both `TRADING_MODE=LIVE`
and `LIVE_TRADING_ENABLED=true`, and remains disabled until explicitly configured.

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

Services:

- Frontend: http://localhost:3000
- API: http://localhost:8000
- API documentation: http://localhost:8000/docs
- Grafana: http://localhost:3001

The frontend can also be deployed without a custom domain to Cloudflare Pages:

```bash
cd frontend && npm ci && npm run build
npx wrangler login
npx wrangler pages deploy out --project-name fo-trading-platform --branch main
```

For Git-connected Pages builds, leave the root directory blank, use build command
`cd frontend && npm ci && npm run build`, output directory `frontend/out`, and
leave the deploy command blank. Cloudflare Pages publishes the output
automatically; do not use `npx wrangler deploy` because that command targets
Workers rather than Pages.

Verify the default safety posture:

```bash
curl http://localhost:8000/api/trading/status
```

See [docs/setup.md](docs/setup.md), [docs/architecture.md](docs/architecture.md),
[docs/cloudflare.md](docs/cloudflare.md), and
[docs/open-source-self-hosting.md](docs/open-source-self-hosting.md) for local
operation, system boundaries, and deployment guidance.
