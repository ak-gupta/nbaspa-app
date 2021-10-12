
function playerDivs(playerList, info, tag) {
    // Get average SPA+
    var grouped = playerList.map(
        obs =>  {
            return {
                PLAYER_ID: obs[0].PLAYER_ID,
                SEASON: obs[0].SEASON,
                IMPACT_ADJ: d3.mean(obs, d => d.IMPACT_ADJ),
            }
        }
    )
    var sorted = grouped.sort((a, b) => a.IMPACT_ADJ < b.IMPACT_ADJ)
    var divs = d3.select(tag).selectAll("div").data(sorted).enter();

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
        .attr("href", d => $SCRIPT_ROOT + `/players/${d.PLAYER_ID}/${d.SEASON}`)
        .insert("img")
        .attr(
            "src", d => `https://cdn.nba.com/headshots/nba/latest/260x190/${d.PLAYER_ID}.png`
        )
        .attr("width", "100px")

    var divContent = card.insert("div")
        .classed("media-content", true)
    divContent.insert("p")
        .classed("title", true)
        .classed("is-4", true)
        .text(d => info.filter(obs => obs.PERSON_ID == d.PLAYER_ID)[0].DISPLAY_FIRST_LAST)
    var navContent = divContent.insert("nav")
        .classed("level", true)
        .classed("is-mobile", true)
        .insert("div")
        .classed("level-item", true)
        .classed("has-text-centered", true)
        .insert("div")
    navContent.insert("p")
        .classed("heading", true)
        .text("Average SPA+")
    navContent.insert("p")
        .classed("title", true)
        .text(d => d.IMPACT_ADJ.toFixed(3))
}