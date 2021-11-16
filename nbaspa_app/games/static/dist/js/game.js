/**
 * @module game Create game assets
 */

// Populate the content
let game = new Game(GameDate, GameID)
game.loadData()
game.createHeader("#gameHeader", "#graphTitle")
game.topPerformers("#topPerformers")
game.draw("#gameGraph")
game.teamBoxscore("#teamBox")
game.playerBoxscore("#playerBox")
