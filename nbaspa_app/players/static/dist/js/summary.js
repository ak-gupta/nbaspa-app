/**
 * @module The javascript code for running the season summary page
 */

 function onClick(divTag, inputTag, playerName, playerID) {
    // Clear the inputs
    d3.select(divTag).selectAll("div").remove()
    document.getElementById(inputTag).value = null
    // Add the player to the compare list
    searchList.push(
        {"DISPLAY_FIRST_LAST": playerName, "PERSON_ID": playerID}
    )
    d3.select("#currentCompare").selectAll("div").remove()
    var div = d3.select("#currentCompare").selectAll("div").data(searchList).enter()
    div.append("div")
        .attr("id", d => `compare-${d.PERSON_ID}`)
        .classed("notification", true)
        .classed("is-info", true)
        .text(d => d.DISPLAY_FIRST_LAST)
        .insert("button")
        .classed("delete", true)
        .attr("onclick", d => `removeFromCompare(${d.PERSON_ID})`)
}

function removeFromCompare(playerID) {
    searchList = searchList.filter(obs => obs.PERSON_ID !== playerID)
    d3.select(`#compare-${playerID}`).remove()
}

function clearCompare() {
    searchList = []
    d3.select("#currentCompare").selectAll("div").remove()
}


let searchList = []

let newSearch = new CompareSearch("compareSearch", "#searchResults", Season, "#compareGraph", "#playerList")
newSearch.loadData()

formElement = document.getElementById("graphForm")
formElement.onsubmit = (e) => {
    e.preventDefault()
    params = new FormData(formElement)
    // Parse the data
    if (params.get("mode") !== null) {
        mode = "survival"
    } else {
        mode = "survival-plus"
    }
    newSearch.updateCompareChart(mode)
}
