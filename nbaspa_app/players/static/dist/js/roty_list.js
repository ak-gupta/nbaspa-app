/**
 * @module roty_list A module dedicated to updating the ROtY List
 */

const roty = new AwardList(Season, "/api/league/roty", mode, sortBy)
roty.loadData(page)
roty.updateList()
roty.createPagination()

// Take in the form input and re-load data, update list
formElement = document.getElementById("sortForm")
formElement.onsubmit = (e) => {
    e.preventDefault()
    params = new FormData(formElement)
    // Parse the data
    if (params.get("mode") !== null) {
        mode = "survival"
    } else {
        mode = "survival-plus"
    }
    if (params.get("sortBy") == "Average") {
        sortBy = "mean"
    } else {
        sortBy = "sum"
    }
    window.location = $SCRIPT_ROOT + `/season/roty/${Season}/1?mode=${mode}&sortBy=${sortBy}`
}
