/**
 * @module Pull player index information and create a basic div.
 */

let basicInfo = null;

loadPlayerInfo(
    PlayerID=PlayerID,
    Season=Season,
    result => {
        basicInfo = result
        headerDiv(info=basicInfo, tag="#playerHeader")
    }
);
