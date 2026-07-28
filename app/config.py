"""Environment-based configuration classes."""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "change-me-in-production"
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(basedir, "app.db")
    )

    # Render sometimes gives postgres:// instead of postgresql://
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER",
        os.path.join(basedir, "instance", "uploads")
    )

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    SITE_NAME = os.environ.get(
        "SITE_NAME",
        "Persian Language Institute"
    )

    SITE_URL = os.environ.get(
        "SITE_URL",
        "http://localhost:5000"
    )

    MAIL_SERVER = os.environ.get(
        "MAIL_SERVER",
        "localhost"
    )

    MAIL_PORT = int(
        os.environ.get("MAIL_PORT", 25)
    )

    MAIL_USE_TLS = os.environ.get(
        "MAIL_USE_TLS",
        "false"
    ).lower() == "true"

    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    MAIL_DEFAULT_SENDER = os.environ.get(
        "MAIL_DEFAULT_SENDER",
        "no-reply@example.com"
    )

    CACHE_TYPE = os.environ.get(
        "CACHE_TYPE",
        "SimpleCache"
    )

    RATELIMIT_DEFAULT = os.environ.get(
        "RATELIMIT_DEFAULT",
        "200 per day, 50 per hour"
    )

    RATELIMIT_STORAGE_URI = os.environ.get(
        "RATELIMIT_STORAGE_URI",
        "memory://"
    )

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False


class ProductionConfig(BaseConfig):
    DEBUG = False

    @staticmethod
    def init_app(app):
        BaseConfig.init_app(app)

        if app.config["SECRET_KEY"] == "change-me-in-production":
            app.logger.warning(
                "Using the default SECRET_KEY in production is insecure. "
                "Set the SECRET_KEY environment variable."
            )


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}