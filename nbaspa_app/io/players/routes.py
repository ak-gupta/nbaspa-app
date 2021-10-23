"""File I/O paths."""

from pathlib import Path

from flask import current_app as app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import numpy as np
import pandas as pd

from nbaspa.data.endpoints import AllPlayers, PlayerInfo, PlayerGameLog
from nbaspa.data.factory import NBADataFactory

from . import schemas as sc

io_players = Blueprint(
    "io_bp", __name__, url_prefix="/players", description="Load player data"
)
io_players.DEFAULT_PAGINATION_PARAMETERS["max_page_size"] = 250


@io_players.route("/time-series")
class TimeSeries(MethodView):
    """Load a season time-series for a given player."""

    @io_players.arguments(sc.PlayerQueryArgSchema, location="query")
    @io_players.response(200, sc.TimeSeriesOutput(many=True))
    def get(self, args):
        """Retrieve the season time-series."""
        if args["mode"] == "survival":
            fpath = Path(
                app.config["DATA_DIR"],
                args["Season"],
                "impact-timeseries",
                f"data_{args['PlayerID']}.csv"
            )
        elif args["mode"] == "survival-plus":
            fpath = Path(
                app.config["DATA_DIR"],
                args["Season"],
                "impact-plus-timeseries",
                f"data_{args['PlayerID']}.csv"
            )
        
        performances = pd.read_csv(fpath, sep="|", index_col=0, dtype={"GAME_ID": str})
        # TODO: Drop 0s and NAs
        performances = performances[performances["IMPACT"] != 0.0].copy()
        performances["IMPACT"] = performances["IMPACT"].round(3)
        # Parse game date
        performances["GAME_DATE_PARSED"] = pd.to_datetime(performances["GAME_DATE"])
        performances["DAY"] = performances["GAME_DATE_PARSED"].dt.day
        performances["MONTH"] = performances["GAME_DATE_PARSED"].dt.month
        performances["YEAR"] = performances["GAME_DATE_PARSED"].dt.year
        performances.sort_values(by="GAME_DATE_PARSED", ascending=True, inplace=True)

        columns = [
            "PLAYER_ID",
            "IMPACT",
            "SEASON",
            "GAME_ID",
            "GAME_DATE",
            "DAY",
            "MONTH",
            "YEAR"
        ]

        return performances[columns].to_dict(orient="records")

@io_players.route("/impact-profile")
class CareerProfile(MethodView):
    """Load a player impact profile."""

    @io_players.arguments(sc.PlayerQueryArgSchema, location="query")
    @io_players.response(200, sc.CareerProfileOutput(many=True))
    def get(self, args):
        """Load the player impact profile."""
        if args["mode"] == "survival":
            fglob = Path(app.config["DATA_DIR"]).glob(
                f"*/impact-timeseries/data_{args['PlayerID']}.csv"
            )
        elif args["mode"] == "survival-plus":
            fglob = Path(app.config["DATA_DIR"]).glob(
                f"*/impact-plus-timeseries/data_{args['PlayerID']}.csv"
            )
        
        performances = pd.concat(
            (pd.read_csv(fpath, sep="|", index_col=0, dtype={"GAME_ID": str}) for fpath in fglob),
            ignore_index=True
        )
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
                        "PlayerID": args["PlayerID"]
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
        agg = performances.groupby("SEASON")[["IMPACT", "PTS", "REB", "AST"]].mean().reset_index()
        agg["YEAR"] = agg["SEASON"].str.split("-", expand=True)[0]
        agg["YEAR"] = agg["YEAR"].astype(int)
        agg["IMPACT"] = agg["IMPACT"].round(3)
        agg["PTS"] = agg["PTS"].round(1)
        agg["REB"] = agg["REB"].round(1)
        agg["AST"] = agg["AST"].round(1)
        agg["PLAYER_ID"] = args["PlayerID"]

        return agg.to_dict(orient="records")

