/**
 * @module The javascript code for running the season summary page
 */

let searchList = []

let newSearch = new CompareSearch("compareSearch", "#searchResults", Season, "#compareGraph", "#playerList")
newSearch.loadData()
