
/**
 * Create a hover format
 * @function gameHover
 * @param {number} wprob The win probability
 * @param {number} margin The current scoring margin
 * @param {string} description The event description
 * @param {number} period The period of the game
 * @param {string} time The game time
 */
function gameHover(wprob, margin, description, period, time, playerid) {
    return `
        <table class="u-full-width">
            <tbody>
                <tr>
                    <td rowspan="4">
                        <img src="https://cdn.nba.com/headshots/nba/latest/260x190/${playerid}.png">
                    </td>
                    <td colspan="2" style="text-align: center;">${description}</td>
                </tr>
                <tr>
                    <td style="text-align: right;">Win Probability Change</td>
                    <td style="text-align: left;">${wprob}</td>
                </tr>
                    <td style="text-align: right;">Margin</td>
                    <td style="text-align: left;">${margin}</td>
                <tr>
                    <td style="text-align: right;">Time</td>
                    <td style="text-align: left;">Q${period} ${time}</td>
                </tr>
            </tbody>
        </table>
    `
}

/**
 * Creates a D3.js visualization for game win probability.
 * @function drawGameChart
 * @param {Array} lineData The event-level game data
 * @param {Array} dotData The top 5 events in the game
 * @param {string} tag The HTML div ID for the graph
 */

function drawGameChart(lineData, dotData, tag) {
    var margin = {
        top: 20,
        right: 20,
        bottom: 30,
        left: 40,
    }
    const graphWidth = 800 - margin.left - margin.right;
    const graphHeight = 400 - margin.top - margin.bottom;
    // Create axes
    var x = d3.scaleLinear().range([0, graphWidth])
    x.domain(
        d3.extent(
            lineData,
            function (d) {
                return d.TIME
            }
        )
    )
    const y = d3.scaleLinear().domain([0, 1]).range([graphHeight, 0])
    const percentFormat = d3.format("~%")
    const wProbAxis = d3.axisLeft(y).ticks(5).tickFormat(percentFormat)
    // Create the win probability line
    var winLine = d3.line().x(
        function (d) {
            return x(d.TIME)
        }
    ).y(
        function (d) {
            return y(d.WIN_PROB)
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
        .call(d3.axisBottom(x))
    svg.append("g").call(wProbAxis)
    // Add a horizontal line
    var horiz = [
        {TIME: 0, WIN_PROB: 0.5},
        {TIME: d3.max(lineData, d => d.TIME), WIN_PROB: 0.5}
    ]
    svg.append("path")
        .data([horiz])
        .attr("class", "line")
        .attr("d", winLine)
        .style("stroke", "black")
        .style("stroke-width", 0.5)
        .style("stroke-dasharray", ("2, 2"))
        .style("fill", "none")
    // Add the Win Probability line
    svg.append("path")
        .data([lineData])
        .attr("class", "line")
        .attr("d", winLine)
        .style("stroke", "black")
        .attr("stroke-width", 2)
        .style("fill", "none")
    // Add dots with mouseover
    var div = d3.select(tag).append("div")
        .attr("class", "tooltip")
        .style("opacity", 0)
    svg.selectAll("dot")
        .data(dotData)
        .enter()
        .append("circle")
        .attr("r", 4)
        .attr(
            "cx",
            function (d) {
                return x(d.TIME)
            }
        )
        .attr(
            "cy",
            function (d) {
                return y(d.SURV_PROB)
            }
        )
        .attr("stroke", "black")
        .attr("stroke-width", 1)
        .attr("fill", "#FFFFFF")
        .on(
            "mouseover",
            function (event, d) {
                d3.select(this)
                    .transition()
                    .duration("100")
                    .attr("r", 6)
                // Make the div appear
                div.transition()
                    .duration("100")
                    .style("opacity", 1)
                // Add data
                div.html(
                    gameHover(
                        wprob=percentFormat(d.SURV_PROB_CHANGE),
                        margin=d.SCOREMARGIN,
                        description=d.DESCRIPTION,
                        period=d.PERIOD,
                        time=d.PCTIMESTRING,
                        playerid=d.PLAYER1_ID
                    )
                )
            }
        )
        .on(
            "mouseout",
            function (event, d) {
                d3.select(this)
                    .transition()
                    .duration("200")
                    .attr("r", 4)
                // Make div disappear
                div.transition()
                    .duration("200")
                    .style("opacity", 0)
            }
        )
}
