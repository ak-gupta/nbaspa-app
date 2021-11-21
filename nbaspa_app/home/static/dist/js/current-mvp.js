/**
 * @module tracker The homepage MVP tracker
 */

const mvp = new AwardList(Season, "/api/league/mvp", "/league/mvp/", "survival-plus", "mean");
mvp.loadData()
mvp.updateList()
