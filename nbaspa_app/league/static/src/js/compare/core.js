/**
 * @module core The code for combining I/O, graph, and div for the compare page
 */

class CompareSearch extends PlayerSearch {
    constructor(inputTag, divTag, Season, graphDiv, listDiv) {
        super(inputTag, divTag, "75px");

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

    addFooter(card) {
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
