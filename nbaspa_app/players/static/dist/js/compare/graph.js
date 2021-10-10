/**
 * Create a D3.js visualization for comparing season performance
 * @function compareChart
 * @param {Array} playerData An array of arrays. Each entry is a time-series.
 * @param {Array} info The display information
 * @param {string} tag The HTML div ID for the graph
 */
function compareChart(playerData, info, tag) {
    var margin = {
        top: 20,
        right: 20,
        bottom: 30,
        left: 40,
    }
    const graphWidth = 800 - margin.left - margin.right;
    const graphHeight = 400 - margin.top - margin.bottom;
    // Parse the date format
    var parseDate = d3.timeParse("%Y-%m-%dT%H:%M:%S")
    playerData.forEach(
        series => series.forEach(obs => obs.PARSED_DATE = parseDate(obs.GAME_DATE))
    )
    // Create axes
    var x = d3.scaleTime()
        .domain(
            [
                d3.min(playerData, series => d3.min(series, obs => obs.PARSED_DATE)),
                d3.max(playerData, series => d3.max(series, obs => obs.PARSED_DATE))
            ]
        )
        .range([0, graphWidth])
    const dateFormat = d3.timeFormat("%b")
    const dateAxis = d3.axisBottom(x).tickFormat(dateFormat)

    var y = d3.scaleLinear()
        .domain(
            [
                d3.least(
                    [0, d3.min(playerData, series => d3.min(series, obs => obs.IMPACT_ADJ))]
                ),
                d3.max(playerData, series => d3.max(series, obs => obs.IMPACT_ADJ))
            ]
        )
        .range([graphHeight, 0])

    // Create the line
    var timeLine = d3.line()
        .x(obs => x(obs.PARSED_DATE))
        .y(obs => y(obs.IMPACT_ADJ))
    
    // Create the SVG
    const svg = d3.select(tag).append("svg")
        .attr("width", graphWidth + margin.left + margin.right)
        .attr("height", graphHeight + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
    svg.append("g")
        .attr("transform", "translate(0," + graphHeight + ")")
        .call(dateAxis)
    svg.append("g").call(d3.axisLeft(y))

    // Add the line
    var div = d3.select(tag).append("div")
        .attr("class", "tooltip")
        .style("opacity", 0)
    const path = svg.append("g")
        .attr("fill", "none")
        .attr("stroke", "hsl(0, 0%, 21%)")
        .attr("stroke-width", 1.5)
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .selectAll("path")
        .data(playerData)
        .join("path")
        .style("mix-blend-mode", "multiply")
        .attr("d", timeLine)
    
    // Add fade/focus events
    path.on(
        "mouseenter",
        function (event) {
            d3.select(this)
                .style("mix-blend-mode", null)
                .attr("stroke", "hsl(0, 0%, 21%)")
            // Create a hover div
            const eventData = d3.select(this).data()[0]
            const displayName = info.filter(obs => obs.PERSON_ID == eventData[0].PLAYER_ID)[0].DISPLAY_FIRST_LAST
            div.selectAll("div").remove()
            div.transition()
                .duration("100")
                .style("opacity", 1)
            var cardContent = div.insert("div")
                .classed("card", true)
                .insert("div")
                .classed("media", true)
            cardContent.insert("div")
                .classed("media-left", true)
                .insert("img")
                .attr("src", `https://cdn.nba.com/headshots/nba/latest/260x190/${eventData[0].PLAYER_ID}.png`)
                .attr("width", "75px")
            cardContent.insert("div")
                .classed("media-content", true)
                .insert("p")
                .classed("title", true)
                .classed("is-4", true)
                .text(displayName)
            div.style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 15) + "px")
        }
    )
    .on(
        "mouseleave",
        function () {
            d3.select(this)
                .style("mix-blend-mode", "multiply")
                .attr("stroke", null)
        }
    )
    .on(
        "mousemove",
        function (event) {
            path.attr("stroke", "hsl(0, 0%, 86%)")
        }
    )
}