import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Match
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

# Metrics definitions
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency/duration in seconds",
    ["method", "endpoint"]
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        
        # Try to find the matched route template to avoid high cardinality metrics
        # (e.g., /users/{id} instead of /users/123). If no match, fallback to request.url.path.
        path = request.url.path
        for route in request.app.routes:
            # We look for route instances that have the 'matches' method
            if hasattr(route, "matches"):
                match, _ = route.matches(request.scope)
                if match == Match.FULL:
                    path = getattr(route, "path", path)
                    break
        
        # Exclude /metrics to prevent noise
        if path == "/metrics":
            return await call_next(request)
            
        start_time = time.perf_counter()
        
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            # Handle unhandled exceptions as 500 Internal Server Error
            status_code = 500
            REQUEST_COUNT.labels(method=method, endpoint=path, status_code=status_code).inc()
            REQUEST_LATENCY.labels(method=method, endpoint=path).observe(time.perf_counter() - start_time)
            raise e
            
        # Update metrics for successful requests
        REQUEST_COUNT.labels(method=method, endpoint=path, status_code=status_code).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=path).observe(time.perf_counter() - start_time)
        return response

def metrics_handler():
    """
    Endpoint that exposes Prometheus metrics.
    It automatically includes default Python process and runtime metrics 
    collected by prometheus-client.
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
