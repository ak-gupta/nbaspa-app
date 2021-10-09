/**
 * Creates a D3.js visualization for comparing specific season performance
 * @function compareChart
 * @param {Array} lineData The time-series data
 * @param {Array} players The list of players in the graph
 * @param {string} tag The HTML div ID for the graph
 */
function compareChart(lineData, players, tag) {
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
    lineData.forEach(
        function(obs) {
            obs.PARSED_DATE = parseDate(obs.GAME_DATE)
        }
    )
    // Create axes
    var x = d3.scaleTime().range([0, graphWidth])
    x.domain(d3.extent(lineData, obs => obs.PARSED_DATE))
    var y = d3.scaleLinear()
        .domain([0, d3.max(lineData, obs => obs.IMPACT_ADJ)])
        .range([graphHeight, 0])
    const dateFormat = d3.timeFormat("%b")
    const dateAxis = d3.axisBottom(x).tickFormat(dateFormat)
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
    // Re-arrange the data into groups by player
    var groupData = d3.groups(lineData, obs => obs.PLAYER_ID)
    svg.append("g")
        .attr("fill", "none")
        .attr("stroke", "hsl(0, 0%, 21%)")
        .attr("stroke-width", 1)
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .selectAll("path")
        .data(groupData.map(obs => obs[1]))
        .join("path")
        .style("mix-blend-mode", "multiply")
        .attr("d", timeLine)
        .on(
            "mouseenter",
            function () {
                d3.select(this)
                    .style("mix-blend-mode", null)
                    .attr("stroke", "hsl(0, 0%, 7%)")
                    .attr("stroke-width", 4)
            }
        )
        .on(
            "mouseleave",
            function () {
                d3.select(this)
                    .style("mix-blend-mode", "multiply")
                    .attr("stroke-width", 1)
                    .attr("stroke", null)
            }
        )
}
