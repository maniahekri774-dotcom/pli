from flask import Blueprint
from app.decorators import admin_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@admin_required
def dashboard():
    return "Admin dashboard placeholder."