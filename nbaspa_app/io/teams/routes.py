"""I/O paths for team information."""

from pathlib import Path

from flask import current_app as app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import pandas as pd

from nbaspa.data.endpoints import TeamStats, TeamGameLog, TeamRoster
from nbaspa.data.endpoints.parameters import CURRENT_SEASON
from nbaspa.data.factory import NBADataFactory

from . import schemas as sc

io_teams = Blueprint(
    "io_teams", __name__, url_prefix="/api/teams", description="Load team data"
)

@io_teams.route("/stats")
class AllTeamStats(MethodView):
    """Load all the team stats for a given season."""

    @io_teams.arguments(sc.TeamStatsQueryArgsSchema, location="query")
    @io_teams.response(200, sc.TeamStatsOutputSchema(many=True))
    def get(self, args):
        """Retrieve the team stats for a given season."""
        loader = TeamStats(
            output_dir=Path(app.config["DATA_DIR"], args.get("Season", CURRENT_SEASON)),
            filesystem=app.config["FILESYSTEM"],
            Season=args.get("Season", CURRENT_SEASON),
        )
        if not loader.exists():
            abort(404, message="Unable to retrieve team statistics.")
        loader.load()
        # Parse
        data = loader.get_data()
        data.sort_values(by="TEAM_NAME", ascending=True, inplace=True)

        return data.to_dict(orient="records")

@io_teams.route("/summary")
class Summary(MethodView):
    """Single team summary for every season."""

    @io_teams.arguments(sc.TeamSummaryQueryArgsSchema, location="query")
    @io_teams.response(200, sc.TeamSummaryOutputSchema(many=True))
    def get(self, args):
        """Retrieve a team's stats for every season."""
        calls = []
        for season in app.config["SEASONS"]:
            calls.append(
                (
                    "TeamStats",
                    {
                        "Season": season,
                        "output_dir": Path(app.config["DATA_DIR"], season),
                    }
                )
            )
        factory = NBADataFactory(calls=calls, filesystem=app.config["FILESYSTEM"])
        factory.load()
        allstats = factory.get_data()
        # Filter and return
        allstats = allstats[allstats["TEAM_ID"] == args["TeamID"]].copy()
        allstats["SEASON"] = list(app.config["SEASONS"].keys())

        return allstats.to_dict(orient="records")

@io_teams.route("/gamelog")
class GameLog(MethodView):
    """Load the team game log."""

    @io_teams.arguments(sc.TeamQueryArgsSchema, location="query")
    @io_teams.response(200, sc.TeamGameLogOutputSchema(many=True))
    def get(self, args):
        """Retrieve the team gamelog."""
        loader = TeamGameLog(
            output_dir=Path(app.config["DATA_DIR"], args.get("Season", CURRENT_SEASON)),
            filesystem=app.config["FILESYSTEM"],
            Season=args.get("Season", CURRENT_SEASON)
        )
        if not loader.exists():
            abort(404, message="Unable to find team gamelog.")
        loader.load()
        # Parse and return
        data = loader.get_data()
        # Filter to games within season download bounds
        data["PARSED"] = pd.to_datetime(data["GAME_DATE"], format="%b %d, %Y")
        bounds = app.config["SEASONS"][args.get("Season", CURRENT_SEASON)]
        data = data[
            (data["PARSED"] <= bounds["END"]) & (data["PARSED"] >= bounds["START"])
        ]

        return data.to_dict(orient="records")

@io_teams.route("/roster")
class Roster(MethodView):
    """Load the team roster."""

    @io_teams.arguments(sc.TeamQueryArgsSchema, location="query")
    @io_teams.response(200, sc.TeamRosterOutputSchema(many=True))
    def get(self, args):
        """Retrieve the team roster."""
        loader = TeamRoster(
            output_dir=Path(app.config["DATA_DIR"], args.get("Season", CURRENT_SEASON)),
            filesystem=app.config["FILESYSTEM"],
            Season=args.get("Season", CURRENT_SEASON)
        )
        if not loader.exists():
            abort(404, message="Unable to find the team roster.")
        loader.load()
        # Parse and return
        data = loader.get_data()

        return data.to_dict(orient="records")
