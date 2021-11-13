/**
 * @module header The team header
 */

async function headerDiv(info, tag) {
    // Create the header
    info = await info
    var div = d3.select(tag).selectAll("div").data(info).enter()
    var cols = div.append("div")
        .classed("columns", true)
        .classed("is-mobile", true)
        .classed("is-vcentered", true)
    cols.append("div")
        .classed("column", true)
        .insert("span")
        .classed("title", true)
        .text(obs => obs.TEAM_NAME)
    cols.append("div")
        .classed("column", true)
        .insert("div")
        .classed("is-pulled-right", true)
        .insert("figure")
        .classed("image", true)
        .classed("is-96x96", true)
        .insert("img")
        .attr(
            "src", obs => `https://cdn.nba.com/logos/nba/${obs.TEAM_ID}/primary/L/logo.svg`
        )
}
