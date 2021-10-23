/**
 * @module core The code for combining I/O, graph, and div for the compare page
 */

/**
 * @function populateCompare Load the default comparison chart for a given season
 */
async function populateCompare() {
    const [index, top] = await Promise.all([
        axios.get($SCRIPT_ROOT + "/players/index", {
            params: {
                "Season": Season
            }
        }),
        axios.get($SCRIPT_ROOT + "/players/top", {
            params: {
                "Season": Season,
                "mode": "survival-plus",
                "sortBy": "mean",
                "page_size": 250
            }
        })
    ])
    displayInfo = index.data
    topPlayers = top.data
    // Reduce the displayInfo to the players we can graph
    allGraphable = topPlayers.map(obs => obs.PLAYER_ID)
    displayInfo = displayInfo.filter(obs => allGraphable.includes(obs.PERSON_ID))
    // Create the playerfilter select list
    d3.select("#playerFilter")
        .selectAll("select")
        .data(displayInfo)
        .enter()
        .insert("option")
        .attr("value", d => d.PERSON_ID)
        .text(d => d.DISPLAY_FIRST_LAST)
    // Create the default comparison
    defaultSelect = topPlayers.map(obs => obs.PLAYER_ID).slice(0, 5);
    defaultFiltered = await Promise.all(
        defaultSelect.map(
            player => axios.get($SCRIPT_ROOT + "/players/time-series", {
                params: {
                    "PlayerID": player,
                    "Season": Season,
                    "mode": "survival-plus"
                }
            })
        )
    )
    defaultFiltered = defaultFiltered.map(obj => obj.data)
    compareChart(playerData=defaultFiltered, info=displayInfo, tag="#compareGraph")
    playerDivs(playerList=defaultFiltered, info=displayInfo, tag="#playerList")
}

async function updateCompareChart() {
    var selected = [];
    for (var option of document.getElementById('playerFilter').options) {
        if (option.selected) {
            selected.push(parseInt(option.value));
        }
    }
    d3.select("#compareGraph").selectAll("svg").remove();
    d3.select("#compareGraph").selectAll("div").remove();
    d3.select("#playerList").selectAll("div").remove();
    var newFiltered = await Promise.all(
        selected.map(
            player => axios.get($SCRIPT_ROOT + "/players/time-series", {
                params: {
                    "PlayerID": player,
                    "Season": Season,
                    "mode": "survival-plus"
                }
            })
        )
    )
    newFiltered = newFiltered.map(obj => obj.data)
    playerDivs(playerList=newFiltered, info=displayInfo, tag="#playerList")
    compareChart(playerData=newFiltered, info=displayInfo, tag="#compareGraph")
}
