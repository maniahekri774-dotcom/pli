from flask import Blueprint

teacher_bp = Blueprint("teacher", __name__)


@teacher_bp.route("/")
def dashboard():
    return "Teacher dashboard placeholder."
