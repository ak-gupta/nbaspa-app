/**
 * @module season The team season summary page
 */

let roster = new RosterList(TeamID, Season)
roster.loadData()
roster.addList("#rosterList")

let gamelog = new Gamelog(TeamID, Season)
gamelog.loadData()
gamelog.createTable("#gameLog")