from functools import wraps
from flask import abort
from flask_login import current_user, login_required


def role_required(role_name):
    def decorator(func):

        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):

            if not current_user.has_role(role_name):
                abort(403)

            return func(*args, **kwargs)

        return wrapper

    return decorator



def student_required(func):
    return role_required("student")(func)



def teacher_required(func):
    return role_required("teacher")(func)



def admin_required(func):
    return role_required("admin")(func)



def super_admin_required(func):
    return role_required("super_admin")(func)