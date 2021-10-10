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
