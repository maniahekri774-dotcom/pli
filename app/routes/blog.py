from flask import Blueprint, jsonify
from app.models.content import BlogPost

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/")
def index():
    posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.published_at.desc()).all()
    return jsonify([{"title": p.title, "slug": p.slug} for p in posts])
