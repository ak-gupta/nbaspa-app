"""Homepage information."""

from flask import Blueprint, render_template
from flask import current_app as app

from nbaspa.data.endpoints.parameters import CURRENT_SEASON

home_bp = Blueprint(
    "home_bp",
    __name__,
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"],
    static_url_path=f"/home/{app.config['STATIC_FOLDER']}",
)


@home_bp.get("/")
@home_bp.get("/home")
@home_bp.get("/index")
def homepage():
    """Homepage."""
    return render_template("home.html", title="NBA SPA Homepage", season=CURRENT_SEASON)
