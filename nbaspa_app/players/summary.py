"""Get season summary data."""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from flask import Flask
import numpy as np
import pandas as pd

from nbaspa.data.endpoints import AllPlayers, PlayerInfo

def get_top_players(app: Flask, Season: str) -> List[Dict]:
    """Get the top players for a given season.

    Parameters
    ----------
    app : Flask
        The current application.
    Season : str
        The season to search for.
    
    Returns
    -------
    List
        The JSON-ified output.
    """
    loader = AllPlayers(
        output_dir=Path(app.config["DATA_DIR"], Season),
        Season=Season
    )
    if not loader.exists():
        raise FileNotFoundError("Cannot find the roster info.")
    loader.load()

    playerindex = loader.get_data()
    playerindex.drop_duplicates(subset="PERSON_ID", keep="first", inplace=True)
    playerindex.set_index("PERSON_ID", inplace=True)
    gameratings = pd.read_csv(
        Path(app.config["DATA_DIR"], Season, "impact-summary.csv"), sep="|", index_col=0
    )
    gameratings.set_index("PLAYER_ID", inplace=True)
    gameratings["IMPACT_sum"] = gameratings["IMPACT_sum"].round(3)
    gameratings["IMPACT_mean"] = gameratings["IMPACT_mean"].round(3)
    gameratings["IMPACT+_sum"] = gameratings["IMPACT+_sum"].round(3)
    gameratings["IMPACT+_mean"] = gameratings["IMPACT+_mean"].round(3)
    gameratings["DISPLAY_FIRST_LAST"] = playerindex["DISPLAY_FIRST_LAST"]
    gameratings.reset_index(inplace=True)
    gameratings.sort_values(by="IMPACT+_mean", ascending=False, inplace=True)
    gameratings["RANK"] = np.arange(1, gameratings.shape[0] + 1)

    return gameratings.to_dict(orient="records")


def get_player_info(app: Flask, PlayerID: int) -> Dict:
    """Get player information.

    Parameters
    ----------
    app : Flask
        The current application.
    PlayerID : int
        The player identifier.
    
    Returns
    -------
    Dict
        The player info.
    """
    loader = PlayerInfo(PlayerID=PlayerID, output_dir=app.config["DATA_DIR"])
    if not loader.exists():
        raise FileNotFoundError("Cannot find the player information.")
    loader.load()
    info = loader.get_data("CommonPlayerInfo").to_dict(orient="records")[0]
    info["BIRTHDATE"] = datetime.strptime(info["BIRTHDATE"], "%Y-%m-%dT%H:%M:%S")

    return info

def get_player_time_series(app: Flask, PlayerID: int) -> List[Dict]:
    """Get the player time-series.
    
    Parameters
    ----------
    app : Flask
        The current application.
    PlayerID : int
        The player identifier.
    
    Returns
    -------
    Dict
        The player info.
    """
    performances = pd.concat(
        (
            pd.read_csv(fpath, sep="|", index_col=0, dtype={"GAME_ID": str})
            for fpath in Path(app.config["DATA_DIR"]).glob(f"*/impact-timeseries/data_{PlayerID}.csv")
        ),
        ignore_index=True
    )
    performances.rename(columns={"IMPACT+": "IMPACT_ADJ"}, inplace=True)
    performances = performances[(performances["IMPACT"] != 0) & (performances["IMPACT_ADJ"] != 0)].copy()
    performances.dropna(inplace=True)
    performances["IMPACT"] = performances["IMPACT"].round(3)
    performances["IMPACT_ADJ"] = performances["IMPACT_ADJ"].round(3)
    # Date parsing
    performances["GAME_DATE_PARSED"] = pd.to_datetime(performances["GAME_DATE"])
    performances["DAY"] = performances["GAME_DATE_PARSED"].dt.day
    performances["MONTH"] = performances["GAME_DATE_PARSED"].dt.month
    performances["YEAR"] = performances["GAME_DATE_PARSED"].dt.year

    return performances[
        ["IMPACT", "IMPACT_ADJ", "SEASON", "GAME_ID", "GAME_DATE", "DAY", "MONTH", "YEAR"]
    ].to_dict(orient="records")

def get_player_impact_profile(data: List[Dict]) -> List[Dict]:
    """Get the player impact profile.
    
    Parameters
    ----------
    data : list
        The output of ``get_player_time_series``
    
    Returns
    -------
    List
        A season-by-season average impact rating
    """
    df = pd.DataFrame(data)
    agg = df.groupby("SEASON")["IMPACT_ADJ"].mean().to_frame().reset_index()
    agg["YEAR"] = agg["SEASON"].str.split("-", expand=True)[0]
    agg["YEAR"] = agg["YEAR"].astype(int)

    return agg.to_dict(orient="records")

def get_all_players(app: Flask) -> List[Dict]:
    """Get all players.
    
    Parameters
    ----------
    app : Flask
        The current application.
    
    Returns
    -------
    List
        The JSON-ified output.
    """
    # Using 2019-20 season for the player directory
    loader = AllPlayers(
        output_dir=Path(app.config["DATA_DIR"], "2019-20"),
        Season="2019-20"
    )
    if not loader.exists():
        raise FileNotFoundError("Cannot find the roster info.")
    loader.load()
    df = loader.get_data()
    df.drop_duplicates(subset="PERSON_ID", keep="first", inplace=True)
    df["SECTION"] = df["DISPLAY_LAST_COMMA_FIRST"].str[0]
    df["TO_YEAR"] = df["TO_YEAR"].astype(int)
    df = df[df["TO_YEAR"] >= 2005].copy()

    output = {}
    for name, group in df.groupby("SECTION"):
        records = group.to_dict(orient="records")
        output[name] = [records[i:i+3] for i in range(0, len(records), 3)]

    return output


def get_top_performances(app: Flask, Season: str) -> List[Dict]:
    """Get top performances.
    
    Parameters
    ----------
    app : Flask
        The current application.
    Season : str
        The season to search for.
    
    Returns
    -------
    List
        The JSON-ified output.
    """
    loader = AllPlayers(
        output_dir=Path(app.config["DATA_DIR"], Season),
        Season=Season
    )
    if not loader.exists():
        raise FileNotFoundError("Cannot find the roster info.")
    loader.load()

    playerindex = loader.get_data()
    playerindex.drop_duplicates(subset="PERSON_ID", keep="first", inplace=True)
    playerindex.set_index("PERSON_ID", inplace=True)

    performances = pd.concat(
        (
            pd.read_csv(fpath, sep="|", index_col=0, dtype={"GAME_ID": str})
            for fpath in Path(app.config["DATA_DIR"]).glob(f"{Season}/impact-timeseries/data_*.csv")
        ),
        ignore_index=True
    )
    performances.set_index("PLAYER_ID", inplace=True)
    performances["DISPLAY_FIRST_LAST"] = playerindex["DISPLAY_FIRST_LAST"]
    performances.reset_index(inplace=True)
    performances.sort_values(by="IMPACT", ascending=False, inplace=True)
    performances["RANK"] = np.arange(1, performances.shape[0] + 1)
    performances["IMPACT"] = performances["IMPACT"].round(3)
    performances["GAME_DATE"] = pd.to_datetime(performances["GAME_DATE"])

    return performances.to_dict(orient="records")
