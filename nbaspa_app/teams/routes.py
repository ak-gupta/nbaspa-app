"""Team information."""

from flask import Blueprint, render_template
from flask import current_app as app

from .data import (
    gen_teamlist,
    gen_roster
)

teams_bp = Blueprint(
    "teams_bp",
    __name__,
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"],
    static_url_path=f"/teams/{app.config['STATIC_FOLDER']}"
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
    return render_template("teamsummary.html", teamid=teamid)

@teams_bp.get("/teams/<int:teamid>/<season>")
def team_season_summary(teamid: int, season: int):
    """The team season summary.
    
    Parameters
    ----------
    teamid : int
        The team identifier.
    season : str
        The season.
    """
    return render_template("teamseason.html", teamid=teamid, season=season)


@teams_bp.get("/teams/<int:teamid>/<season>/players")
def team_players(teamid: int, season: int):
    """The team roster.

    Parameters
    ----------
    team_id : int
        The team identifier.
    season : int
        The season year.
    """
    teamlist = gen_teamlist(app=app)
    teamname = [row["teamname"] for row in teamlist if row["teamid"] == teamid][0]
    roster = gen_roster(app=app, teamid=teamid, season=season)
    return render_template(
        "players.html",
        title=f"{season} Roster",
        teamid=teamid,
        teamname=teamname,
        season=season,
        data=[roster[i:i+3] for i in range(0, len(roster), 3)]
    )
