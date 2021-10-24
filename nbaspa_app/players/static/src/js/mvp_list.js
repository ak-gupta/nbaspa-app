/**
 * @module mvp Code for generating a paginated list of the top players in a given season.
 */

class MVPList {
    #topRequest;
    #indexRequest;

    constructor() {}

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
     * @param {string} Season What season to retrieve
     * @param {string} mode Whether to retrieve the context-aware or context-unaware metrics
     * @param {string} sortBy Whether to sort by mean or sum
     * @param {number} page The page number to load
     */
    async loadData(Season, mode="survival-plus", sortBy="mean", page=1) {
        this.index = axios.get($SCRIPT_ROOT + "/api/players/index")
        this.top = axios.get($SCRIPT_ROOT + "/api/players/top", {
            params: {
                "Season": Season,
                "mode": mode,
                "sortBy": sortBy,
                "page": page
            }
        })
    }

    /**
     * @function updateList Update page
     */
    async updateList() {
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
            .text("Average Impact")
        avgContent.insert("p")
            .classed("title", true)
            .text(d => d.IMPACT_mean.toFixed(3))
        var sumContent = nav.insert("div")
            .classed("level-item", true)
            .classed("has-text-centered", true)
            .insert("div")
        sumContent.insert("p")
            .classed("heading", true)
            .text("Total Impact")
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
        console.log(headers)
        // Remove existing navigation
        d3.select("#pagination").selectAll("ul").remove()
        d3.select("#pagination").selectAll("a").remove()
        var nav = d3.select("#pagination").selectAll("nav")
        if ("previous_page" in headers) {
            nav.insert("a")
                .classed("pagination-previous", true)
                .attr(
                    "href", $SCRIPT_ROOT + "/players/top/" + Season +  "/" + headers["previous_page"]
                )
                .text("Previous")
        }
        if ("next_page" in headers) {
            nav.insert("a")
                .classed("pagination-next", true)
                .attr(
                    "href", $SCRIPT_ROOT + "/players/top/" + Season + "/" + headers["next_page"]
                )
                .text("Next")
            var pageList = nav.insert("ul")
                .classed("pagination-list", true)
            pageList.insert("li")
                .insert("a")
                .classed("pagination-link", true)
                .attr("href", $SCRIPT_ROOT + "/players/top/" + Season + "/1")
                .text(1)
            if (!("previous_page" in headers) || (headers["page"] <= 3)) {
                pageList.insert("li")
                    .insert("a")
                    .classed("pagination-link", true)
                    .attr("href", $SCRIPT_ROOT + "/players/top/" + Season + "/2")
                    .text(2)
                pageList.insert("li")
                    .insert("a")
                    .classed("pagination-link", true)
                    .attr("href", $SCRIPT_ROOT + "/players/top/" + Season + "/3")
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
                    .attr("href", $SCRIPT_ROOT + "/players/top/" + Season + "/" + headers["previous_page"])
                    .text(headers["previous_page"])
                pageList.insert("li")
                    .insert("a")
                    .classed("pagination-link", true)
                    .attr("href", $SCRIPT_ROOT + "/players/top/" + Season + "/" + headers["page"])
                    .text(headers["page"])
                pageList.insert("li")
                    .insert("a")
                    .classed("pagination-link", true)
                    .attr("href", $SCRIPT_ROOT + "/players/top/" + Season + "/" + headers["next_page"])
                    .text(headers["next_page"])
            }
            if (headers["page"] == headers["total_pages"] - 1) {
                pageList.insert("li")
                    .insert("a")
                    .classed("pagination-link", true)
                    .attr("href", $SCRIPT_ROOT + "/players/top/" + Season + "/" + headers["page"])
                    .text(headers["page"])
                pageList.insert("li")
                    .insert("a")
                    .classed("pagination-link", true)
                    .attr("href", $SCRIPT_ROOT + "/players/top/" + Season + "/" + headers["next_page"])
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
                        "href", $SCRIPT_ROOT + "/players/top/" + Season + "/" + headers["total_pages"]
                    )
                    .text(headers["total_pages"])
            }
        } else {
            var pageList = nav.insert("ul")
                .classed("pagination-list", true)
            pageList.insert("li")
                .insert("a")
                .classed("pagination-link", true)
                .attr("href", $SCRIPT_ROOT + "/players/top/" + Season + "/1")
                .text(1)
            pageList.insert("li")
                .insert("span")
                .classed("pagination-ellipsis", true)
                .text("...")
            pageList.insert("li")
                .insert("a")
                .classed("pagination-link", true)
                .attr("href", $SCRIPT_ROOT + "/players/top/" + Season + "/" + headers["previous_page"])
                .text(headers["previous_page"])
            pageList.insert("li")
                .insert("a")
                .classed("pagination-link", true)
                .attr("href", $SCRIPT_ROOT + "/players/top/" + Season + "/" + headers["page"])
                .text(headers["page"])
        }
    }
}
