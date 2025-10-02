from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from kluster.models import User
from kluster.services.messaging_service import MessagingService

messages_bp = Blueprint("messages", __name__, url_prefix="/messages")

@messages_bp.route("")
@login_required
def inbox():
    threads = MessagingService.list_user_threads(current_user.id)
    # Compute the "other user" for display
    items = []
    for t in threads:
        other_id = t.user_b_id if t.user_a_id == current_user.id else t.user_a_id
        other = User.query.get(other_id)
        last = None
        msgs = MessagingService.thread_messages(t.id)
        if msgs:
            last = msgs[-1].created_at.strftime("%Y-%m-%d %H:%M")
        items.append({"thread": t, "other": other, "last": last})
    return render_template("messages_inbox.html", items=items)

@messages_bp.route("/start/<username>", methods=["GET", "POST"])
@login_required
def start(username: str):
    other = User.query.filter_by(username=username).first_or_404()
    if request.method == "POST":
        body = request.form.get("body", "").strip()
        if body:
            MessagingService.send(current_user.id, other.id, body)
            return redirect(url_for("messages.thread", username=other.username))
    return redirect(url_for("messages.thread", username=other.username))

@messages_bp.route("/with/<username>", methods=["GET", "POST"])
@login_required
def thread(username: str):
    other = User.query.filter_by(username=username).first_or_404()
    thr = MessagingService.get_or_create_thread(current_user.id, other.id)
    if request.method == "POST":
        body = request.form.get("body", "").strip()
        if body:
            MessagingService.send(current_user.id, other.id, body)
            return redirect(url_for("messages.thread", username=other.username))
    msgs = MessagingService.thread_messages(thr.id)
    return render_template("messages_thread.html", other=other, messages=msgs, thread=thr)
