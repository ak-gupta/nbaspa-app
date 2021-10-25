/**
 * @module core The code for combining I/O, graph, and div for player summary pages
 */

class PlayerSeasonSummary {
    #timeRequest;
    #gameRequest;
    #joinData;

    constructor() {}

    set time(value) {
        this.#timeRequest = value
    }

    get time() {
        return this.#timeRequest
    }

    set game(value) {
        this.#gameRequest = value
    }

    get game() {
        return this.#gameRequest
    }

    set data(value) {
        this.#joinData = value
    }

    get data() {
        return this.#joinData
    }

    async loadData(PlayerID, Season) {
        this.time = axios.get($SCRIPT_ROOT + "/api/players/time-series", {
            params: {
                "PlayerID": PlayerID,
                "Season": Season,
                "mode": "survival-plus"
            }
        })
        this.game = axios.get($SCRIPT_ROOT + "/api/players/gamelog", {
            params: {
                "PlayerID": PlayerID,
                "Season": Season
            }
        })
    }

    async parseData() {
        const timeReq = await this.time
        const timeData = timeReq.data
        const gameReq = await this.game
        const gameLog = gameReq.data
    
        this.data = timeData.map(
            obs => ({
                ...gameLog.find((game) => (game.Game_ID == obs.GAME_ID) && obs),
                ...obs
            })
        )
    }
    
    async draw(graphTag) {
        await this.parseData()
        drawTimeChart(
            this.data, "GAME_DATE", "%Y-%m-%dT%H:%M:%S", "%b", graphTag
        )
    }
    async headlineStats(divTag) {
        await this.parseData()
        var rawData = this.data
        rawData = rawData.filter(obs => obs.IMPACT !== 0.0)
        // Get the headlines
        const info = [
            {"field": "Impact", "value": d3.mean(rawData, obs => obs.IMPACT).toFixed(3)},
            {"field": "Points", "value": d3.mean(rawData, obs => obs.PTS).toFixed(1)},
            {"field": "Assists", "value": d3.mean(rawData, obs => obs.AST).toFixed(1)},
            {"field": "Rebounds", "value": d3.mean(rawData, obs => obs.REB).toFixed(1)}
        ]
        var divs = d3.select(divTag).selectAll("div").data(info).enter()
        var card = divs.append("div")
            .classed("columns", true)
            .insert("div")
            .classed("column", true)
            .insert("div")
            .classed("card", true)
        var nav = card.insert("nav")
            .classed("level", true)
            .classed("is-mobile", true)
            .insert("div")
            .classed("level-item", true)
            .classed("has-text-centered", true)
            .insert("div")
        nav.insert("p")
            .classed("heading", true)
            .text(d => d.field)
        nav.insert("p")
            .classed("title", true)
            .text(d => d.value)
    }
}

async function populateCareerGraph() {
    result = await axios.get($SCRIPT_ROOT + "/api/players/impact-profile", {
        params: {
            "PlayerID": PlayerID,
            "mode": "survival-plus"
        }
    })
    drawTimeChart(
        result.data,
        dateVar="YEAR",
        dateVarFormat="%Y",
        axisFormat="%Y",
        tag="#timeGraph"
    )
}
