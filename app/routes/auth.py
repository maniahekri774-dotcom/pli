from datetime import datetime
import traceback

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from app.extensions import db
from app.models.user import User, Role


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    try:
        if request.method == "POST":

            email = request.form.get("email")
            password = request.form.get("password")

            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):

                if not user.is_active:
                    flash("Your account is disabled.", "danger")
                    return redirect(url_for("auth.login"))

                login_user(user)

                user.last_login_at = datetime.utcnow()
                db.session.commit()

                if user.has_role("student"):
                    return redirect(url_for("student.dashboard"))

                elif user.has_role("teacher"):
                    return redirect(url_for("teacher.dashboard"))

                elif user.has_role("admin") or user.has_role("super_admin"):
                    return redirect(url_for("admin.dashboard"))

                return redirect(url_for("main.index"))

            flash("Invalid email or password.", "danger")

        return render_template("auth/login.html")

    except Exception as e:
        traceback.print_exc()

        return f"""
        <h1>LOGIN ERROR</h1>
        <pre>
        {str(e)}
        </pre>
        """, 500



@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    try:

        if request.method == "POST":

            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            email = request.form.get("email")
            password = request.form.get("password")

            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                flash("Email already exists.", "danger")
                return redirect(url_for("auth.register"))

            student_role = Role.query.filter_by(name="student").first()

            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                role=student_role
            )

            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            flash("Registration successful. Please login.", "success")

            return redirect(url_for("auth.login"))

        return render_template("auth/register.html")


    except Exception as e:
        traceback.print_exc()

        return f"""
        <h1>REGISTER ERROR</h1>
        <pre>
        {str(e)}
        </pre>
        """, 500



@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("main.index"))