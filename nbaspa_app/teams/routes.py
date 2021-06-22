"""Team information."""

from flask import Blueprint, render_template
from flask import current_app as app
from nbaspa.data.endpoints.parameters import SEASONS
import pandas as pd

from .data import (
    gen_teamlist,
    gen_summarymetrics,
    gen_gamelog,
    gen_roster
)

teams_bp = Blueprint(
    "teams_bp",
    __name__,
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"]
)

@teams_bp.get("/teams")
def teams_home():
    """Team homepage."""
    teamlist = gen_teamlist(app=app)
    return render_template(
        "team_nav.html",
        title="Teams",
        teamlist=[teamlist[i:i+6] for i in range(0, len(teamlist), 6)]
    )


@teams_bp.get("/teams/<int:teamid>")
def team_summary(teamid: int):
    """The team summary.

    Parameters
    ----------
    team_id : int
        The team identifier.
    """
    teamlist = gen_teamlist(app=app)
    teamname = [row["teamname"] for row in teamlist if row["teamid"] == teamid][0]
    summarydata = gen_summarymetrics(app=app, teamid=teamid)
    return render_template(
        "summary.html",
        title=teamname,
        teamid=teamid,
        teamname=teamname,
        data=summarydata
    )


@teams_bp.get("/teams/<int:teamid>/<season>/gamelog")
def team_gamelog(teamid: int, season: int):
    """The team gamelog for a given season.

    Parameters
    ----------
    team_id : int
        The team identifier.
    season : int
        The season year.
    """
    teamlist = gen_teamlist(app=app)
    teamname = [row["teamname"] for row in teamlist if row["teamid"] == teamid][0]
    data = gen_gamelog(app=app, teamid=teamid, season=season)
    data["GAME_DATE"] = pd.to_datetime(data["GAME_DATE"])
    data["W_PCT"] = (data["W_PCT"] * 100).round(1)
    return render_template(
        "gamelog.html",
        season=season,
        title=f"{teamname} - {season} Gamelog",
        teamid=teamid,
        teamname=teamname,
        data=data
    )


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
