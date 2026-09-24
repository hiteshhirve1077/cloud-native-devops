from flask import Flask, jsonify, Response, request
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
import os
import time

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "flask_http_request_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "flask_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
)


@app.before_request
def before_request():
    request.start_time = time.time()


@app.after_request
def after_request(response):
    request_latency = time.time() - request.start_time

    endpoint = request.endpoint or "unknown"

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        http_status=response.status_code,
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=endpoint,
    ).observe(request_latency)

    return response


@app.get("/")
def home():
    return jsonify({
        "message": "DevOps application is running!",
        "version": os.getenv("APP_VERSION", "1.0.0"),
    })


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


@app.get("/version")
def version():
    return jsonify({
        "version": os.getenv("APP_VERSION", "1.0.0"),
    })


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
