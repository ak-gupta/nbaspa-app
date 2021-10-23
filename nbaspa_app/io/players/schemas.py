"""Marshmallow schemas for the player endpoints."""

from marshmallow import Schema, fields, validate

from nbaspa.data.endpoints.parameters import CURRENT_SEASON

SEASON_FIELD = fields.String(default=CURRENT_SEASON)
SURV_MODE = fields.String(
    validate=validate.OneOf(["survival", "survival-plus"]), default="survival-plus"
)

class PlayerQueryArgSchema(Schema):
    PlayerID = fields.Int(required=True)
    Season = SEASON_FIELD
    mode = SURV_MODE

class IndexQueryArgSchema(Schema):
    Season = fields.String()

class SummaryQueryArgsSchema(Schema):
    Season = SEASON_FIELD
    mode = SURV_MODE
    sortBy = fields.String(
        validate=validate.OneOf(["sum", "mean"])
    )

class TimeSeriesOutput(Schema):
    PLAYER_ID = fields.Int()
    IMPACT = fields.Float()
    SEASON = fields.String()
    GAME_ID = fields.String()
    GAME_DATE = fields.String()
    DAY = fields.Int()
    MONTH = fields.Int()
    YEAR = fields.Int()

class CareerProfileOutput(Schema):
    PLAYER_ID = fields.Int()
    YEAR = fields.Int()
    IMPACT = fields.Float()
    PTS = fields.Float()
    REB = fields.Float()
    AST = fields.Float()
    SEASON = fields.String()

class PlayerIndexOutput(Schema):
    PERSON_ID = fields.Int()
    DISPLAY_LAST_COMMA_FIRST = fields.String()
    DISPLAY_FIRST_LAST = fields.String()
    ROSTERSTATUS = fields.Int()
    FROM_YEAR = fields.String()
    TO_YEAR = fields.String()
    PLAYERCODE = fields.String()
    PLAYER_SLUG = fields.String()
    TEAM_ID = fields.Int()
    TEAM_CITY = fields.String()
    TEAM_NAME = fields.String()
    TEAM_ABBREVIATION = fields.String()
    TEAM_CODE = fields.String()
    TEAM_SLUG = fields.String()
    GAMES_PLAYED_FLAG = fields.String()
    OTHERLEAGUE_EXPERIENCE_C = fields.String()

class PlayerInfoOutput(Schema):
    PERSON_ID = fields.Int()
    FIRST_NAME = fields.String()
    LAST_NAME = fields.String()
    DISPLAY_FIRST_LAST = fields.String()
    DISPLAY_LAST_COMMA_FIRST = fields.String()
    DISPLAY_FI_LAST = fields.String()
    PLAYER_SLUG = fields.String()
    BIRTHDATE = fields.String()
    SCHOOL = fields.String()
    COUNTRY = fields.String()
    LAST_AFFILIATION = fields.String()
    HEIGHT = fields.String()
    WEIGHT = fields.String()
    SEASON_EXP = fields.Int()
    JERSEY = fields.String()
    POSITION = fields.String()
    ROSTERSTATUS = fields.String()
    GAMES_PLAYED_CURRENT_SEASON_FLAG = fields.String()
    TEAM_ID = fields.Int()
    TEAM_NAME = fields.String()
    TEAM_ABBREVIATION = fields.String()
    TEAM_CODE = fields.String()
    TEAM_CITY = fields.String()
    PLAYERCODE = fields.String()
    FROM_YEAR = fields.Int()
    TO_YEAR = fields.Int()
    DLEAGUE_FLAG = fields.String()
    NBA_FLAG = fields.String()
    GAMES_PLAYED_FLAG = fields.String()
    DRAFT_YEAR = fields.String()
    DRAFT_ROUND = fields.String()
    DRAFT_NUMBER = fields.String()

class TopPlayersOutput(Schema):
    PLAYER_ID = fields.Int()
    IMPACT_mean = fields.Float()
    IMPACT_sum = fields.Float()
    RANK = fields.Int()

class GamelogOutputSchema(Schema):
    SEASON_ID = fields.String()
    Player_ID = fields.Int()
    Game_ID = fields.String()
    GAME_DATE = fields.String()
    MATCHUP = fields.String()
    WL = fields.String()
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
    PLUS_MINUS = fields.Int()
    VIDEO_AVAILABLE = fields.Int()
