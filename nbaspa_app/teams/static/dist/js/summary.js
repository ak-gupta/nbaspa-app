/**
 * @module summary Team summary
 */

// Change the page based on the form input
formElement = document.getElementById("selectForm")
formElement.onsubmit = (e) => {
    e.preventDefault()
    params = new FormData(formElement)
    window.location = $SCRIPT_ROOT + `/teams/${TeamID}/${params.get("Season")}/gamelog`
}