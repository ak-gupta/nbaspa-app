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
        .attr("fill", "#FFFFFF")
}
