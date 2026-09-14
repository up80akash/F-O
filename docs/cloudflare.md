# Cloudflare deployment

Cloudflare should be the public edge layer. The backend, database, Redis, broker
credentials, and Ollama service must remain private to the application network.

## Deployment checklist

1. Create a Cloudflare zone and point the application domain at the deployment host.
2. Create separate hostnames for the UI and API, for example `app.example.com` and `api.example.com`.
3. Route the UI hostname to the frontend service and the API hostname to port `8000`.
4. Enable HTTPS with Full (strict), HSTS, and a restrictive WAF policy.
5. Allow CORS only for the deployed UI hostname. Do not use `allow_origins=["*"]` in production.
6. Keep PostgreSQL, Redis, Ollama, Grafana, Loki, and Prometheus off the public network.
7. Set `TRADING_MODE=PAPER` and `LIVE_TRADING_ENABLED=false` for the first deployment.
8. Store broker and signing secrets in the deployment secret manager, never in Git or frontend variables.

## Smoke checks

```bash
curl -fsS https://api.example.com/health
curl -fsS https://api.example.com/ready
curl -fsS https://api.example.com/api/trading/status
```

The trading status response must report `mode` as `PAPER` and
`execution_allowed` as `false` before the deployment is considered ready.
