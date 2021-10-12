/**
 * Load top players and their impact ratings for the season
 * @function loadTopPlayers
 * @param {string} Season The season of data to load
 * @param {function} callback A function to run on success.
 */
function loadTopPlayers(Season, callback) {
    $.ajax(
        {
            method: "GET",
            async: false,
            dataType: "json",
            url: $SCRIPT_ROOT + "/players/top",
            data: {
                "Season": Season
            },
            success: callback
        }
    )
}

/**
 * Load player information
 * @function loadPlayerIndex
 * @param {string} Season The season of data to load
 * @param {function} callback A function to run on success.
 */
function loadPlayerIndex(Season, callback) {
    $.ajax(
        {
            method: "GET",
            async: false,
            dataType: "json",
            url: $SCRIPT_ROOT + "/players/index",
            data: {
                "Season": Season
            },
            success: callback
        }
    )
}

/**
 * @function loadPlayerInfo The player information
 * @param {number} PlayerID The player identifier
 * @param {string} Season The season of data to load
 * @returns {Array} The player time-series
 */
function loadPlayerInfo(PlayerID, Season, callback) {
    $.ajax(
        {
            method: "GET",
            async: false,
            dataType: "json",
            url: $SCRIPT_ROOT + "/players/info",
            data: {
                "PlayerID": PlayerID,
                "Season": Season
            },
            success: callback
        }
    )
}

/**
 * Load player time-series from the I/O endpoints
 * @function loadPlayerTS
 * @param {number} PlayerID The player identifier
 * @param {string} Season The season of data to load
 * @returns {Array} The player time-series
 */
function loadPlayerTS(PlayerID, Season, callback) {
    $.ajax(
        {
            method: "GET",
            async: false,
            dataType: "json",
            url: $SCRIPT_ROOT + "/players/time-series",
            data: {
                "PlayerID": PlayerID,
                "Season": Season
            },
            success: callback,
        }
    )
}

/**
 * @function loadCompareData
 * @param {Array} playerList A list of player ID values
 * @param {string} Season The season of data to load
 * @returns {Array} An array of arrays. Each array will correspond to a single time-series
 */
function loadCompareData(playerList, Season) {
    var tmp = [];
    for (var i = 0; i < playerList.length; i++) {
        loadPlayerTS(
            PlayerID=playerList[i],
            Season=Season,
            callback=result => { tmp.push(result) }
        )
    }

    return tmp
}
