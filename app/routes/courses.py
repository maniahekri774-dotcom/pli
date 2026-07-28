from flask import Blueprint, jsonify
from app.models.course import Course

courses_bp = Blueprint("courses", __name__)


@courses_bp.route("/")
def index():
    courses = Course.query.filter_by(is_published=True).all()
    return jsonify([{"title": c.title, "slug": c.slug} for c in courses])
