"""Application factory for the Persian Language Institute Management System."""

import os
from flask import Flask, render_template, request

from app.config import config
from app.extensions import db, migrate, login_manager, mail, csrf, cache, limiter, cors
from app.logging_config import configure_logging


def create_app(config_name=None):
    """Create and configure the Flask application instance."""
    config_name = config_name or os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    configure_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_shell_context(app)
    register_template_globals(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)
    cors.init_app(app)

    limiter.init_app(app)
    limiter._default_limits = [app.config["RATELIMIT_DEFAULT"]]


def register_blueprints(app):
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.student import student_bp
    from app.routes.teacher import teacher_bp
    from app.routes.admin import admin_bp
    from app.routes.blog import blog_bp
    from app.routes.courses import courses_bp
    from app.routes.health import health_bp
    from app.routes.api_v1 import api_v1_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(student_bp, url_prefix="/dashboard/student")
    app.register_blueprint(teacher_bp, url_prefix="/dashboard/teacher")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(blog_bp, url_prefix="/blog")
    app.register_blueprint(courses_bp, url_prefix="/courses")
    app.register_blueprint(health_bp)
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(429)
    def ratelimit_error(error):
        return render_template("errors/429.html"), 429

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error("Server Error: %s | Path: %s", error, request.path)
        return render_template("errors/500.html"), 500


def register_shell_context(app):
    from app.models.user import User, Role
    from app.models.course import Course, Category
    from app.models.enrollment import Enrollment

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "User": User,
            "Role": Role,
            "Course": Course,
            "Category": Category,
            "Enrollment": Enrollment,
        }


def register_template_globals(app):
    @app.context_processor
    def inject_globals():
        return {
            "site_name": app.config["SITE_NAME"],
            "site_url": app.config["SITE_URL"],
        }
