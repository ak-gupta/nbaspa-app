/**
 * @module season Team season summary information
 */

class RosterList {
    #rosterRequest

    constructor(TeamID, Season) {
        this.TeamID = TeamID
        this.Season = Season
    }

    set roster(value) {
        this.#rosterRequest = value
    }

    get roster() {
        return this.#rosterRequest
    }

    async loadData() {
        this.roster = axios.get($SCRIPT_ROOT + "/api/teams/roster", {
            params: {
                "TeamID": this.TeamID,
                "Season": this.Season
            }
        })
    }

    async addList(divTag) {
        const req = await this.roster
        const divData = req.data
        // Add the cards
        var divs = d3.select(divTag).selectAll("div").data(divData).enter();
        var card = divs.append("div")
            .classed("columns", true)
            .insert("div")
            .classed("column", true)
            .insert("div")
            .classed("card", true)
        var mediaContent = card.insert("div")
            .classed("card-content", true)
            .classed("media", true)
        mediaContent.insert("div")
            .classed("media-left", true)
            .insert("a")
            .insert("img")
            .attr(
                "src", obs => `https://cdn.nba.com/headshots/nba/latest/260x190/${obs.PLAYER_ID}.png`
            )
            .attr("width", "75px")
        var divContent = mediaContent.insert("div")
            .classed("media-content", true)
        divContent.insert("a")
            .insert("p")
            .classed("title", true)
            .classed("is-4", true)
            .text(obs => obs.PLAYER)
        divContent.insert("p")
            .classed("subtitle", true)
            .classed("is-6", true)
            .text(obs => `Rank: #${obs.RANK}`)
        var nav = divContent.insert("nav")
            .classed("level", true)
            .classed("is-mobile", true)
        var avgContent = nav.insert("div")
            .classed("level-item", true)
            .classed("has-text-centered", true)
            .insert("div")
        avgContent.insert("p")
            .classed("heading", true)
            .text("Average impact")
        avgContent.insert("p")
            .classed("title", true)
            .text(d => d.IMPACT_mean.toFixed(3))
        var sumContent = nav.insert("div")
            .classed("level-item", true)
            .classed("has-text-centered", true)
            .insert("div")
        sumContent.insert("p")
            .classed("heading", true)
            .text("Total impact")
        sumContent.insert("p")
            .classed("title", true)
            .text(d => d.IMPACT_sum.toFixed(3))
        card.insert("div")
            .classed("card-footer", true)
            .insert("a")
            .classed("card-footer-item", true)
            .attr("href", obs => $SCRIPT_ROOT + `/players/${obs.PLAYER_ID}/${Season}`)
            .text("Season summary")
    }
}

class Gamelog {
    #logRequest;

    constructor(TeamID, Season) {
        this.TeamID = TeamID
        this.Season = Season
    }

    set gamelog(value) {
        this.#logRequest = value
    }

    get gamelog() {
        return this.#logRequest
    }

    async loadData() {
        this.gamelog = axios.get($SCRIPT_ROOT + "/api/teams/gamelog", {
            params: {
                "TeamID": this.TeamID,
                "Season": this.Season
            }
        })
    }

    async createTable(divTag) {
        const req = await this.gamelog
        const data = req.data
        // Create the table
        const columns = [
            {"value": "GAME_DATE", "alias": "Date"},
            {"value": "MATCHUP", "alias": "Matchup"},
            {"value": "WL", "alias": "Result"},
            {"value": "W", "alias": "Total wins"},
            {"value": "L", "alias": "Total losses"},
            {"value": "W_PCT", "alias": "Win percentage"}
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
                    return {
                        column: column.value,
                        value: row[column.value],
                        day: row.DAY,
                        month: row.MONTH,
                        year: row.YEAR,
                        gameid: row.Game_ID
                    };
		        });
		    })
            .enter()
            .append("td")
            .html(
                obs => {
                    if(obs.column == "MATCHUP") {
                        return `<a href="${$SCRIPT_ROOT}/games/${obs.day}/${obs.month}/${obs.year}/${obs.gameid}">${obs.value}</a>`
                    } else if(obs.column == "W_PCT") {
                        return Intl.NumberFormat("en-US", { style: "percent", maximumFractionDigits: 2}).format(obs.value)
                    } else {
                        return obs.value
                    }
                }
            )
    }
}
