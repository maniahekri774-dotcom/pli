from flask import Blueprint, jsonify

api_v1_bp = Blueprint("api_v1", __name__)


@api_v1_bp.route("/ping")
def ping():
    return jsonify({"pong": True})
