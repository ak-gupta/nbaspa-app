"""Retrieve calendar-specific data."""

from datetime import datetime
from pathlib import Path
from typing import List

from flask import Flask
from nbaspa.data.endpoints import Scoreboard

def get_scoreboard(app: Flask, GameDate: datetime) -> Scoreboard:
    """Load the scoreboard data.

    Parameters
    ----------
    app : Flask
        The current application.
    GameDate : datetime
        The game date.
    
    Returns
    -------
    Scoreboard
        The loaded Scoreboard object.
    """
    if GameDate.month > 8:
        season = str(GameDate.year) + "-" + str(GameDate.year + 1)[2:]
    else:
        season = str(GameDate.year - 1) + "-" + str(GameDate.year)[2:]
    scoreboard = Scoreboard(
        output_dir=Path(app.config["DATA_DIR"], season),
        GameDate=GameDate.strftime("%m/%d/%Y")
    )
    scoreboard.load()

    return scoreboard


def create_list(scoreboard: Scoreboard) -> List:
    """Create a list of the data necessary for the schedule page.

    Parameters
    ----------
    scoreboard : Scoreboard
        The loaded scoreboard data.
    
    Returns
    -------
    List
        A list of JSON data.
    """
    output = []
    header = scoreboard.get_data("GameHeader")
    linescore = scoreboard.get_data("LineScore")

    for _, row in header.iterrows():
        home = linescore[linescore["TEAM_ID"] == row["HOME_TEAM_ID"]]
        away = linescore[linescore["TEAM_ID"] == row["VISITOR_TEAM_ID"]]
        output.append(
            {
                "game_id": row["GAME_ID"],
                "home_id": row["HOME_TEAM_ID"],
                "home_pts": home["PTS"].values[0],
                "home_abbrev": home["TEAM_ABBREVIATION"].values[0],
                "visitor_id": row["VISITOR_TEAM_ID"],
                "visitor_pts": away["PTS"].values[0],
                "visitor_abbrev": away["TEAM_ABBREVIATION"].values[0]
            }
        )
    
    return output
