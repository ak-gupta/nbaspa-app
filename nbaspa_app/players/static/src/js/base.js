/**
 * @module base The core player-level header code
 */

async function populatePlayerHeader() {
    basicInfo = await axios.get($SCRIPT_ROOT + "/players/info", {
        params: {
            "PlayerID": PlayerID
        }
    })
    headerDiv(info=basicInfo.data, tag="#playerHeader")    
}
