"""I/O paths for team information."""

from pathlib import Path

from flask import current_app as app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from nbaspa.data.endpoints import TeamStats, TeamGameLog, TeamRoster
from nbaspa.data.endpoints.parameters import CURRENT_SEASON

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
