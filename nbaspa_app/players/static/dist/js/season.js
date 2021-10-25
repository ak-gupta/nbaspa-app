/**
 * @module Create a season summary plot for a player season
 */

let summaryData = new PlayerSeasonSummary();
summaryData.loadData(PlayerID, Season)
summaryData.parseData()
summaryData.draw("#timeGraph")
summaryData.headlineStats("#headline")