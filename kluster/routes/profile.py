from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from kluster.models import User
import structlog

profile_bp = Blueprint("profile", __name__, url_prefix="/u")
log = structlog.get_logger()

@profile_bp.route("/<username>")
@login_required
def view_profile(username: str):
    user: User = User.query.filter_by(username=username).first_or_404()
    is_owner = current_user.id == user.id
    return render_template("profile.html", user=user, is_owner=is_owner)

@profile_bp.route("/<username>/update", methods=["POST"])
@login_required
def update_profile(username: str):
    if current_user.username != username:
        return ("Forbidden", 403)
    current_user.bio = request.form.get("bio", "")
    current_user.specialization = request.form.get("specialization", "")
    from kluster.models import db
    db.session.commit()
    log.info("profile_updated", user_id=current_user.id)
    return render_template("profile.html", user=current_user, is_owner=True)
