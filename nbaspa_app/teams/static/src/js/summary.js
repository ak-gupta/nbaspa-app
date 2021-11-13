/**
 * @module summary The team summary page
 */

class TeamSummary {
    #statsRequest;

    constructor(TeamID) {
        this.TeamID = TeamID
    }

    set stats(value) {
        this.#statsRequest = value
    }

    get stats() {
        return this.#statsRequest
    }

    async loadData() {
        this.stats = axios.get($SCRIPT_ROOT + "/api/teams/summary", {
            params: {
                "TeamID": this.TeamID
            }
        })
    }

    async createTable(divTag) {
        const req = await this.stats
        const data = req.data
        // Create the table
        const columns = [
            {"value": "SEASON", "description": "", "alias": "Season"},
            {"value": "W", "description": "", "alias": "Wins"},
            {"value": "L", "description": "", "alias": "Losses"},
            {"value": "E_OFF_RATING", "description": "Points scored per 100 possessions", "alias": "Offensive rating"},
            {"value": "E_OFF_RATING_RANK", "description": "Offensive rating rank", "alias": "Rank"},
            {"value": "E_DEF_RATING", "description": "Points allowed per 100 possessions", "alias": "Defensive rating"},
            {"value": "E_DEF_RATING", "description": "Defensive rating rank", "alias": "Rank"},
            {"value": "E_NET_RATING", "description": "Net scoring margin per 100 possessions", "alias": "Net rating"},
            {"value": "E_NET_RATING_RANK", "description": "Net rating rank", "alias": "Rank"}
        ]
        var divs = d3.select(divTag).append("table")
            .classed("table", true)
            .classed("is-hoverable", true)
            .classed("has-background-light", true)
        var thead = divs.append("thead")
        var tbody = divs.append("tbody")
        // Create header row
        thead.append("tr")
            .selectAll("th")
            .data(columns)
            .enter()
            .append("th")
            .insert("abbr")
            .attr("title", obs => obs.description)
            .text(obs => obs.alias)
        // Create rows
        var rows = tbody.selectAll("tr")
            .data(data)
            .enter()
            .append("tr")

		// create a cell in each row for each column
		rows.selectAll("td")
            .data(row => {
                return columns.map(column => {
                    return {column: column.value, value: row[column.value]};
		        });
		    })
            .enter()
            .append("td")
            .html(
                obs => {
                    if(obs.column == "SEASON") {
                        return `<a href="${$SCRIPT_ROOT}/teams/${this.TeamID}/${obs.value}">${obs.value}</a>`
                    } else {
                        return obs.value
                    }
                }
            )
    }
}
