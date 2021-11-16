/**
 * @module core Core module for creating the game page content
 */

class Game {
    #dateRequest;
    #boxRequest;
    #winRequest;
    #momentRequest;

    constructor(gameDate, gameID) {
        this.gameDate = gameDate
        this.gameID = gameID
    }

    set games(value) {
        this.#dateRequest = value
    }

    get games() {
        return this.#dateRequest
    }

    set box(value) {
        this.#boxRequest = value
    }

    get box() {
        return this.#boxRequest
    }

    set line(value) {
        this.#winRequest = value
    }

    get line() {
        return this.#winRequest
    }

    set moments(value) {
        this.#momentRequest = value
    }

    get moments() {
        return this.#momentRequest
    }

    async loadData() {
        this.games = axios.get($SCRIPT_ROOT + "/api/game/schedule", {
            params: {
                "GameDate": this.gameDate
            }
        })
        this.box = axios.get($SCRIPT_ROOT + "/api/game/boxscore", {
            params: {
                "GameDate": this.gameDate,
                "GameID": this.gameID
            }
        })
        this.line = axios.get($SCRIPT_ROOT + "/api/game/playbyplay", {
            params: {
                "GameDate": this.gameDate,
                "GameID": this.gameID
            }
        })
        this.moments = axios.get($SCRIPT_ROOT + "/api/game/moments", {
            params: {
                "GameDate": this.gameDate,
                "GameID": this.gameID
            }
        })
    }

    async createHeader(divTag, headerTag) {
        const req = await this.games
        const allData = req.data
        const data = allData.filter(obs => obs.GAME_ID == this.gameID)
        // Create the header
        var div = d3.select(divTag).selectAll("div").data(data).enter()
        var nav = div.insert("nav").classed("level", true)
        nav.append("p")
            .classed("level-item", true)
            .classed("has-text-centered", true)
            .insert("a")
            .attr(
                "href", obs => $SCRIPT_ROOT + `/teams/${obs.VISITOR_TEAM_ID}`
            )
            .insert("img")
            .attr(
                "src", obs => `https://cdn.nba.com/logos/nba/${obs.VISITOR_TEAM_ID}/primary/L/logo.svg`
            )
            .attr("width", "100px")
        nav.append("div")
            .classed("level-item", true)
            .classed("has-text-centered", true)
            .insert("p")
            .classed("title", true)
            .text(obs => obs.VISITOR_PTS)
        nav.append("div")
            .classed("level-item", true)
            .classed("has-text-centered", true)
            .insert("p")
            .classed("title", true)
            .text(obs => obs.HOME_PTS)
        nav.append("p")
            .classed("level-item", true)
            .classed("has-text-centered", true)
            .insert("a")
            .attr(
                "href", obs => $SCRIPT_ROOT + `/teams/${obs.HOME_TEAM_ID}`
            )
            .insert("img")
            .attr(
                "src", obs => `https://cdn.nba.com/logos/nba/${obs.HOME_TEAM_ID}/primary/L/logo.svg`
            )
            .attr("width", "100px")
        // Set the page title
        document.title = `${data[0].VISITOR_ABBREVIATION} @ ${data[0].HOME_ABBREVIATION}`
        // Set a header title
        var title = d3.select(headerTag).selectAll("h4").data(data).enter()
        title.insert("h4")
            .classed("title", true)
            .classed("is-4", true)
            .text(obs => `${obs.HOME_ABBREVIATION} win probability over game time`)
    }

