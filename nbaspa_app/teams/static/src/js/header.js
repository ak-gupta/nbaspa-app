/**
 * @module header The team header
 */

async function setTitle(info) {
    info = await info

    document.title = info[0].TEAM_NAME
}

async function headerDiv(info, tag) {
    // Create the header
    info = await info
    var div = d3.select(tag).selectAll("div").data(info).enter()
    var navList = div.insert("nav")
        .classed("breadcrumb", true)
        .attr("aria-label", "breadcrumbs")
        .insert("ul")
    navList.append("li")
        .insert("a")
        .attr("href", $SCRIPT_ROOT + "/teams")
        .text("Teams")
    navList.append("li")
        .insert("a")
        .attr("href", obs => $SCRIPT_ROOT + `/teams/${obs.TEAM_ID}`)
        .text(obs => obs.TEAM_NAME)
    // Add navigation if we're on the season page
    if(typeof Season != 'undefined') {
        navList.append("li")
            .insert("a")
            .attr("href", obs => $SCRIPT_ROOT + `/teams/${obs.TEAM_ID}/${Season}`)
            .text(Season)
    }
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
