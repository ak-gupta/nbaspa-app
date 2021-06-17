"""Game information."""

from datetime import datetime
import json

from flask import Blueprint, render_template, redirect, request, url_for
from flask import current_app as app

from .calendar import get_scoreboard, create_list
from .forms import ScheduleDatePicker
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


@game_bp.post("/games")
def picker():
    """Using the datepicker to redirect to the correct day."""
    form = ScheduleDatePicker()
    gamedate = form.gamedate.data

    return redirect(
        url_for(
            "game_bp.schedule",
            day=gamedate.day,
            month=gamedate.month,
            year=gamedate.year
        )
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
    form = ScheduleDatePicker()
    gamedate = datetime(year=year, month=month, day=day)
    scoreboard = get_scoreboard(app=app, GameDate=gamedate)
    if scoreboard.exists():
        datalist = create_list(scoreboard)
    else:
        datalist = []

    return render_template(
        "schedule.html",
        title="Game Schedule",
        form=form,
        gamedate=gamedate.strftime("%A, %B %d, %Y"),
        day=day,
        month=month,
        year=year,
        data=[datalist[i:i+3] for i in range(0, len(datalist), 3)]
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
        title=f"{gameinfo['visitor_abbrev']} @ {gameinfo['home_abbrev']} Summary",
        hometbs=[record for record in tbs if record["TEAM_ID"] == gameinfo["home_id"]][0],
        visitortbs=[record for record in tbs if record["TEAM_ID"] == gameinfo["visitor_id"]][0],
        homepbs=[record for record in pbs if record["TEAM_ID"] == gameinfo["home_id"]],
        visitorpbs=[record for record in pbs if record["TEAM_ID"] == gameinfo["visitor_id"]],
        line_chart_data=linechart,
        point_chart_data=pointchart,
        gameinfo=gameinfo,
        gameid=gameid
    )


@game_bp.get("/games/detail/<gameid>")
def detail(gameid: str):
    """Player-level page for each game.

    Parameters
    ----------
    gameid : str
        The game ID.
    """
    # Get the player boxscore information
    playerid = int(request.args["playerid"])
    _, pbs = table_data(app=app, GameID=gameid)
    box = [record for record in pbs if record["PLAYER_ID"] == playerid][0]

    # Get the chart data
    linedata = line_graph(app=app, GameID=gameid)
    linechart = json.dumps(linedata, indent=2)

    moments = get_moments(app=app, GameID=gameid, num_moments=None, playerid=playerid)
    pointchart = json.dumps(moments, indent=2)

    return render_template(
        "detail.html",
        title=f"Game Detail - {box['PLAYER_NAME']}",
        box=box,
        line_chart_data=linechart,
        point_chart_data=pointchart,
    )
