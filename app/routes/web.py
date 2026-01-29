"""Web routes for frontend"""
from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    """Home page"""
    return render_template("index.html")


@web_bp.route("/chat")
def chat():
    """Chat page"""
    return render_template("chat.html")
