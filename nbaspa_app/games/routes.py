"""Game information."""

from datetime import datetime
import json

from flask import Blueprint, render_template
from flask import current_app as app

from .calendar import get_scoreboard, create_list
from .summary import table_data
from .graph import line_graph, get_moments

TODAY = datetime.today()

game_bp = Blueprint(
    "game_bp",
    __name__,
    template_folder=app.config["TEMPLATES_FOLDER"],
    static_folder=app.config["STATIC_FOLDER"],
    static_url_path=f"/games/{app.config['STATIC_FOLDER']}"
)



@game_bp.get(
    "/games",
    defaults={"day": TODAY.day, "month": TODAY.month, "year": TODAY.year}
)
@game_bp.get("/games/<int:day>/<int:month>/<int:year>")
def schedule(day: int, month: int, year: int):
    """The schedule page.
    
    Parameters
    ----------
    day : int
        The day of the games.
    month : int
        The month of the games.
    year : int
        The year of the games.
    """
    gamedate = datetime(year=year, month=month, day=day)
    return render_template(
        "schedule.html",
        title="Game Schedule",
        gamedate=gamedate.strftime("%A, %B %d, %Y"),
        day=day,
        month=month,
        year=year,
    )


@game_bp.get("/games/<int:day>/<int:month>/<int:year>/<gameid>")
def game(day: int, month: int, year: int, gameid: str):
    """The overall game summary page.

    Parameters
    ----------
    day : int
        The day of the games.
    month : int
        The month of the games.
    year : int
        The year of the games.
    gameid : str
        The game ID.
    """
    tbs, pbs = table_data(app=app, GameID=gameid)
    gamedate = datetime(year=year, month=month, day=day)
    scoreboard = get_scoreboard(app=app, GameDate=gamedate)
    if scoreboard.exists():
        datalist = create_list(scoreboard)
        gameinfo = [itm for itm in datalist if itm["game_id"] == gameid][0]

    # Get the chart data
    linedata = line_graph(app=app, GameID=gameid)
    linechart = json.dumps(linedata, indent=2)

    moments = get_moments(app=app, GameID=gameid)
    pointchart = json.dumps(moments, indent=2)

    return render_template(
        "game.html",
        hometbs=[record for record in tbs if record["TEAM_ID"] == gameinfo["home_id"]][0],
        visitortbs=[record for record in tbs if record["TEAM_ID"] == gameinfo["visitor_id"]][0],
        homepbs=[record for record in pbs if record["TEAM_ID"] == gameinfo["home_id"]],
        visitorpbs=[record for record in pbs if record["TEAM_ID"] == gameinfo["visitor_id"]],
        gameinfo=gameinfo,
        year=gamedate.year,
        month=gamedate.month,
        day=gamedate.day,
        gameid=gameid
    )
