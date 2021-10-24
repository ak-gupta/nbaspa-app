/**
 * @module mvp_list A module dedicated to updating the MVP List
 */

const mvp = new MVPList()
mvp.loadData(Season=Season, mode="survival-plus", sortBy="mean", page=page)
mvp.updateList()
mvp.createPagination()

// Take in the form input and re-load data, update list
formElement = document.getElementById("sortForm")
formElement.onsubmit = (e) => {
    e.preventDefault()
    params = new FormData(formElement)
    // Parse the data
    if (params.get("mode") !== null) {
        var survMode = "survival"
    } else {
        var survMode = "survival-plus"
    }
    if (params.get("sortBy") == "Average") {
        var sortMethod = "mean"
    } else {
        var sortMethod = "sum"
    }
    mvp.loadData(Season=Season, mode=survMode, sortBy=sortMethod, page=page)
    mvp.updateList()
    mvp.createPagination()
}
