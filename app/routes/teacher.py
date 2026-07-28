from flask import Blueprint
from app.decorators import teacher_required

teacher_bp = Blueprint("teacher", __name__)


@teacher_bp.route("/")
@teacher_required
def dashboard():
    return "Teacher dashboard placeholder."