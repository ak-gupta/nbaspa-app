/**
 * @module schedule The schedule page
 */

// Retrieve the schedule data
let currentGames = new Schedule(GameDate)
currentGames.loadData()
currentGames.tile("#gameList")

formElement = document.getElementById("datePicker")
formElement.onsubmit = (e) => {
    e.preventDefault()
    params = new FormData(formElement)
    dateinput = params.get("gamedate")
    datevals = dateinput.split("-")

    window.location = $SCRIPT_ROOT + `/games/${datevals[2]}/${datevals[1]}/${datevals[0]}`
}
