# Production Deployment

## Docker with MySQL

```
docker run -d --name cs-roster -p 8000:8000 \
  -e DB_HOST=host -e DB_USER=user -e DB_PASSWORD=pass -e DB_NAME=cs_roster \
  cs-roster:latest
```

## Health Checks

- GET /health (liveness)
- GET /api/health (readiness)
