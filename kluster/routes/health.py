from flask import Blueprint, jsonify
from kluster.metrics import metrics_endpoint

health_bp = Blueprint("health", __name__)

@health_bp.route("/healthz")
def health():
    # Simple readiness probe
    return jsonify(status="ok")

@health_bp.route("/livez")
def live():
    # Simple liveness probe
    return jsonify(status="alive")

@health_bp.route("/metrics")
def metrics():
    return metrics_endpoint()
