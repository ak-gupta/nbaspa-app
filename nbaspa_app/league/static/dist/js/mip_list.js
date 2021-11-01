/**
 * @module mip_list A module dedicated to updating the MIP List
 */

 const mip = new AwardList(Season, "/api/league/mip", "/season/mip/", mode, sortBy)
 mip.loadData(page)
 mip.updateList(averageHeader="Impact lift per game", totalHeader="Total impact lift")
 mip.createPagination()
 
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
     window.location = $SCRIPT_ROOT + `/season/mip/${Season}/1?mode=${mode}&sortBy=${sortBy}`
 }
 