from flask import Blueprint, render_template, request
from flask_login import login_required
from kluster.services.search_service import SearchService

search_bp = Blueprint("search", __name__, url_prefix="/search")

@search_bp.route("", methods=["GET", "POST"])
@login_required
def search():
    term = request.values.get("q", "")
    users = SearchService.search_users(term) if term else []
    items = SearchService.search_items(term) if term else []
    return render_template("search.html", term=term, users=users, items=items)
