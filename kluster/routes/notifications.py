from flask import Blueprint, render_template
from flask_login import login_required, current_user
from kluster.models import Notification, db

notifications_bp = Blueprint("notifications", __name__, url_prefix="/notifications")

@notifications_bp.route("")
@login_required
def view_notifications():
    notifications = current_user.notifications.order_by(Notification.created_at.desc()).all()

    unread = current_user.notifications.filter_by(is_read=False).all()
    for notification in unread:
        notification.is_read = True
    db.session.commit()

    return render_template("notifications.html", notifications=notifications)
