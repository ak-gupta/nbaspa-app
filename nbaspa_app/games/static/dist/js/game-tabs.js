/**
 * Create tabs for the player boxscore data
 * @param {*} event 
 * @param {*} team 
 */
function openBox(event, team) {
    // Declare variables
    var i, tabcontent, tablinks;

    // Hide all tabs
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Remove active class
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" is-active", "");
    }

    // Show the current tab, and add an "active" class
    document.getElementById(team).style.display = "block";
    event.currentTarget.className += " is-active";
}
