/**
 * @module teamlist This module defines a way to pull and tile the teamlist
 */

class TeamNavigation {
    #teamRequest;

    constructor() {}

    set teams(value) {
        this.#teamRequest = value
    }

    get teams() {
        return this.#teamRequest
    }

    async loadData() {
        this.teams = axios.get($SCRIPT_ROOT + "/api/teams/stats")
    }

    async filterData(TeamID) {
        const teamReq = await this.teams
        const allData = teamReq.data

        return allData.filter(obs => obs.TEAM_ID == TeamID)
    }

    async tile(divTag) {
        const teamReq = await this.teams
        const teamData = teamReq.data
        // Slice the data and create the tiles with D3
        var i, j, tmp
        for (i = 0, j = teamData.length; i < j; i += 5) {
            tmp = teamData.slice(i, i + 5)
            console.log(tmp)
            var div = d3.select(divTag)
                .append("div")
                .classed("columns", true)
                .selectAll("div")
                .data(tmp)
                .enter()
            var card = div.insert("div")
                .classed("column", true)
                .classed("is-one-twelve", true)
                .insert("div")
                .classed("card", true)
            card.insert("div")
                .classed("card-image", true)
                .insert("figure")
                .classed("image", true)
                .classed("is-square", true)
                .insert("a")
                .attr(
                    "href", d => $SCRIPT_ROOT + `/teams/${d.TEAM_ID}`
                )
                .insert("img")
                .attr(
                    "src", d => `https://cdn.nba.com/logos/nba/${d.TEAM_ID}/primary/L/logo.svg`
                )
            card.insert("div")
                .classed("card-header", true)
                .insert("div")
                .classed("card-header-title", true)
                .text(d => d.TEAM_NAME)
        }
    }
}
