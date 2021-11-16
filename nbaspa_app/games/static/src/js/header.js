/**
 * @module header The game header
 */

class GameHeader {
    #dateRequest;
    #boxRequest;

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
    }

    async createHeader(divTag) {
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
}
