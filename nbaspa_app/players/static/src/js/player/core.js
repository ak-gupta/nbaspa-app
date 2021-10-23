/**
 * @module core The code for combining I/O, graph, and div for player summary pages
 */

/**
 * @function populateSeasonGraph Load season impact data and graph it with boxscore information
 */
async function populateSeasonGraph() {
    timeData = await axios.get($SCRIPT_ROOT + "/players/time-series", {
        params: {
            "PlayerID": PlayerID,
            "Season": Season,
            "mode": "survival-plus"
        }
    })
    timeData = timeData.data
    gameLog = await axios.get($SCRIPT_ROOT + "/players/gamelog", {
        params: {
            "PlayerID": PlayerID,
            "Season": Season
        }
    })
    gameLog = gameLog.data
    graphData = timeData.map(
        obs => ({
            ...gameLog.find((game) => (game.Game_ID == obs.GAME_ID) && obs),
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

async function populateCareerGraph() {
    result = await axios.get($SCRIPT_ROOT + "/players/impact-profile", {
        params: {
            "PlayerID": PlayerID,
            "mode": "survival-plus"
        }
    })
    drawTimeChart(
        result.data,
        dateVar="YEAR",
        dateVarFormat="%Y",
        axisFormat="%Y",
        tag="#timeGraph"
    )
}
