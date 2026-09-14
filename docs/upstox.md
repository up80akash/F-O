# Broker REST configuration

The platform supports a manually configured REST broker through the
`ManualRestBroker` adapter. It is disabled by default and does not grant order
authority while the application is in paper mode.

## Configuration

Set these server-side variables in `.env`:

```env
BROKER_API_ENABLED=true
BROKER_API_BASE_URL=https://broker.example.com/api
BROKER_API_TOKEN=<server-side-token>
BROKER_API_AUTH_HEADER=Authorization
BROKER_API_AUTH_SCHEME=Bearer
BROKER_API_TIMEOUT_SECONDS=10
```

The default endpoint paths are:

- `GET /quote/{symbol}`
- `GET /quotes?symbols=NIFTY,BANKNIFTY`
- `GET /option-chain?symbol=NIFTY&expiry=YYYY-MM-DD`
- `GET /positions`
- `GET /orders`
- `POST /orders`
- `PATCH /orders/{order_id}`
- `DELETE /orders/{order_id}`
- `GET /orders/{order_id}`
- `GET /instruments`

Each path can be overridden with the corresponding `BROKER_API_*_PATH`
variable. The adapter expects JSON responses and accepts either a list or a
`{"data": [...]}` list wrapper for collection endpoints.

## Safety rules

- Tokens remain on the backend and are never sent to the frontend.
- Read-only requests can be enabled for integration testing in paper mode.
- Order placement, modification, and cancellation are rejected unless both
	`TRADING_MODE=LIVE` and `LIVE_TRADING_ENABLED=true` are explicitly set.
- Verify the effective configuration with `GET /api/broker/status`.

Upstox, Zerodha, and Angel One still require their official credentials and
provider-specific authentication. This generic adapter does not bypass broker
terms, exchange licensing, or provider rate limits.
