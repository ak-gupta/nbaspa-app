/**
 * @module season The team season summary page
 */

let roster = new RosterList(TeamID, Season)
roster.loadData()
roster.addList("#rosterList")