    async topPerformers(divTag) {
        const gameReq = await this.games
        const allGames = gameReq.data
        const gameInfo = allGames.filter(obs => obs.GAME_ID == this.gameID)
        // Get boxscore data
        const boxReq = await this.box
        const playerData = boxReq.data.PLAYER
        // Filter by team ID
        const homeLeader = playerData.filter(obs => obs.TEAM_ID == gameInfo[0].HOME_TEAM_ID)[0]
        const visitorLeader = playerData.filter(obs => obs.TEAM_ID == gameInfo[0].VISITOR_TEAM_ID)[0]
        // Add the cards
        var div = d3.select(divTag)
            .selectAll("div")
            .data([visitorLeader, homeLeader])
            .enter()
            .insert("div")
            .classed("column", true)
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
                "src", obs => `https://cdn.nba.com/headshots/nba/latest/260x190/${obs.PLAYER_ID}.png`
            )
            .attr("height", "100px")
        var divContent = mediaContent.insert("div")
            .classed("media-content", true)
        divContent.insert("p")
            .classed("title", true)
            .classed("is-4", true)
            .text(obs => obs.PLAYER_NAME)
        var nav = divContent.insert("nav")
            .classed("level", true)
            .classed("is-mobile", true)
        var spa = nav.insert("div")
            .classed("level-item", true)
            .classed("has-text-centered", true)
            .insert("div")
        spa.insert("p")
            .classed("heading", true)
            .text("Impact")
        spa.insert("p")
            .classed("title", true)
            .text(obs => obs.IMPACT.toFixed(3))
        var pts = nav.insert("div")
            .classed("level-item", true)
            .classed("has-text-centered", true)
            .insert("div")
        pts.insert("p")
            .classed("heading", true)
            .text("Points")
        pts.insert("p")
            .classed("title", true)
            .text(obs => obs.PTS)
        var ast = nav.insert("div")
            .classed("level-item", true)
            .classed("has-text-centered", true)
            .insert("div")
        ast.insert("p")
            .classed("heading", true)
            .text("Assists")
        ast.insert("p")
            .classed("title", true)
            .text(obs => obs.AST)
        var reb = nav.insert("div")
            .classed("level-item", true)
            .classed("has-text-centered", true)
            .insert("div")
        reb.insert("p")
            .classed("heading", true)
            .text("Rebounds")
        reb.insert("p")
            .classed("title", true)
            .text(obs => obs.REB)
    }

    async draw(graphTag) {
        const lineReq = await this.line
        const dotReq = await this.moments
        const lineData = lineReq.data
        const dotData = dotReq.data
        drawGameChart(lineData, dotData, graphTag)
    }

    async teamBoxscore(divTag) {
        const boxReq = await this.box
        const teamData = boxReq.data.TEAM
        // Create the aggregated fields
        teamData.map(row => {
            // Format percentages
            const fgpct = Intl.NumberFormat("en-US", { style: "percent", maximumFractionDigits: 2}).format(row.FG_PCT)
            row.FG = `${fgpct} (${row.FGM}/${row.FGA})`
            const fg3pct = Intl.NumberFormat("en-US", { style: "percent", maximumFractionDigits: 2}).format(row.FG3_PCT)
            row.FG3 = `${fg3pct} (${row.FG3M}/${row.FG3A})`
            const ftpct = Intl.NumberFormat("en-US", { style: "percent", maximumFractionDigits: 2}).format(row.FT_PCT)
            row.FT = `${ftpct} (${row.FTM}/${row.FTA})`
            // Team image
            row.IMG = `<img src="https://cdn.nba.com/logos/nba/${row.TEAM_ID}/primary/L/logo.svg" width="50px">`

            return row
        })
        // Create the table
        const columns = [
            {"value": "IMG", "description": "", "alias": ""},
            {"value": "FG", "description": "Field goals", "alias": "FG"},
            {"value": "FG3", "description": "3 point field goals", "alias": "FG3"},
            {"value": "FT", "description": "Free throws", "alias": "FT"},
            {"value": "REB", "description": "Rebounds", "alias": "REB"},
            {"value": "AST", "description": "Assists", "alias": "AST"},
            {"value": "STL", "description": "Steals", "alias": "STL"},
            {"value": "BLK", "description": "Blocks", "alias": "BLK"},
            {"value": "TO", "description": "Turnovers", "alias": "TO"}
        ]
        var divs = d3.select(divTag).append("table")
            .classed("table", true)
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
            .data(teamData)
            .enter()
            .append("tr")
        
        // Create a cell in each row for each column
        rows.selectAll("td")
            .data(row => {
                return columns.map(column => {
                    return {
                        column: column.value,
                        value: row[column.value]
                    }
                })
            })
            .enter()
            .append("td")
            .html(obs => obs.value)
    }

    async playerBoxscore(divTag) {
        const gameReq = await this.games
        const allGames = gameReq.data
        const gameInfo = allGames.filter(obs => obs.GAME_ID == this.gameID)
        // Get boxscore data
        const boxReq = await this.box
        const playerData = boxReq.data.PLAYER
        // Filter by team ID
        const homePlayers = playerData.filter(obs => obs.TEAM_ID == gameInfo[0].HOME_TEAM_ID)
        const visitorPlayers = playerData.filter(obs => obs.TEAM_ID == gameInfo[0].VISITOR_TEAM_ID)
        // Create the tables
        const columns = [
            {"value": "PLAYER_NAME", "description": "", "alias": ""},
            {"value": "MIN", "description": "Minutes played", "alias": "MIN"},
            {"value": "IMPACT", "description": "Impact rating", "alias": "IMPACT"},
            {"value": "FG", "description": "Field goals", "alias": "FG"},
            {"value": "FG3", "description": "3 point field goals", "alias": "FG3"},
            {"value": "FT", "description": "Free throws", "alias": "FT"},
            {"value": "PTS", "description": "Points", "alias": "PTS"},
            {"value": "REB", "description": "Rebounds", "alias": "REB"},
            {"value": "AST", "description": "Assists", "alias": "AST"},
            {"value": "STL", "description": "Steals", "alias": "STL"},
            {"value": "BLK", "description": "Blocks", "alias": "BLK"},
            {"value": "TO", "description": "Turnovers", "alias": "TO"}
        ]
        for(const x of [visitorPlayers, homePlayers]) {
            // Some data cleaning
            x.map(row => {
                row.IMPACT = row.IMPACT.toFixed(3)
                row.PLAYER_NAME = `<a href="${$SCRIPT_ROOT}/players/${row.PLAYER_ID}">${row.PLAYER_NAME}</a>`
                // Format percentages
                const fgpct = Intl.NumberFormat("en-US", { style: "percent", maximumFractionDigits: 2}).format(row.FG_PCT)
                row.FG = `${fgpct} (${row.FGM}/${row.FGA})`
                const fg3pct = Intl.NumberFormat("en-US", { style: "percent", maximumFractionDigits: 2}).format(row.FG3_PCT)
                row.FG3 = `${fg3pct} (${row.FG3M}/${row.FG3A})`
                const ftpct = Intl.NumberFormat("en-US", { style: "percent", maximumFractionDigits: 2}).format(row.FT_PCT)
                row.FT = `${ftpct} (${row.FTM}/${row.FTA})`

                return row
            })
            var div = d3.select(divTag).insert("div").classed("column", true)
            div.append("p")
                .classed("level-item", true)
                .classed("has-text-centered", true)
                .insert("img")
                .attr(
                    "src", `https://cdn.nba.com/logos/nba/${x[0].TEAM_ID}/primary/L/logo.svg`
                )
                .attr("width", "75px")
            var table = div.append("table")
                .classed("table", true)
                .classed("has-background-light", true)
            var thead = table.append("thead")
            var tbody = table.append("tbody")
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
                .data(x)
                .enter()
                .append("tr")
            // Create a cell in each row for each column
            rows.selectAll("td")
                .data(row => {
                    return columns.map(column => {
                        return {
                            column: column.value,
                            value: row[column.value]
                        }
                    })
                })
                .enter()
                .append("td")
                .html(obs => obs.value)
        }
    }
}
