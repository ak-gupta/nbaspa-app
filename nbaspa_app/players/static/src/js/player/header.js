/**
 * @module Create a header div for all player summary pages
 */

/**
 * Create a header div object for each player page
 * @function headerDiv
 * @param {Object} info Basic player information
 * @param {string} tag The HTML tag to create the div in
 */
function headerDiv(info, tag) {
    var div = d3.select(tag).selectAll("div").data([info]).enter()
    var card = div.append("div")
        .classed("columns", true)
        .insert("div")
        .classed("column", true)
        .insert("div")
        .classed("card", true)
        .insert("div")
        .classed("media", true)
    card.insert("div")
        .classed("media-left", true)
        .insert("img")
        .attr(
            "src", d => `https://cdn.nba.com/headshots/nba/latest/260x190/${d.PERSON_ID}.png`
        )
        .attr("height", "100px")
    var divContent = card.insert("div")
        .classed("media-content", true)
    divContent.insert("p")
        .classed("title", true)
        .classed("is-2", true)
        .text(d => d.DISPLAY_FIRST_LAST)
    divContent.insert("p")
        .classed("subtitle", true)
        .classed("is-4", true)
        .text(d => `${d.POSITION} | ${d.JERSEY}`)
    var navContent = divContent.insert("nav")
        .classed("level", true)
        .classed("is-mobile", true)
    var country = navContent.insert("div")
        .classed("level-item", true)
        .classed("has-text-centered", true)
        .insert("div")
    country.insert("p")
        .classed("heading", true)
        .text("Country")
    country.insert("p")
        .classed("title", true)
        .text(d => d.COUNTRY)
    var school = navContent.insert("div")
        .classed("level-item", true)
        .classed("has-text-centered", true)
        .insert("div")
    school.insert("p")
        .classed("heading", true)
        .text("School")
    school.insert("p")
        .classed("title", true)
        .text(d => d.SCHOOL)
    var birthday = navContent.insert("div")
        .classed("level-item", true)
        .classed("has-text-centered", true)
        .insert("div")
    birthday.insert("p")
        .classed("heading", true)
        .text("Birthdate")
    birthday.insert("p")
        .classed("title", true)
        .text(d => d.BIRTHDATE)
}
