/**
 * @module header The team layout header
 */

let infoGetter = new TeamNavigation();

infoGetter.loadData()
info = infoGetter.filterData(TeamID)

setTitle(info)
headerDiv(info, "#teamHeader")