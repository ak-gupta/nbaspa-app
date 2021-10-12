let topPlayers = null;
let defaultSelect = null;
let defaultFiltered = null;
let displayInfo = null;
loadPlayerIndex(
    Season=$SEASON,
    function (result) {
        // Set the displayInfo result
        displayInfo = result
        d3.select("#playerFilter")
            .selectAll("select")
            .data(result)
            .enter()
            .insert("option")
            .attr("value", d => d.PERSON_ID)
            .text(d => d.DISPLAY_FIRST_LAST)
    }
);
loadTopPlayers(
    Season=$SEASON,
    function (result) {
        topPlayers = result
        defaultSelect = result.map(obs => obs.PLAYER_ID).slice(0, 5);
        defaultFiltered = loadCompareData(playerList=defaultSelect, Season=$SEASON)
        compareChart(playerData=defaultFiltered, info=displayInfo, tag="#compareGraph")
        playerDivs(playerList=defaultFiltered, info=displayInfo, tag="#playerList")
    }
)


document.getElementById('submit').onclick = function() {
    var selected = [];
    for (var option of document.getElementById('playerFilter').options) {
        if (option.selected) {
            selected.push(parseInt(option.value));
        }
    }
    d3.select("#compareGraph").selectAll("svg").remove();
    d3.select("#compareGraph").selectAll("div").remove();
    d3.select("#playerList").selectAll("div").remove();
    var newFiltered = loadCompareData(
        playerList=selected,
        Season=$SEASON
    )
    playerDivs(playerList=newFiltered, info=displayInfo, tag="#playerList")
    compareChart(playerData=newFiltered, info=displayInfo, tag="#compareGraph")
}