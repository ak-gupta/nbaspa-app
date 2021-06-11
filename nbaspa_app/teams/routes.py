"""Team information."""

from flask import Blueprint, render_template
from flask import current_app as app

teams_bp = Blueprint(
    "teams_bp",
    __name__,
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"]
)

@teams_bp.get("/teams")
def teams_home():
    """Team homepage."""
    return render_template(
        "team_nav.html",
        title="Teams",
    )


@teams_bp.get("/teams/<int:teamid>")
def team_summary(teamid: int):
    """The team summary.

    Parameters
    ----------
    team_id : int
        The team identifier.
    """
    return render_template(
        "summary.html",
        title="Summary",
        teamid=teamid
    )


@teams_bp.get("/teams/<int:team_id>/<int:season>/gamelog")
def team_gamelog(team_id: int, season: int):
    """The team gamelog for a given season.

    Parameters
    ----------
    team_id : int
        The team identifier.
    season : int
        The season year.
    """
    return render_template(
        "gamelog.html",
        title=f"{season} Gamelog"
    )


@teams_bp.get("/teams/<int:team_id>/<int:season>/players")
def team_players(team_id: int, season: int):
    """The team roster.

    Parameters
    ----------
    team_id : int
        The team identifier.
    season : int
        The season year.
    """
    return render_template(
        "players.html",
        title="{season} Roster"
    )
