"""File I/O paths."""

from datetime import datetime
import json
from pathlib import Path

from flask import Blueprint, request
from flask import current_app as app
import numpy as np
import pandas as pd

from nbaspa.data.endpoints import AllPlayers, PlayerInfo, PlayerGameLog
from nbaspa.data.factory import NBADataFactory

io_players = Blueprint("io_bp", __name__)

@io_players.get("/players/time-series")
def player_time_series():
    """Retrieve player impact time-series."""

    performances = pd.read_csv(
        Path(
            app.config["DATA_DIR"],
            request.args["Season"],
            "impact-timeseries",
            f"data_{request.args['PlayerID']}.csv"
        ),
        sep="|",
        index_col=0,
        dtype={"GAME_ID": str}
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

    columns = [
        "PLAYER_ID",
        "IMPACT",
        "IMPACT_ADJ",
        "SEASON",
        "GAME_ID",
        "GAME_DATE",
        "DAY",
        "MONTH",
        "YEAR",
    ]

    return json.dumps(performances[columns].to_dict(orient="records"))

@io_players.get("/players/impact-profile")
def player_impact_profile():
    """Retrieve a player impact profile."""
    performances = pd.concat(
        (
            pd.read_csv(fpath, sep="|", index_col=0, dtype={"GAME_ID": str})
            for fpath in Path(app.config["DATA_DIR"]).glob(f"*/impact-timeseries/data_{request.args['PlayerID']}.csv")
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
    # Get every season gamelog
    seasons = set(row["SEASON"] for _, row in performances.iterrows())
    calls = []
    for season in seasons:
        calls.append(
            (
                "PlayerGameLog",
                {
                    "Season": season,
                    "output_dir": Path(app.config["DATA_DIR"], season),
                    "PlayerID": request.args["PlayerID"]
                }
            )
        )
    factory = NBADataFactory(calls=calls)
    factory.load()
    gamelog = factory.get_data()
    # Merge with the performance data
    performances = pd.merge(
        performances,
        gamelog[["Game_ID", "PTS", "REB", "AST"]],
        left_on="GAME_ID",
        right_on="Game_ID",
        how="left"
    )
    # Aggregate to the season
    agg = performances.groupby("SEASON")[["IMPACT_ADJ", "PTS", "REB", "AST"]].mean().reset_index()
    agg["YEAR"] = agg["SEASON"].str.split("-", expand=True)[0]
    agg["YEAR"] = agg["YEAR"].astype(int)
    agg["IMPACT_ADJ"] = agg["IMPACT_ADJ"].round(3)
    agg["PTS"] = agg["PTS"].round(1)
    agg["REB"] = agg["REB"].round(1)
    agg["AST"] = agg["AST"].round(1)
    agg["PLAYER_ID"] = request.args["PlayerID"]

    return json.dumps(agg.to_dict(orient="records"))

@io_players.get("/players/index")
def player_index():
    """Retrieve player index."""
    loader = AllPlayers(
        output_dir=Path(app.config["DATA_DIR"], request.args["Season"]), Season=request.args["Season"]
    )
    if not loader.exists():
        raise FileNotFoundError("Cannot find the roster info.")
    loader.load()

    playerinfo = loader.get_data()
    playerinfo.drop_duplicates(subset="PERSON_ID", keep="first", inplace=True)

    seasonyear = int(request.args["Season"].split("-")[0])
    playerinfo["TO_YEAR"] = playerinfo["TO_YEAR"].astype(int)
    playerinfo["FROM_YEAR"] = playerinfo["FROM_YEAR"].astype(int)
    playerinfo = playerinfo[
        (playerinfo["TO_YEAR"] >= seasonyear) & (playerinfo["FROM_YEAR"] <= seasonyear)
    ].copy()
    playerinfo.sort_values(by="DISPLAY_FIRST_LAST", ascending=True, inplace=True)

    return json.dumps(playerinfo.to_dict(orient="records"))

@io_players.get("/players/info")
def player_info():
    """Retrieve player information."""
    loader = PlayerInfo(PlayerID=request.args["PlayerID"], output_dir=app.config["DATA_DIR"])
    if not loader.exists():
        raise FileNotFoundError("Cannot find the player information.")
    loader.load()
    info = loader.get_data("CommonPlayerInfo").to_dict(orient="records")[0]

    return json.dumps(info)

@io_players.get("/players/top")
def top_players():
    """Retrieve the top players for a given season."""

    gameratings = pd.read_csv(
        Path(app.config["DATA_DIR"], request.args["Season"], "impact-summary.csv"),
        sep="|",
        index_col=0
    )
    gameratings["IMPACT_sum"] = gameratings["IMPACT_sum"].round(3)
    gameratings["IMPACT_mean"] = gameratings["IMPACT_mean"].round(3)
    gameratings["IMPACT+_sum"] = gameratings["IMPACT+_sum"].round(3)
    gameratings["IMPACT+_mean"] = gameratings["IMPACT+_mean"].round(3)
    gameratings.sort_values(by="IMPACT+_mean", ascending=False, inplace=True)
    gameratings["RANK"] = np.arange(1, gameratings.shape[0] + 1)

    return json.dumps(gameratings.to_dict(orient="records"))

@io_players.get("/players/gamelog")
def player_gamelog():
    """Retrieve the player gamelog for a given season."""
    loader = PlayerGameLog(
        output_dir=Path(app.config["DATA_DIR"], request.args["Season"]),
        PlayerID=request.args["PlayerID"]
    )
    if not loader.exists():
        raise FileNotFoundError("Unable to get player gamelog.")
    loader.load()
    gamelog = loader.get_data()

    return json.dumps(gamelog.to_dict(orient="records"))
