/**
 * @module search Code for a generalized player search
 */

 class PlayerSearch {
    #indexRequest;

    constructor(inputTag, divTag, imgWidth) {
        this.inputTag = inputTag;
        this.divTag = divTag;
        this.imgWidth = imgWidth
    }

    set index(value) {
        this.#indexRequest = value
    }

    get index() {
        return this.#indexRequest
    }

    async loadData() {
        this.index = axios.get($SCRIPT_ROOT + "/api/players/index")
    }

    async search() {
        // Get the input value
        let input = document.getElementById(this.inputTag).value
        input = input.toLowerCase()

        if (input.length >= 3) {
            const indexRequest = await this.index
            const indexData = indexRequest.data
            var filterIndex = indexData.filter(obs => obs.DISPLAY_FIRST_LAST.toLowerCase().includes(input))
            d3.select(this.divTag).selectAll("div").remove()
            this.addCards(filterIndex)
        }
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
            .attr("width", this.imgWidth)
        var divContent = mediaContent.insert("div")
            .classed("media-content", true)
        divContent.insert("a")
            .insert("p")
            .classed("title", true)
            .classed("is-4", true)
            .text(obs => obs.DISPLAY_FIRST_LAST)
        divContent.insert("p")
            .classed("subtitle", true)
            .classed("is-6", true)
            .text(d => `${d.FROM_YEAR} - ${d.TO_YEAR}`)
        // Add the link to the player summary
        this.addFooter(card)
    }

    addFooter(card) {
        card.insert("div")
            .classed("card-footer", true)
            .insert("a")
            .classed("card-footer-item", true)
            .attr("href", d => $SCRIPT_ROOT + `/players/${d.PERSON_ID}`)
            .text("Career Overview")
    }
}
