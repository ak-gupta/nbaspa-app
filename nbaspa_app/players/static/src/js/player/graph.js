/**
 * Creates a D3.js visualization for player impact time-series.
 * @function drawTimeChart
 * @param {Array} lineData The time-series impact data
 * @param {string} dateVar The name of the date variable for the time-series
 * @param {string} dateVarFormat The format of the datetime variable
 * @param {string} axisFormat The date-time format for the x-axis
 * @param {string} tag The HTML div ID for the graph
 */
function drawTimeChart(lineData, dateVar, dateVarFormat, axisFormat, tag) {
    var margin = {
        top: 20,
        right: 20,
        bottom: 30,
        left: 40,
    }
    const graphWidth = 800 - margin.left - margin.right;
    const graphHeight = 400 - margin.top - margin.bottom;
    // Parse the date format
    var parseDate = d3.timeParse(dateVarFormat)
    lineData.forEach(
        function(d) {
            d[dateVar] = parseDate(d[dateVar])
        }
    )
    // Create axes
    var x = d3.scaleTime().range([0, graphWidth])
    x.domain(
        d3.extent(
            lineData,
            function (d) {
                return d[dateVar]
            }
        )
    )
    var y = d3.scaleLinear().domain(
        [
            0,
            d3.max(lineData, function(d) { return d.IMPACT_ADJ })
        ]
    ).range([graphHeight, 0])
    const dateFormat = d3.timeFormat(axisFormat)
    const dateAxis = d3.axisBottom(x).tickFormat(dateFormat)
    // Create the line
    var timeLine = d3.line().x(
        function (d) {
            return x(d[dateVar])
        }
    ).y(
        function (d) {
            return y(d.IMPACT_ADJ)
        }
    )
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
    svg.append("path")
        .data([lineData])
        .attr("class", "line")
        .attr("d", timeLine)
        .style("stroke", "hsl(0, 0%, 21%)")
        .attr("stroke-width", 2)
        .style("fill", "none")
    // Add dots
    maxImpact = d3.max(
        lineData,
        function(d) {
            return d.IMPACT_ADJ
        }
    )
    minImpact = d3.min(
        lineData,
        function(d) {
            return d.IMPACT_ADJ
        }
    )
    var div = d3.select(tag).append("div")
        .attr("class", "tooltip")
        .style("opacity", 0)
    svg.selectAll("dot")
        .data(lineData)
        .enter()
        .append("circle")
        .attr("r", 4)
        .attr(
            "cx",
            function(d) {
                return x(d[dateVar])
            }
        )
        .attr(
            "cy",
            function (d) {
                return y(d.IMPACT_ADJ)
            }
        )
        .attr("stroke", "black")
        .attr("stroke-width", 1)
        .attr(
            "fill",
            function (d) {
                if (d.IMPACT_ADJ == maxImpact) {
                    return "hsl(141, 53%, 53%)"
                } else if (d.IMPACT_ADJ == minImpact) {
                    return "hsl(348, 100%, 61%)"
                } else {
                    return "hsl(0, 0%, 100%)"
                }
            }
        )
        .on(
            "mouseover",
            function (event, d) {
                d3.select(this)
                    .transition()
                    .duration("100")
                // Make the div appear
                div.selectAll("div").remove()
                div.transition()
                    .duration("100")
                    .style("opacity", 1)
                // Add hover -- define a card
                var cardContent = div.insert("div")
                    .classed("card", true)
                // Add the image
                var mediaContent = cardContent.insert("div")
                    .classed("card-content", true)
                    .insert("div")
                    .classed("media", true)
                mediaContent.insert("div")
                    .classed("media-left", true)
                    .insert("img")
                    .attr(
                        "src", `https://cdn.nba.com/headshots/nba/latest/260x190/${d.PLAYER_ID}.png`
                    )
                    .attr("width", "75px")
                // Add SPA+
                var divContent = mediaContent.insert("div")
                    .classed("media-content", true)
                    .insert("nav")
                    .classed("level", true)
                    .classed("is-mobile", true)
                var spa = divContent.insert("div")
                    .classed("level-item", true)
                    .classed("has-text-centered", true)
                    .insert("div")
                spa.insert("p")
                    .classed("heading", true)
                    .text("SPA+")
                spa.insert("p")
                    .classed("title", true)
                    .text(d.IMPACT_ADJ)
                // Add PTS
                pts = divContent.insert("div")
                    .classed("level-item", true)
                    .classed("has-text-centered", true)
                    .insert("div")
                pts.insert("p")
                    .classed("heading", true)
                    .text("PTS")
                pts.insert("p")
                    .classed("title", true)
                    .text(d.PTS)
                // Add REB
                reb = divContent.insert("div")
                    .classed("level-item", true)
                    .classed("has-text-centered", true)
                    .insert("div")
                reb.insert("p")
                    .classed("heading", true)
                    .text("REB")
                reb.insert("p")
                    .classed("title", true)
                    .text(d.REB)
                // Add AST
                ast = divContent.insert("div")
                    .classed("level-item", true)
                    .classed("has-text-centered", true)
                    .insert("div")
                ast.insert("p")
                    .classed("heading", true)
                    .text("AST")
                ast.insert("p")
                    .classed("title", true)
                    .text(d.AST)
                
                // Add the footer
                cardContent.insert("div")
                    .classed("card-footer", true)
                    .insert("a")
                    .classed("card-footer-item", true)
                    .attr(
                        "href", $SCRIPT_ROOT + `/games/${d.DAY}/${d.MONTH}/${d.YEAR}/${d.GAME_ID}`
                    )
                    .text("Details")


                div.style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 15) + "px")
            }
        )
}
