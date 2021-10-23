/**
 * @module directory Code for generating the player directory and search
 */

async function loadDirectory() {
    index = await axios.get($SCRIPT_ROOT + "/api/players/index")
    indexData = index.data
}

async function searchDirectory() {
    // Get the input value
    let input = document.getElementById("playerSearch").value
    input = input.toLowerCase()

    if (input.length >= 3) {
        filterIndex = indexData.filter(obs => obs.DISPLAY_FIRST_LAST.toLowerCase().includes(input))
        d3.select("#playerList").selectAll("div").remove()
        var divs = d3.select("#playerList").selectAll("div").data(filterIndex).enter()
        var card = divs.append("div")
            .classed("columns", true)
            .insert("div")
            .classed("column", true)
            .insert("div")
            .classed("card", true)
            .insert("div")
            .classed("media", true)

        card.insert("div")
            .classed("media-left", true)
            .insert("a")
            .attr("href", d => $SCRIPT_ROOT + `/players/${d.PERSON_ID}`)
            .insert("img")
            .attr(
                "src", d => `https://cdn.nba.com/headshots/nba/latest/260x190/${d.PERSON_ID}.png`
            )
            .attr("width", "100px")
        var divContent = card.insert("div")
            .classed("media-content", true)
        divContent.insert("a")
            .attr("href", d => $SCRIPT_ROOT + `/players/${d.PERSON_ID}`)
            .insert("p")
            .classed("title", true)
            .classed("is-4", true)
            .text(obs => obs.DISPLAY_FIRST_LAST)
        divContent.insert("p")
            .classed("subtitle", true)
            .classed("is-4", true)
            .text(d => `${d.FROM_YEAR} - ${d.TO_YEAR}`)
    }
}
