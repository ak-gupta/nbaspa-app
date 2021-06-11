"""Homepage information."""

from flask import Blueprint, render_template
from flask import current_app as app

home_bp = Blueprint(
    "home_bp",
    __name__,
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"]
)

@home_bp.get("/")
@home_bp.get("/home")
@home_bp.get("/index")
def home():
    """Homepage."""
    return render_template(
        "home.html",
        title="My Demo Title",
    )
