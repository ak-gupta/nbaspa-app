/**
 * @module core The code for combining I/O, graph, and div for the compare page
 */

class CompareSearch extends PlayerDirectory {
    constructor(inputTag, divTag, Season, graphDiv, listDiv) {
        super(inputTag, divTag);

        this.Season = Season;
        this.graphDiv = graphDiv;
        this.listDiv = listDiv;
    }

    async loadData() {
        this.index = axios.get($SCRIPT_ROOT + "/api/players/index", {
            params: {
                "Season": this.Season
            }
        })
    }

    addCards(divData) {
        var divs = d3.select(this.divTag).selectAll("div").data(divData).enter()
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
                "src", d => `https://cdn.nba.com/headshots/nba/latest/260x190/${d.PERSON_ID}.png`
            )
            .attr("width", "75px")
        var divContent = mediaContent.insert("div")
            .classed("media-content", true)
        divContent.insert("a")
            .insert("p")
            .classed("title", true)
            .classed("is-4", true)
            .text(obs => obs.DISPLAY_FIRST_LAST)
        // Add the link to the player summary
        card.insert("div")
            .classed("card-footer", true)
            .insert("a")
            .classed("card-footer-item", true)
            .attr("onclick", d => `onClick("${this.divTag}", "${this.inputTag}", "${d.DISPLAY_FIRST_LAST}", ${d.PERSON_ID})`)
            .text("Add to compare")
    }

    async updateCompareChart(mode) {
        d3.select(this.graphDiv).selectAll("svg").remove();
        d3.select(this.graphDiv).selectAll("div").remove();
        d3.select(this.listDiv).selectAll("div").remove();
        var newFiltered = await Promise.all(
            searchList.map(
                player => axios.get($SCRIPT_ROOT + "/api/players/time-series", {
                    params: {
                        "PlayerID": player.PERSON_ID,
                        "Season": Season,
                        "mode": mode
                    }
                })
            )
        )
        newFiltered = newFiltered.map(obj => obj.data)
        const indexRequest = await this.index
        const indexData = indexRequest.data
        playerDivs(newFiltered, indexData, this.listDiv)
        compareChart(newFiltered, indexData, this.graphDiv)
    }
}
