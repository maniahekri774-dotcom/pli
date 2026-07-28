from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required

from app.extensions import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email") or (request.json or {}).get("email")
        password = request.form.get("password") or (request.json or {}).get("password")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return jsonify({"status": "ok"})
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401
    return "Login page placeholder — build a real template here."


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
