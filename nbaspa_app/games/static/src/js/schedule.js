/**
 * @module schedule Core code for rendering the schedule page
 */

class Schedule {
    #dateRequest

    constructor(gameDate, divTag) {
        this.gameDate = gameDate
        this.divTag = divTag
    }

    set games(value) {
        this.#dateRequest = value
    }

    get games() {
        return this.#dateRequest
    }

    async loadData() {
        this.games = axios.get($SCRIPT_ROOT + "/api/game/schedule", {
            params: {
                "GameDate": this.gameDate
            }
        }).catch(
            error => {
                if(error.response) {
                    var div = d3.select(this.divTag)
                        .selectAll("div")
                        .data([error.response.data])
                        .enter()
                        .insert("div")
                        .classed("notification", true)
                        .classed("is-danger", true)
                        .text(obs => obs.message)
                } else {
                    console.log("Error", error.message)
                }
            }
        )
    }

    async tile() {
        const req = await this.games
        const data = req.data
        // Slice the data and create tiles
        var i, j, tmp
        for(i = 0, j = data.length; i < j; i += 3) {
            tmp = data.slice(i, i + 3)
            // Create the divs
            var div = d3.select(this.divTag)
                .append("div")
                .classed("columns", true)
                .selectAll("div")
                .data(tmp)
                .enter()
            var card = div.insert("div")
                .classed("column", true)
                .classed("is-one-fourth", true)
                .insert("div")
                .classed("card", true)
            var cardContent = card.insert("div")
                .classed("card-content", true)
            // Home team
            var homeTeam = cardContent.append("div")
                .classed("media", true)
            homeTeam.append("div")
                .classed("media-left", true)
                .insert("a")
                .attr("href", obs => $SCRIPT_ROOT + `/teams/${obs.HOME_TEAM_ID}`)
                .insert("img")
                .attr("src", obs => `https://cdn.nba.com/logos/nba/${obs.HOME_TEAM_ID}/primary/L/logo.svg`)
                .attr("width", "50px")
            var homeContent = homeTeam.append("div")
                .classed("media-content", true)
            homeContent.append("p")
                .classed("title", true)
                .classed("is-4", true)
                .text(obs => obs.HOME_PTS)
            homeContent.append("p")
                .classed("subtitle", true)
                .classed("is-6", true)
                .text(obs => obs.HOME_ABBREVIATION)
            // Visiting team
            var visitorTeam = cardContent.append("div")
                .classed("media", true)
            visitorTeam.append("div")
                .classed("media-left", true)
                .insert("a")
                .attr("href", obs => $SCRIPT_ROOT + `/teams/${obs.VISITOR_TEAM_ID}`)
                .insert("img")
                .attr("src", obs => `https://cdn.nba.com/logos/nba/${obs.VISITOR_TEAM_ID}/primary/L/logo.svg`)
                .attr("width", "50px")
            var visitorContent = visitorTeam.append("div")
                .classed("media-content", true)
            visitorContent.append("p")
                .classed("title", true)
                .classed("is-4", true)
                .text(obs => obs.VISITOR_PTS)
            visitorContent.append("p")
                .classed("subtitle", true)
                .classed("is-6", true)
                .text(obs => obs.VISITOR_ABBREVIATION)
            // Footer
            card.insert("div")
                .classed("card-footer", true)
                .insert("a")
                .classed("card-footer-item", true)
                .attr("href", obs => {
                    const dateparts = this.gameDate.split("-")
                    return $SCRIPT_ROOT + `/games/${dateparts[2]}/${dateparts[1]}/${dateparts[0]}/${obs.GAME_ID}`
                })
                .text("Game Summary")
        }
    }
}