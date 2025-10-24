import os
from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from dotenv import load_dotenv
import logging
from werkzeug.exceptions import HTTPException

# Import app configuration and utilities
from kluster.config import DevelopmentConfig, TestingConfig, ProductionConfig
from kluster.logging_conf import setup_logging
from kluster.metrics import before_request_metrics, after_request_metrics
from kluster.models import db
from kluster.routes import auth_bp, profile_bp, collection_bp, search_bp, health_bp, messages_bp, notifications_bp
from kluster.routes.auth import login_manager


def create_app(config_name: str | None = None) -> Flask:
    load_dotenv()
    env = config_name or os.getenv("FLASK_ENV", "development")
    setup_logging(os.getenv("LOG_LEVEL", "INFO"))

    app = Flask(__name__, template_folder="templates", static_folder="static")

    if env == "production":
        app.config.from_object(ProductionConfig)
    elif env == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(collection_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(notifications_bp)

    app.before_request(before_request_metrics)
    app.after_request(after_request_metrics)

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    @app.errorhandler(404)
    def page_not_found(e):
        return redirect(url_for('auth.login'))
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return e
        app.logger.error(f"Server Error: {e}", exc_info=True)
        return "Internal Server Error", 500

    return app
