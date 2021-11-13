/**
 * @module summary Team summary
 */

// Load team stats
let summary = new TeamSummary(TeamID);
summary.loadData()
summary.createTable("#summaryTable")
