"""League pages."""

from flask import Blueprint, render_template, request
from flask import current_app as app

from nbaspa.data.endpoints.parameters import CURRENT_SEASON

league_bp = Blueprint(
    "league_bp",
    __name__,
    url_prefix="/league",
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"],
    static_url_path=f"/league/{app.config['STATIC_FOLDER']}"
)

@league_bp.get("/mvp", defaults={"season": CURRENT_SEASON, "page": 1})
@league_bp.get("/mvp/<season>/<int:page>")
def mvp(season: str, page: int):
    """Produce an ordered list of players based on page."""
    return render_template(
        "mvp.html",
        title=f"{season} MVP Tracker",
        season=season,
        page=page,
        mode=request.args.get("mode", "survival-plus"),
        sortBy=request.args.get("sortBy", "mean")
    )

@league_bp.get("/mip", defaults={"season": CURRENT_SEASON, "page": 1})
@league_bp.get("/mip/<season>/<int:page>")
def mip(season: str, page: int):
    """Produce an ordered list of players based on page."""
    return render_template(
        "mip.html",
        title=f"{season} MIP Tracker",
        season=season,
        page=page,
        mode=request.args.get("mode", "survival-plus"),
        sortBy=request.args.get("sortBy", "mean")
    )

@league_bp.get("/roty", defaults={"season": CURRENT_SEASON, "page": 1})
@league_bp.get("/roty/<season>/<int:page>")
def roty(season: str, page: int):
    """Produce an ordered list of players based on page."""
    return render_template(
        "roty.html",
        title=f"{season} ROtY Tracker",
        season=season,
        page=page,
        mode=request.args.get("mode", "survival-plus"),
        sortBy=request.args.get("sortBy", "mean")
    )

@league_bp.get("/season/<season>")
def season_home(season: str):
    """Get the season summary page.
    
    Parameters
    ----------
    season : str
        The season.
    """
    return render_template(
        "season_home.html", title=f"{season} Summary", season=season,
    )
