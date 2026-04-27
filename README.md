# Media AI Platform Starter

A production-style **FastAPI + PostgreSQL + Redis + JWT + Alembic + Kubernetes + Terraform + GitHub Actions** starter for a licensed media, catalog, or recommendation platform.

This is intentionally built to look like a **Platform / DevOps Engineer portfolio repo** instead of a toy app.

## Included

- FastAPI API with dependency injection, health probes, JWT auth, and metrics
- SQLAlchemy 2.0 ORM models
- Alembic migration scaffolding
- PostgreSQL persistence
- Redis-backed caching for recommendation responses
- Recommendation service with deterministic scoring you can later swap for embeddings + reranking
- Docker and docker-compose for local development
- Kubernetes manifests for Deployment, Service, HPA, ConfigMap, Secret, ServiceAccount, and Ingress
- Terraform starter modules for ECR and IAM/IRSA
- GitHub Actions CI workflow
- Pytest tests

## Architecture

- **API**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **DB**: PostgreSQL
- **Cache**: Redis
- **Auth**: OAuth2 password flow with JWT bearer tokens
- **Observability**: Prometheus metrics endpoint + structured request logging
- **Deploy target**: Kubernetes / EKS
- **Infra as Code**: Terraform
- **Delivery**: GitHub Actions

## Project structure

```text
app/
  api/routes/           # route handlers
  core/                 # settings, auth, logging, metrics
  db/                   # session + init helpers
  models/               # ORM models
  schemas/              # request/response models
  services/             # business logic
alembic/                # db migration scaffolding
k8s/base/               # kubernetes manifests
terraform/              # infrastructure starter
.github/workflows/      # CI
tests/                  # tests
```

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d postgres redis
uvicorn app.main:app --reload
```

## Seed a demo user and media

The app seeds:
- user: `demo`
- password: `ChangeMe123!`

## Run migrations later

This starter includes Alembic scaffolding. For a real project, point Alembic at the same `DATABASE_URL` and create revision files as your schema evolves.

## Obtain a token

```bash
curl -X POST http://localhost:8000/v1/auth/token   -H "Content-Type: application/x-www-form-urlencoded"   -d "username=demo&password=ChangeMe123!"
```

## Call the assistant

```bash
curl -X POST http://localhost:8000/v1/assistant/query   -H "Authorization: Bearer <TOKEN>"   -H "Content-Type: application/json"   -d '{
    "user_id": "demo",
    "query": "Show me gritty sci-fi thrillers with AI themes",
    "context": {
      "preferred_genres": ["sci-fi", "thriller"],
      "excluded_ratings": ["G"]
    }
  }'
```

## Endpoints

- `GET /healthz`
- `GET /readyz`
- `GET /metrics`
- `POST /v1/auth/token`
- `GET /v1/users/me`
- `POST /v1/assistant/query`

## Hardening path

1. Move JWT secret and database credentials to AWS Secrets Manager or Vault
2. Add refresh tokens and token revocation
3. Add PostgreSQL migrations per feature using Alembic
4. Add real recommendation signals from clickstream / watch history
5. Add vector search with pgvector or OpenSearch
6. Add OpenTelemetry traces and log shipping
7. Add environment promotion with Argo CD or GitHub environments
8. Add WAF, TLS cert management, PodDisruptionBudget, NetworkPolicy, and external secrets

## Why these choices

FastAPI documents first-class support for dependency injection and security patterns including OAuth2/JWT. SQLAlchemy 2.0’s ORM quick start and querying guides are the current primary references for ORM usage. Redis officially positions Redis for caching and related high-performance application patterns. HashiCorp’s tutorials show Terraform as the standard path to provision AWS services and EKS. citeturn215348search12turn215348search20turn215348search0turn215348search1turn215348search21turn215348search2turn215348search22turn215348search3turn215348search19
