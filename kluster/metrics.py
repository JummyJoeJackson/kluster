from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from flask import Response, request
import time
import structlog

log = structlog.get_logger()

REQUEST_COUNT = Counter(
    "kluster_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "http_status"]
)
REQUEST_LATENCY = Histogram(
    "kluster_http_request_latency_seconds",
    "Latency of HTTP requests in seconds",
    ["method", "endpoint"]
)
LOGGED_IN_USERS = Gauge(
    "kluster_logged_in_users",
    "Number of authenticated sessions"
)

def metrics_endpoint():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

def before_request_metrics():
    request._start_time = time.perf_counter()

def after_request_metrics(response):
    try:
        latency = time.perf_counter() - getattr(request, "_start_time", time.perf_counter())
        REQUEST_LATENCY.labels(request.method, request.endpoint or "unknown").observe(latency)
        REQUEST_COUNT.labels(request.method, request.endpoint or "unknown", response.status_code).inc()
    except Exception as exc:
        log.warning("metrics_after_request_error", error=str(exc))
    return response
