from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from kluster.services.collection_service import CollectionService
from kluster.services.price_service import PriceService

collection_bp = Blueprint("collection", __name__, url_prefix="/collection")

@collection_bp.route("")
@login_required
def view_collection():
    try:
        items = CollectionService.list_items(current_user.id)
        total = CollectionService.total_value(current_user.id)
        average = CollectionService.average_value(current_user.id)
        centerpiece = max(items, key=lambda x: x.estimated_value, default=None)
        series = PriceService.get_series(centerpiece.id if centerpiece else 0, centerpiece.estimated_value if centerpiece else 0.0)
        return render_template("collection.html", items=items, total=total, average=average, centerpiece=centerpiece, series=series)
    except SQLAlchemyError as e:
        print(f"Database Error: {e}")
        flash("An error occurred while fetching your collections.", "danger")
        return redirect(url_for("profile.profile"))
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return "Internal Server Error", 500

@collection_bp.route("/add", methods=["POST"])
@login_required
def add_item():
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "")
    category = request.form.get("category", "")
    value = float(request.form.get("estimated_value", "0") or 0)
    CollectionService.add_item(current_user.id, name, description, category, value)
    return redirect(url_for("collection.view_collection"))

@collection_bp.route("/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_item(item_id: int):
    try:
        CollectionService.delete_item(current_user.id, item_id)
    except ValueError:
        abort(404)
    return redirect(url_for("collection.view_collection"))
