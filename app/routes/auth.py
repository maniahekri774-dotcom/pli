from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models.user import User


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("این ایمیل قبلاً ثبت شده است.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name
        )

        db.session.add(user)
        db.session.commit()

        flash("ثبت نام با موفقیت انجام شد.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)

            flash("ورود موفق بود.", "success")

            return redirect(url_for("main.index"))

        flash("ایمیل یا رمز عبور اشتباه است.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()

    flash("با موفقیت خارج شدید.", "success")

    return redirect(url_for("auth.login"))