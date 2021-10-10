/**
 * Create a list of players in the current plot
 * @param {string} tag 
 * @param {Array} players The player data
 * @param {Array} info The display information
 */
function playerDivs(tag, players, info) {
    // group the data and get the average impact
    var grouped = d3.rollup(players, v => d3.mean(v, d => d.IMPACT_ADJ), e => e.PLAYER_ID)
    var sorted = new Map([...grouped.entries()].sort((a, b) => a[1] < b[1]))
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
        .attr("href", d => info.filter(obs => obs[0] == d[0])[0][2])
        .insert("img")
        .attr(
            "src", d => `https://cdn.nba.com/headshots/nba/latest/260x190/${d[0]}.png`
        )
        .attr("width", "100px")
    
    var divContent = card.insert("div")
        .classed("media-content", true)
    divContent.insert("p")
        .classed("title", true)
        .classed("is-4", true)
        .text(d => info.filter(obs => obs[0] == d[0])[0][1])
    var navContent = divContent.insert("nav")
        .classed("level", true)
        .classed("is-mobile", true)
        .insert("div")
        .classed("level-item", "has-text-centered")
        .insert("div")
    navContent.insert("p")
        .classed("heading", true)
        .text("Average SPA+")
    navContent.insert("p")
        .classed("title", true)
        .text(d => d[1].toFixed(3))
}
