from flask import Blueprint

student_bp = Blueprint("student", __name__)


@student_bp.route("/")
def dashboard():
    return "Student dashboard placeholder."
