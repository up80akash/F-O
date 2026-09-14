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

## Frontend without a custom domain

The dashboard is configured as a static export for Cloudflare Pages. It can be
published with Cloudflare's default `pages.dev` hostname:

```bash
cd frontend
npm ci
npm run build
npx wrangler login
npx wrangler pages deploy out --project-name fo-trading-platform --branch main
```

The deployment URL will be similar to:

```text
https://fo-trading-platform.pages.dev
```

### Cloudflare Pages Git settings

For a Git-connected Pages project, use these settings:

```text
Root directory:        frontend
Build command:         npm ci && npm run build
Build output directory: out
Deploy command:        leave blank
```

Cloudflare Pages automatically publishes the output directory after the build.
Do not use `npx wrangler deploy` or a custom `wrangler pages deploy` command for
a Git-connected Pages project. Those commands call the Cloudflare API with the
build token and can fail when the token does not have Pages permissions.

If the Pages project runs the build from the repository root instead, use:

```text
Build command:         cd frontend && npm ci && npm run build
Build output directory: frontend/out
Deploy command:         leave blank
```

The repository includes `wrangler.toml` with the Pages output directory. The
Cloudflare dashboard settings still take precedence for a Git-connected Pages
build, so verify the root directory and output directory there.

If a separate Workers Builds workflow requires a deploy command, create an
account API token with `Account -> Cloudflare Pages -> Edit` for account
`f207b777c7bc6a3a41ddd0a5efb384d7`, store it as `CLOUDFLARE_API_TOKEN`, and use
`npx wrangler pages deploy frontend/out --project-name fo-trading-platform`.

The backend still needs to run on a VPS or container host. Set
`NEXT_PUBLIC_API_URL` to that backend URL before building the frontend if the
dashboard makes API requests.