@io_players.route("/index")
class PlayerIndex(MethodView):
    """Load the player index."""

    @io_players.arguments(sc.IndexQueryArgSchema, location="query")
    @io_players.response(200, sc.PlayerIndexOutput(many=True))
    def get(self, args):
        """Load the player index for a given season."""
        loader = AllPlayers(
            output_dir=Path(app.config["DATA_DIR"], args["Season"]), Season=args["Season"]
        )
        if not loader.exists():
            abort(404, message="Unable to find roster information.")
        loader.load()
        # Parse
        playerinfo = loader.get_data()
        playerinfo.drop_duplicates(subset="PERSON_ID", keep="first", inplace=True)
        seasonyear = int(args["Season"].split("-")[0])
        playerinfo["TO_YEAR"] = playerinfo["TO_YEAR"].astype(int)
        playerinfo["FROM_YEAR"] = playerinfo["FROM_YEAR"].astype(int)
        playerinfo = playerinfo[
            (playerinfo["TO_YEAR"] >= seasonyear) & (playerinfo["FROM_YEAR"] <= seasonyear)
        ].copy()
        playerinfo.sort_values(by="DISPLAY_FIRST_LAST", ascending=True, inplace=True)

        return playerinfo.to_dict(orient="records")

@io_players.route("/info")
class CommonPlayerInfo(MethodView):
    """Load common player information."""

    @io_players.arguments(sc.PlayerQueryArgSchema, location="query")
    @io_players.response(200, sc.PlayerInfoOutput())
    def get(self, args):
        """Load common player information."""
        loader = PlayerInfo(PlayerID=args["PlayerID"], output_dir=app.config["DATA_DIR"])
        if not loader.exists():
            abort(404, message="Unable to find player information.")
        loader.load()

        return loader.get_data("CommonPlayerInfo").to_dict(orient="records")[0]

@io_players.route("/top")
class TopPlayers(MethodView):
    """Get the top players for a given season."""

    @io_players.arguments(sc.SummaryQueryArgsSchema, location="query")
    @io_players.response(200, sc.TopPlayersOutput(many=True))
    @io_players.paginate()
    def get(self, args, pagination_parameters):
        """Get the top players for a given season."""
        if args["mode"] == "survival":
            fpath = Path(
                app.config["DATA_DIR"], args["Season"], "impact-summary.csv"
            )
        elif args["mode"] == "survival-plus":
            fpath = Path(
                app.config["DATA_DIR"], args["Season"], "impact-plus-summary.csv"
            )
        
        gameratings = pd.read_csv(fpath, sep="|", index_col=0)
        gameratings["IMPACT_sum"] = gameratings["IMPACT_sum"].round(3)
        gameratings["IMPACT_mean"] = gameratings["IMPACT_mean"].round(3)

        if args["sortBy"] == "mean":
            gameratings.sort_values(by="IMPACT_mean", ascending=False, inplace=True)
        elif args["sortBy"] == "sum":
            gameratings.sort_values(by="IMPACT_sum", ascending=False, inplace=True)
        gameratings["RANK"] = np.arange(1, gameratings.shape[0] + 1)

        output = gameratings.to_dict(orient="records")
        pagination_parameters.item_count = len(output)
        
        return output[
            pagination_parameters.first_item:pagination_parameters.last_item
        ]

@io_players.route("/gamelog")
class Gamelog(MethodView):
    """Load the player gamelog."""

    @io_players.arguments(sc.PlayerQueryArgSchema, location="query")
    @io_players.response(200, sc.GamelogOutputSchema(many=True))
    def get(self, args):
        """Load the player gamelog."""
        loader = PlayerGameLog(
            output_dir=Path(app.config["DATA_DIR"], args["Season"]),
            PlayerID=args["PlayerID"]
        )
        if not loader.exists():
            abort(404, message="Unable to find player gamelog.")
        loader.load()
        gamelog = loader.get_data()

        return gamelog.to_dict(orient="records")
