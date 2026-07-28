from flask import Blueprint
from app.decorators import student_required

student_bp = Blueprint("student", __name__)


@student_bp.route("/")
@student_required
def dashboard():
    return "Student dashboard placeholder."