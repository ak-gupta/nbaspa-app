"""Create some summary plotting for each game."""

import os
from pathlib import Path
from typing import Dict, List, Tuple

from flask import Flask
import pandas as pd

from nbaspa.data.endpoints import BoxScoreTraditional

def table_data(app: Flask, GameID: str) -> Tuple:
    """Load the table data.

    Parameters
    ----------
    app : Flask
        The current application.
    GameID : str
        The game identifier.
    """
    season = GameID[2] + "0" + GameID[3:5] + "-" + str(int(GameID[3:5]) + 1)
    boxscore = BoxScoreTraditional(
        output_dir=os.path.join(app.config["DATA_DIR"], season),
        GameID=GameID
    )

    boxscore.load()
    tdata = boxscore.get_data("TeamStats")
    pdata = boxscore.get_data("PlayerStats")

    # Clean up percentages
    tdata["FG_PCT"] = (tdata["FG_PCT"] * 100).round(2)
    tdata["FG3_PCT"] = (tdata["FG3_PCT"] * 100).round(2)
    tdata["FT_PCT"] = (tdata["FT_PCT"] * 100).round(2)

    gameimpact = pd.read_csv(
        Path(app.config["DATA_DIR"], season, "game-impact", f"data_{GameID}.csv"),
        sep="|",
        index_col=0,
        dtype={"GAME_ID": str}
    )
    pdata["IMPACT"] = pd.merge(
        pdata,
        gameimpact,
        left_on=("GAME_ID", "TEAM_ID", "PLAYER_ID"),
        right_on=("GAME_ID", "TEAM_ID", "PLAYER_ID"),
        how="left"
    )["IMPACT"]
    pdata["IMPACT"] = pdata["IMPACT"].round(3)
    pdata.sort_values(by=["TEAM_ID", "IMPACT"], ascending=False, inplace=True)
    pdata = pdata[~pd.isnull(pdata["MIN"])]

    return tdata[
        [
            "TEAM_ID",
            "FG_PCT",
            "FGM",
            "FGA",
            "FG3_PCT",
            "FG3M",
            "FG3A",
            "FT_PCT",
            "FTM",
            "FTA",
            "PTS",
            "REB",
            "OREB",
            "DREB",
            "AST",
            "STL",
            "BLK",
            "TO"
        ]
    ].to_dict(orient="records"), pdata[
        [
            "TEAM_ID",
            "GAME_ID",
            "PLAYER_ID",
            "PLAYER_NAME",
            "MIN",
            "IMPACT",
            "PTS",
            "REB",
            "AST",
            "STL",
            "BLK",
            "TO",
            "FGM",
            "FGA"
        ]
    ].to_dict(orient="records")
