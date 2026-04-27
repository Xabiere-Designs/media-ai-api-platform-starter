from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

REQUEST_COUNT = Counter(
    "media_ai_requests_total",
    "Total request count",
    ["method", "path"],
)

REQUEST_LATENCY = Histogram(
    "media_ai_request_latency_seconds",
    "Request latency in seconds",
    ["path"],
)

metrics_router = APIRouter()


@metrics_router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
