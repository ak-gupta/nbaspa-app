/**
 * @module mvp_list A module dedicated to updating the MVP List
 */

const mvp = new AwardList(Season, "/api/league/mvp", "/league/mvp/", mode, sortBy)
mvp.loadData(page)
mvp.updateList()
mvp.createPagination()

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
    window.location = $SCRIPT_ROOT + `/league/mvp/${Season}/1?mode=${mode}&sortBy=${sortBy}`
}
