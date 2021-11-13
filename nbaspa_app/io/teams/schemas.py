"""Marshmallow schemas for the team endpoints."""

from marshmallow import Schema, fields, validate

from nbaspa.data.endpoints.parameters import CURRENT_SEASON, ParameterValues

class TeamStatsQueryArgsSchema(Schema):
    Season = fields.String(default=CURRENT_SEASON)

class TeamQueryArgsSchema(Schema):
    Season = fields.String(default=CURRENT_SEASON)
    TeamID = fields.Int(required=True, validate=validate.OneOf(list(ParameterValues().TeamID)))

class TeamSummaryQueryArgsSchema(Schema):
    TeamID = fields.Int(required=True, validate=validate.OneOf(list(ParameterValues().TeamID)))

class TeamStatsOutputSchema(Schema):
    TEAM_NAME = fields.String()
    TEAM_ID = fields.Int()
    GP = fields.Int()
    W = fields.Int()
    L = fields.Int()
    W_PCT = fields.Float()
    MIN = fields.Int()
    E_OFF_RATING = fields.Float()
    E_DEF_RATING = fields.Float()
    E_NET_RATING = fields.Float()
    E_PACE = fields.Float()
    E_AST_RATIO = fields.Float()
    E_OREB_PCT = fields.Float()
    E_DREB_PCT = fields.Float()
    E_REB_PCT = fields.Float()
    E_TM_TOV_PCT = fields.Float()
    GP_RANK = fields.Int()
    W_RANK = fields.Int()
    L_RANK = fields.Int()
    W_PCT_RANK = fields.Int()
    MIN_RANK = fields.Int()
    E_OFF_RATING_RANK = fields.Int()
    E_DEF_RATING_RANK = fields.Int()
    E_NET_RATING_RANK = fields.Int()
    E_AST_RATIO_RANK = fields.Int()
    E_OREB_PCT_RANK = fields.Int()
    E_DREB_PCT_RANK = fields.Int()
    E_REB_PCT_RANK = fields.Int()
    E_TM_TOV_PCT_RANK = fields.Int()
    E_PACE_RANK = fields.Int()

class TeamSummaryOutputSchema(TeamStatsOutputSchema):
    SEASON = fields.String()

class TeamGameLogOutputSchema(Schema):
    Team_ID = fields.Int()
    Game_ID = fields.String()
    GAME_DATE = fields.String()
    MATCHUP = fields.String()
    WL = fields.String(validate=validate.OneOf(["W", "L"]))
    W = fields.Int()
    L = fields.Int()
    W_PCT = fields.Float()
    MIN = fields.Int()
    FGM = fields.Int()
    FGA = fields.Int()
    FG_PCT = fields.Float()
    FG3M = fields.Int()
    FG3A = fields.Int()
    FG3_PCT = fields.Float()
    FTM = fields.Int()
    FTA = fields.Int()
    FT_PCT = fields.Float()
    OREB = fields.Int()
    DREB = fields.Int()
    REB = fields.Int()
    AST = fields.Int()
    STL = fields.Int()
    BLK = fields.Int()
    TOV = fields.Int()
    PF = fields.Int()
    PTS = fields.Int()

class TeamRosterOutputSchema(Schema):
    TeamID = fields.Int()
    SEASON = fields.String()
    LeagueID = fields.String()
    PLAYER = fields.String()
    NICKNAME = fields.String()
    PLAYER_SLUG = fields.String()
    NUM = fields.String()
    POSITION = fields.String()
    HEIGHT = fields.String()
    WEIGHT = fields.String()
    BIRTH_DATE = fields.String()
    AGE = fields.Float()
    EXP = fields.String()
    SCHOOL = fields.String()
    PLAYER_ID = fields.Int()
