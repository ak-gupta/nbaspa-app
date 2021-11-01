"""Marshmallow schemas for the league endpoints."""

from marshmallow import Schema, fields, validate

from nbaspa.data.endpoints.parameters import CURRENT_SEASON, SEASONS, ParameterValues

class StandingsQueryArgsSchema(Schema):
    Season = fields.String(
        validate=validate.OneOf(list(SEASONS.keys())),
        default=CURRENT_SEASON
    )
    Conference = fields.String(validate=validate.OneOf(["east", "west"]), required=True)

class StandingsOutputSchema(Schema):
    TEAM_ID = fields.String(
        validate=validate.OneOf(list(ParameterValues().TeamID))
    )
    TEAM = fields.String()
    G = fields.Int()
    W = fields.Int()
    L = fields.Int()
    W_PCT = fields.Float()

class SummaryQueryArgsSchema(Schema):
    Season = fields.String(default=CURRENT_SEASON)
    mode = fields.String(
        validate=validate.OneOf(["survival", "survival-plus"]), default="survival-plus"
    )
    sortBy = fields.String(
        validate=validate.OneOf(["sum", "mean"])
    )

class AwardOutputSchema(Schema):
    PLAYER_ID = fields.Int()
    IMPACT_mean = fields.Float()
    IMPACT_sum = fields.Float()
    RANK = fields.Int()
