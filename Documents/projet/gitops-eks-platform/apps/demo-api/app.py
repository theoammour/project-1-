import os

from flask import Flask, jsonify
from prometheus_client import Counter, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

REQUESTS = Counter("demo_api_requests_total", "Nombre total de requetes", ["endpoint"])
VERSION = os.getenv("APP_VERSION", "dev")


@app.get("/")
def index():
    REQUESTS.labels(endpoint="/").inc()
    return jsonify(
        service="demo-api",
        version=VERSION,
        message="Deploye en GitOps sur Amazon EKS",
    )


@app.get("/healthz")
def healthz():
    # Sonde utilisee par les liveness/readiness probes de Kubernetes.
    return jsonify(status="ok"), 200


# Expose /metrics au format Prometheus (scrape par kube-prometheus-stack).
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
