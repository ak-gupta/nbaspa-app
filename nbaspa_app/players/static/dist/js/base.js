/**
 * @module Pull player index information and create a basic div.
 */

let basicInfo = null;

// Load the player info -- Birthdate, School, etc.
loadPlayerInfo(
    PlayerID=PlayerID,
    result => {
        basicInfo = result
        headerDiv(info=basicInfo, tag="#playerHeader")
    }
);
