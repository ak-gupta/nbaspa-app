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
                "Season": Season
            }
        })
    ])
    displayInfo = index.data
    d3.select("#playerFilter")
        .selectAll("select")
        .data(displayInfo)
        .enter()
        .insert("option")
        .attr("value", d => d.PERSON_ID)
        .text(d => d.DISPLAY_FIRST_LAST)
    // Create the default comparison
    topPlayers = top.data
    defaultSelect = topPlayers.map(obs => obs.PLAYER_ID).slice(0, 5);
    defaultFiltered = await Promise.all(
        defaultSelect.map(
            player => axios.get($SCRIPT_ROOT + "/players/time-series", {
                params: {
                    "PlayerID": player,
                    "Season": Season
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
                    "Season": Season
                }
            })
        )
    )
    newFiltered = newFiltered.map(obj => obj.data)
    playerDivs(playerList=newFiltered, info=displayInfo, tag="#playerList")
    compareChart(playerData=newFiltered, info=displayInfo, tag="#compareGraph")
}
