from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from datetime import datetime

from app.extensions import db
from app.models.user import User, Role


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        print("1 - POST RECEIVED")

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")

        print("2 - FORM DATA OK")


        if not first_name or not last_name or not email or not password:
            flash("لطفاً همه فیلدها را پر کنید.", "danger")
            return redirect(url_for("auth.register"))


        existing_user = User.query.filter_by(email=email).first()

        print("3 - DATABASE CHECK OK")


        if existing_user:
            flash("این ایمیل قبلاً ثبت شده است.", "danger")
            return redirect(url_for("auth.register"))


        role = Role.query.filter_by(name="student").first()

        print("4 - ROLE CHECK OK")


        if not role:
            role = Role(
                name="student",
                description="Student"
            )

            db.session.add(role)
            db.session.commit()

            print("5 - ROLE CREATED")


        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role_id=role.id,
            is_active=True
        )

        user.set_password(password)

        print("6 - USER READY")


        db.session.add(user)
        db.session.commit()

        print("7 - USER SAVED")


        flash("ثبت نام با موفقیت انجام شد.", "success")

        return redirect(url_for("auth.login"))


    return render_template("auth/register.html")



@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()


        if user and user.check_password(password):

            login_user(user)

            user.last_login_at = datetime.utcnow()
            db.session.commit()

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