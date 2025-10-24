from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from kluster.models import User, Notification, Message, db
from kluster.services.messaging_service import MessagingService

messages_bp = Blueprint("messages", __name__, url_prefix="/messages")

@messages_bp.route("")
@login_required
def inbox():
    threads = MessagingService.list_user_threads(current_user.id)
    items = []
    for t in threads:
        other_id = t.user_b_id if t.user_a_id == current_user.id else t.user_a_id
        other_user = User.query.get(other_id)
        msgs = MessagingService.thread_messages(t.id)
        last = msgs[-1].created_at.strftime("%Y-%m-%d %H:%M") if msgs else None
        items.append({"thread": t, "other": other_user, "last": last})
    return render_template("messages_inbox.html", items=items)

@messages_bp.route("/start/<username>", methods=["GET", "POST"])
@login_required
def start(username: str):
    other = User.query.filter_by(username=username).first_or_404()
    if request.method == "POST":
        body = request.form.get("body", "").strip()
        if body:
            message = MessagingService.send(current_user.id, other.id, body)
            send_notification(other.id, message.id)
            return redirect(url_for("messages.thread", username=other.username))
    return redirect(url_for("messages.thread", username=other.username))

@messages_bp.route("/with/<username>", methods=["GET", "POST"])
@login_required
def thread(username: str):
    other = User.query.filter_by(username=username).first_or_404()
    thread = MessagingService.get_or_create_thread(current_user.id, other.id)
    if request.method == "POST":
        body = request.form.get("body", "").strip()
        if body:
            message = MessagingService.send(current_user.id, other.id, body)
            send_notification(other.id, message.id)
            return redirect(url_for("messages.thread", username=other.username))

    messages = MessagingService.thread_messages(thread.id)
    unread = Notification.query.join(Notification.message).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False,
        Message.thread_id == thread.id).all()

    for notif in unread:
        notif.is_read = True
    db.session.commit()
    return render_template("messages_thread.html", other=other, messages=messages, thread=thread)


def send_notification(user_id: int, message_id: int) -> None:
    notification = Notification(user_id=user_id, message_id=message_id)
    db.session.add(notification)
    db.session.commit()

def fetch_unread_notifications(user_id: int):
    return Notification.query.filter_by(user_id=user_id, is_read=False).all()
