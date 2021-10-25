"""League routes."""

from datetime import datetime, timedelta
from pathlib import Path

from flask import current_app as app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from nbaspa.data.endpoints import Scoreboard
from nbaspa.data.endpoints.parameters import CURRENT_SEASON, SEASONS

from . import schemas as sc

io_league = Blueprint(
    "io_league", __name__, url_prefix="/api/league", description="Load league data"
)

@io_league.route("/standings")
class Standings(MethodView):
    """Load the latest available standings."""

    @io_league.arguments(sc.StandingsQueryArgsSchema, location="query")
    @io_league.response(200, sc.StandingsOutputSchema(many=True))
    def get(self, args):
        """Retrieve the standings."""
        if args["Season"] == CURRENT_SEASON:
            gdate = datetime.today().strftime("%m/%d/%Y")
        else:
            gdate = SEASONS[args["Season"]]["END"].strftime("%m/%d/%Y")
        
        loader = Scoreboard(
            output_dir=Path(app.config["DATA_DIR"], args["Season"]),
            Season=args["Season"],
            GameDate=gdate
        )
        if not loader.exists() and args["Season"] == CURRENT_SEASON:
            loader.params["GameDate"] = (datetime.today() - timedelta(days=1)).strftime("%m/%d/%Y")
        if not loader.exists():
            abort(404, message="Unable to load the scoreboard information.")
        # Get the conference standings
        loader.load()
        data = loader.get_data(
            "EastConfStandingsByDay" if args["Conference"] == "east" else "WestConfStandingsByDay"
        )

        return data[["TEAM_ID", "TEAM", "G", "W", "L", "W_PCT"]].to_dict(orient="records")
