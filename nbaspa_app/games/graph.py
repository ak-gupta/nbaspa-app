"""Generate the line plot data."""

from pathlib import Path
from typing import Dict, List

from flask import Flask
import pandas as pd

from nbaspa.data.endpoints.pbp import EventTypes

EVT = EventTypes()

def line_graph(app: Flask, GameID: str) -> List[Dict]:
    """Get the graph data.

    Parameters
    ----------
    app : Flask
        The current application.
    GameID : str
        The game identifier.
    
    Returns
    -------
    List[Dict]
        The JSON-ified data.
    """
    season = GameID[2] + "0" + GameID[3:5] + "-" + str(int(GameID[3:5]) + 1)
    linedata = pd.read_csv(
        Path(app.config["DATA_DIR"], season, "survival-prediction", f"data_{GameID}.csv"),
        sep="|",
        index_col=0,
        dtype={"GAME_ID": str}
    )
    linedata["WIN_PROB"] = linedata["WIN_PROB"].round(3)

    return linedata[["TIME", "WIN_PROB"]].to_dict(orient="records")


def get_moments(app: Flask, GameID: str) -> List[Dict]:
    """Get the top moments from a given game.

    Parameters
    ----------
    app : Flask
        The current application
    GameID : str
        The game identifier
    
    Returns
    -------
    List
        The JSON-ified output.
    """
    # Get play-by-play data
    season = GameID[2] + "0" + GameID[3:5] + "-" + str(int(GameID[3:5]) + 1)

    pbp = pd.read_csv(
        Path(app.config["DATA_DIR"], season, "pbp-impact", f"data_{GameID}.csv"),
        sep="|",
        index_col=0,
        dtype={"GAME_ID": str}
    )
    pbp = pbp[~pbp.duplicated(subset="TIME", keep="last")].copy()
    teamevents = [
        EVT.SUBSTITUTION,
        EVT.TIMEOUT,
        EVT.JUMP_BALL,
        EVT.PERIOD_BEGIN,
        EVT.UNKNOWN,
        EVT.REPLAY,
    ]
    pbp = pbp[(pbp["PLAYER1_IMPACT"] != 0) & (~pbp["EVENTMSGTYPE"].isin(teamevents))]
    pbp.sort_values(by="SURV_PROB_CHANGE", ascending=False, key=abs, inplace=True)
    pbp = pbp.head(n=5).copy()
    pbp["DESCRIPTION"] = pbp[["HOMEDESCRIPTION", "VISITORDESCRIPTION"]].bfill(axis=1).iloc[:, 0]
    pbp["SURV_PROB"] = pbp["SURV_PROB"].round(3)
    pbp["SURV_PROB_CHANGE"] = pbp["SURV_PROB_CHANGE"].round(3)

    return pbp[
        [
            "TIME",
            "PERIOD",
            "PCTIMESTRING",
            "SCOREMARGIN",
            "SURV_PROB",
            "SURV_PROB_CHANGE",
            "DESCRIPTION",
            "PLAYER1_ID"
        ]
    ].to_dict(orient="records")

