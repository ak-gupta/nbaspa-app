function drawGameChart(data, tag) {
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
            data,
            function (d) {
                return d.TIME
            }
        )
    )
    const y = d3.scaleLinear().domain([0, 1]).range([graphHeight, 0])
    const wProbAxis = d3.axisLeft(y).ticks(5).tickFormat(d3.format("~%"))
    const scoreMargin = d3.scaleLinear().range([graphHeight, 0])
    scoreMargin.domain(
        d3.extent(
            data,
            function (d) {
                return d.SCOREMARGIN
            }
        )
    )
    const marginAxis = d3.axisRight(scoreMargin)
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
    // Create the margin line
    var marginLine = d3.line().x(
        function (d) {
            return x(d.TIME)
        }
    ).y(
        function (d) {
            return scoreMargin(d.SCOREMARGIN)
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
    svg.append("g")
        .attr("transform", "translate(" + graphWidth + ")")
        .call(marginAxis)
    // Add the Win Probability line
    svg.append("path")
        .data([data])
        .attr("class", "line")
        .attr("d", winLine)
        .style("stroke", "blue")
        .attr("stroke-width", 2)
        .style("fill", "none")
    // Add the Margin line
    svg.append("path")
        .data([data])
        .attr("class", "line")
        .attr("d", marginLine)
        .style("stroke", "black")
        .attr("stroke-width", 1)
        .style("fill", "none")
}
