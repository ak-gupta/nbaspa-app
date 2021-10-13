/**
 * @module Create a season summary plot for a player season
 */

let timeData = null;
let gameLog = null;
let graphData = null;

// Load impact time-series
loadPlayerTS(
    PlayerID=PlayerID,
    Season=Season,
    result => {
        timeData = result
    }
);

// Load the gamelog
loadPlayerGamelog(
    PlayerID=PlayerID,
    Season=Season,
    result => {
        graphData = timeData.map(
            obs => ({
                ...result.find((game) => (game.Game_ID == obs.GAME_ID) && obs),
                ...obs
            })
        )
        drawTimeChart(
            graphData,
            dateVar="GAME_DATE",
            dateVarFormat="%Y-%m-%dT%H:%M:%S",
            axisFormat="%b",
            tag="#timeGraph"
        )
    }
)
