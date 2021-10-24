/**
 * @module base The core player-level header code
 */

class PlayerHeader {
    #infoRequest;

    constructor() {}

    set info(value) {
        this.#infoRequest = value
    }

    get info() {
        return this.#infoRequest
    }

    async loadData(PlayerID) {
        this.info = axios.get($SCRIPT_ROOT + "/api/players/info", {
            params: {
                "PlayerID": PlayerID
            }
        })
    }

    async populateHeader() {
        const basicInfo = await this.info
        headerDiv(basicInfo.data, "#playerHeader")
    }
}
