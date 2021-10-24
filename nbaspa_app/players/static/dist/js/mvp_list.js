/**
 * @module mvp_list A module dedicated to updating the MVP List
 */

const mvp = new MVPList()
mvp.loadData(Season=Season, mode="survival-plus", sortBy="mean", page=page)
mvp.updateList()
mvp.createPagination()

// Take in the form input and re-load data, update list
