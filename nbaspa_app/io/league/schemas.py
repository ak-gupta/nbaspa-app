"""Marshmallow schemas for the league endpoints."""

from marshmallow import Schema, fields, validate

from nbaspa.data.endpoints.parameters import CURRENT_SEASON


class SummaryQueryArgsSchema(Schema):
    Season = fields.String(default=CURRENT_SEASON)
    mode = fields.String(
        validate=validate.OneOf(["survival", "survival-plus"]), default="survival-plus"
    )
    sortBy = fields.String(validate=validate.OneOf(["sum", "mean"]))


class AwardOutputSchema(Schema):
    PLAYER_ID = fields.Int()
    IMPACT_mean = fields.Float()
    IMPACT_sum = fields.Float()
    RANK = fields.Int()
