/**
 * @module awards Code for generating an awards list
 */

 class AwardList {
    #topRequest;
    #indexRequest;

    constructor(Season, endpoint, mode, sortBy) {
        this.Season = Season;
        this.endpoint = $SCRIPT_ROOT + endpoint;
        this.mode = mode;
        this.sortBy = sortBy;
    }

    set top(value) {
        this.#topRequest = value
    }

    get top() {
        return this.#topRequest
    }

    set index(value) {
        this.#indexRequest = value
    }

    get index() {
        return this.#indexRequest
    }

    /**
     * @function loadData Load the data from the API
     * @param {number} page The page number to load
     */
    async loadData(page=1) {
        this.index = axios.get($SCRIPT_ROOT + "/api/players/index")
        this.top = axios.get(this.endpoint, {
            params: {
                "Season": this.Season,
                "mode": this.mode,
                "sortBy": this.sortBy,
                "page": page
            }
        })
    }

    async updateList(averageHeader="Average Impact", totalHeader="Total Impact") {
        // Wait for the data
        const topRequest = await this.top
        var topPlayers = topRequest.data
        const playerInfo = await this.index
        var displayInfo = playerInfo.data
        // Remove any existing data
        d3.select("#playerList").selectAll("div").remove()
        // Create the new list
        var divs = d3.select("#playerList").selectAll("div").data(topPlayers).enter()

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
            .attr("href", d => $SCRIPT_ROOT + `/players/${d.PLAYER_ID}`)
            .insert("img")
            .attr(
                "src", d => `https://cdn.nba.com/headshots/nba/latest/260x190/${d.PLAYER_ID}.png`
            )
            .attr("width", "100px")
        var divContent = card.insert("div")
            .classed("media-content", true)
        divContent.insert("p")
            .classed("title", true)
            .classed("is-4", true)
            .text(d => displayInfo.filter(obs => obs.PERSON_ID == d.PLAYER_ID)[0].DISPLAY_FIRST_LAST)
        divContent.insert("p")
            .classed("subtitle", true)
            .classed("is-6", true)
            .text(d => `Rank: #${d.RANK}`)
        var nav = divContent.insert("nav")
            .classed("level", true)
            .classed("is-mobile", true)
        var avgContent = nav.insert("div")
            .classed("level-item", true)
            .classed("has-text-centered", true)
            .insert("div")
        avgContent.insert("p")
            .classed("heading", true)
            .text(averageHeader)
        avgContent.insert("p")
            .classed("title", true)
            .text(d => d.IMPACT_mean.toFixed(3))
        var sumContent = nav.insert("div")
            .classed("level-item", true)
            .classed("has-text-centered", true)
            .insert("div")
        sumContent.insert("p")
            .classed("heading", true)
            .text(totalHeader)
        sumContent.insert("p")
            .classed("title", true)
            .text(d => d.IMPACT_sum.toFixed(3))
    }

    /**
     * @function createPagination Create the pagination for navigation
     */
    async createPagination() {
        // Get the top request data so we know the number of pages
        const topRequest = await this.top
        const headers = JSON.parse(topRequest.headers["x-pagination"])
        // Remove existing navigation
        d3.select("#pagination").selectAll("ul").remove()
        d3.select("#pagination").selectAll("a").remove()
        var nav = d3.select("#pagination").selectAll("nav")
        var queryParams = "?mode=" + this.mode + "&sortBy=" + this.sortBy
        if ("previous_page" in headers) {
            nav.insert("a")
                .classed("pagination-previous", true)
                .attr(
                    "href",
                    this.endpoint + this.Season +  "/" + headers["previous_page"] + queryParams
                )
                .text("Previous")
        }
        if ("next_page" in headers) {
            nav.insert("a")
                .classed("pagination-next", true)
                .attr(
                    "href", this.endpoint + this.Season + "/" + headers["next_page"] + queryParams
                )
                .text("Next")
            var pageList = nav.insert("ul")
                .classed("pagination-list", true)
            pageList.insert("li")
                .insert("a")
                .classed("pagination-link", true)
                .attr("href", this.endpoint + this.Season + "/1" + queryParams)
                .text(1)
            if (!("previous_page" in headers) || (headers["page"] <= 3)) {
                pageList.insert("li")
                    .insert("a")
                    .classed("pagination-link", true)
                    .attr("href", this.endpoint + Season + "/2" + queryParams)
                    .text(2)
                pageList.insert("li")
                    .insert("a")
                    .classed("pagination-link", true)
                    .attr("href", this.endpoint + Season + "/3" + queryParams)
                    .text(3)
            } else {
                pageList.insert("li")
                    .insert("span")
                    .classed("pagination-ellipsis", true)
                    .text("...")
            }
            if ((headers["page"] > 3) && (headers["page"] < headers["total_pages"] - 1)) {
                pageList.insert("li")
                    .insert("a")
                    .classed("pagination-link", true)
                    .attr("href", this.endpoint + Season + "/" + headers["previous_page"] + queryParams)
                    .text(headers["previous_page"])
                pageList.insert("li")
                    .insert("a")
                    .classed("pagination-link", true)
                    .attr("href", this.endpoint + Season + "/" + headers["page"] + queryParams)
                    .text(headers["page"])
                pageList.insert("li")
                    .insert("a")
                    .classed("pagination-link", true)
                    .attr("href", this.endpoint + Season + "/" + headers["next_page"] + queryParams)
                    .text(headers["next_page"])
            }
            if (headers["page"] == headers["total_pages"] - 1) {
                pageList.insert("li")
                    .insert("a")
                    .classed("pagination-link", true)
                    .attr("href", this.endpoint + Season + "/" + headers["page"] + queryParams)
                    .text(headers["page"])
                pageList.insert("li")
                    .insert("a")
                    .classed("pagination-link", true)
                    .attr("href", this.endpoint + Season + "/" + headers["next_page"] + queryParams)
                    .text(headers["next_page"])                
            } else {
                pageList.insert("li")
                    .insert("span")
                    .classed("pagination-ellipsis", true)
                    .text("...")
                pageList.insert("li")
                    .insert("a")
                    .classed("pagination-link", true)
                    .attr(
                        "href", this.endpoint + Season + "/" + headers["total_pages"] + queryParams
                    )
                    .text(headers["total_pages"])
            }
        } else {
            var pageList = nav.insert("ul")
                .classed("pagination-list", true)
            pageList.insert("li")
                .insert("a")
                .classed("pagination-link", true)
                .attr("href", this.endpoint + Season + "/1" + queryParams)
                .text(1)
            pageList.insert("li")
                .insert("span")
                .classed("pagination-ellipsis", true)
                .text("...")
            pageList.insert("li")
                .insert("a")
                .classed("pagination-link", true)
                .attr("href", this.endpoint + Season + "/" + headers["previous_page"] + queryParams)
                .text(headers["previous_page"])
            pageList.insert("li")
                .insert("a")
                .classed("pagination-link", true)
                .attr("href", this.endpoint + Season + "/" + headers["page"] + queryParams)
                .text(headers["page"])
        }
    }
}
