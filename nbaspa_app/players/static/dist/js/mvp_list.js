/**
 * @module mvp_list A module dedicated to updating the MVP List
 */

const mvp = new MVPList(Season, mode, sortBy)
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
        mvp.mode = "survival"
    } else {
        mvp.mode = "survival-plus"
    }
    if (params.get("sortBy") == "Average") {
        mvp.sortBy = "mean"
    } else {
        mvp.sortBy = "sum"
    }
    mvp.loadData(page)
    mvp.updateList()
    mvp.createPagination()
}
