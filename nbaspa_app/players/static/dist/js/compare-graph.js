/**
 * Create a hover tooltip for the player season comparison
 * @function compareHover
 * @param {string} playerName The name of the player
 * @param {number} playerid The player identifier
 * @returns 
 */
function compareHover(playerName, playerid) {
    return `
        <div class="card">
            <div class="card-content">
                <div class="media">
                    <div class="media-left">
                        <img src="https://cdn.nba.com/headshots/nba/latest/260x190/${playerid}.png" width="75px">
                    </div>
                    <div class="media-content">
                        <p class="title is-4">${playerName}</p>
                    </div>
                </div>
            </div>
        </div>
    `
}

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

/**
 * Creates a D3.js visualization for comparing specific season performance
 * @function compareChart
 * @param {Array} lineData The time-series data
 * @param {Array} info The display information
 * @param {string} tag The HTML div ID for the graph
 */
function compareChart(lineData, info, tag) {
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
    // Re-arrange the data into groups by player
    var groupData = d3.groups(lineData, obs => obs.PLAYER_ID)
    console.log(
        d3.rollup(lineData, v => d3.mean(v, d => d.IMPACT_ADJ), e => e.PLAYER_ID, d => d.MONTH)
    )
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
        .data(groupData.map(obs => obs[1]))
        .join("path")
        .style("mix-blend-mode", "multiply")
        .attr("d", timeLine)
    // Add the colour fade-docus events
    path.on(
            "mouseenter",
            function (event) {
                d3.select(this)
                    .style("mix-blend-mode", null)
                    .attr("stroke", "hsl(0, 0%, 21%)")
                // Create a hover div
                const eventData = d3.select(this).data()[0]
                const displayName = info.filter(obs => obs[0] == eventData[0].PLAYER_ID)[0][1]
                div.transition()
                    .duration("100")
                    .style("opacity", 1)
                htmlhover = compareHover(
                    playerName=displayName, playerid=eventData[0].PLAYER_ID
                )
                div.html(htmlhover)
                    .style("left", (event.pageX + 10) + "px")
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
