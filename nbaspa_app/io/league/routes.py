"""League routes."""

from datetime import datetime, timedelta
from pathlib import Path

from flask import current_app as app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import numpy as np
import pandas as pd

from nbaspa.data.endpoints import AllPlayers
from nbaspa.data.endpoints.parameters import Season


from . import schemas as sc

io_league = Blueprint(
    "io_league", __name__, url_prefix="/api/league", description="Load league data"
)

@io_league.route("/mvp")
class TopPlayers(MethodView):
    """Get the top players for a given season."""

    @io_league.arguments(sc.SummaryQueryArgsSchema, location="query")
    @io_league.response(200, sc.AwardOutputSchema(many=True))
    @io_league.paginate()
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
        gameratings.dropna(inplace=True)
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
            pagination_parameters.first_item:(pagination_parameters.last_item + 1)
        ]

@io_league.route("/mip")
class MostImprovedPlayers(MethodView):
    """Get the most improved players for a given season."""

    @io_league.arguments(sc.SummaryQueryArgsSchema, location="query")
    @io_league.response(200, sc.AwardOutputSchema(many=True))
    @io_league.paginate()
    def get(self, args, pagination_parameters):
        """Get the most improved players for a given season.
        
        We will exclude all second year players from the list.
        """
        # Get the player index to filter out players that started last season
        loader = AllPlayers(
            output_dir=Path(app.config["DATA_DIR"], args["Season"]),
            filesystem=app.config["FILESYSTEM"],
            Season=args["Season"]
        )
        if not loader.exists():
            abort(404, message="Unable to find roster information.")
        loader.load()
        # Parse
        playerinfo = loader.get_data()
        playerinfo.drop_duplicates(subset="PERSON_ID", keep="first", inplace=True)
        playerinfo["TO_YEAR"] = playerinfo["TO_YEAR"].astype(int)
        playerinfo["FROM_YEAR"] = playerinfo["FROM_YEAR"].astype(int)
        seasonyear = Season(year=int(args["Season"].split("-")[0]))
        # Exclude second-year players
        playerinfo = playerinfo[
            (playerinfo["TO_YEAR"] >= seasonyear.year) & (playerinfo["FROM_YEAR"] < (seasonyear - 1).year)
        ].copy()

        # Load the current season impact ratings
        if args["mode"] == "survival":
            fpath = Path(
                app.config["DATA_DIR"], args["Season"], "impact-summary.csv"
            )
        elif args["mode"] == "survival-plus":
            fpath = Path(
                app.config["DATA_DIR"], args["Season"], "impact-plus-summary.csv"
            )
        
        current = pd.read_csv(fpath, sep="|", index_col=0)
        current.dropna(inplace=True)
        # Filter out second-year players
        current = current[current["PLAYER_ID"].isin(playerinfo["PERSON_ID"].values)].copy()
        current.set_index("PLAYER_ID", inplace=True)
        # Load previous season impact ratings
        previousyear = seasonyear - 1
        if args["mode"] == "survival":
            fpath = Path(
                app.config["DATA_DIR"], str(previousyear), "impact-summary.csv"
            )
        elif args["mode"] == "survival-plus":
            fpath = Path(
                app.config["DATA_DIR"], str(previousyear), "impact-plus-summary.csv"
            )
        previous = pd.read_csv(fpath, sep="|", index_col=0)
        previous.dropna(inplace=True)
        previous.set_index("PLAYER_ID", inplace=True)
        # Join and get the impact difference
        current["IMPACT_mean"] -= previous["IMPACT_mean"]
        current["IMPACT_sum"] -= previous["IMPACT_sum"]

        if args["sortBy"] == "mean":
            current.sort_values(by="IMPACT_mean", ascending=False, inplace=True)
        elif args["sortBy"] == "sum":
            current.sort_values(by="IMPACT_sum", ascending=False, inplace=True)
        current["RANK"] = np.arange(1, current.shape[0] + 1)

        output = current.reset_index().to_dict(orient="records")
        pagination_parameters.item_count = len(output)
        
        return output[
            pagination_parameters.first_item:(pagination_parameters.last_item + 1)
        ]


@io_league.route("/roty")
class RookiePlayers(MethodView):
    """Get the top performing rookies"""

    @io_league.arguments(sc.SummaryQueryArgsSchema, location="query")
    @io_league.response(200, sc.AwardOutputSchema(many=True))
    @io_league.paginate()
    def get(self, args, pagination_parameters):
        """Get the best performing rookies."""
        # Load the player index
        loader = AllPlayers(
            output_dir=Path(app.config["DATA_DIR"], args["Season"]),
            filesystem=app.config["FILESYSTEM"],
            Season=args["Season"]
        )
        if not loader.exists():
            abort(404, message="Unable to find roster information.")
        loader.load()
        # Parse
        playerinfo = loader.get_data()
        playerinfo.drop_duplicates(subset="PERSON_ID", keep="first", inplace=True)
        playerinfo["TO_YEAR"] = playerinfo["TO_YEAR"].astype(int)
        playerinfo["FROM_YEAR"] = playerinfo["FROM_YEAR"].astype(int)
        seasonyear = Season(year=int(args["Season"].split("-")[0]))
        # Only include players that started this year
        playerinfo = playerinfo[playerinfo["FROM_YEAR"] == seasonyear.year].copy()

        # Load impact ratings
        if args["mode"] == "survival":
            fpath = Path(
                app.config["DATA_DIR"], args["Season"], "impact-summary.csv"
            )
        elif args["mode"] == "survival-plus":
            fpath = Path(
                app.config["DATA_DIR"], args["Season"], "impact-plus-summary.csv"
            )

        ratings = pd.read_csv(fpath, sep="|", index_col=0)
        ratings.dropna(inplace=True)
        ratings = ratings[ratings["PLAYER_ID"].isin(playerinfo["PERSON_ID"].values)].copy()

        if args["sortBy"] == "mean":
            ratings.sort_values(by="IMPACT_mean", ascending=False, inplace=True)
        elif args["sortBy"] == "sum":
            ratings.sort_values(by="IMPACT_sum", ascending=False, inplace=True)
        ratings["RANK"] = np.arange(1, ratings.shape[0] + 1)

        output = ratings.to_dict(orient="records")
        pagination_parameters.item_count = len(output)
        
        return output[
            pagination_parameters.first_item:(pagination_parameters.last_item + 1)
        ]
