from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from kluster.models import db, User
from kluster.services.auth_service import AuthService
from kluster.metrics import LOGGED_IN_USERS
import structlog

auth_bp = Blueprint("auth", __name__)
login_manager = LoginManager()
login_manager.login_view = "auth.login"

log = structlog.get_logger()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = AuthService.find_by_email(email)
        if user and user.check_password(password):
            login_user(user)
            LOGGED_IN_USERS.inc()
            log.info("user_login_success", user_id=user.id)
            return redirect(url_for("profile.view_profile", username=user.username))
        flash("Invalid credentials", "danger")
        log.info("user_login_failed", email=email)
    return render_template("login.html")

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        try:
            user = AuthService.register(email=email, username=username, password=password)
            login_user(user)
            LOGGED_IN_USERS.inc()
            return redirect(url_for("profile.view_profile", username=user.username))
        except ValueError as e:
            flash(str(e), "warning")
    return render_template("login.html", signup=True)

@auth_bp.route("/logout")
@login_required
def logout():
    uid = getattr(current_user, "id", None)
    logout_user()
    LOGGED_IN_USERS.dec()
    log.info("user_logout", user_id=uid)
    return redirect(url_for("auth.login"))
