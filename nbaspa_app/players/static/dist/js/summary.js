/**
 * @module The javascript code for running the season summary page
 */

// Set null variables for AJAX results
let topPlayers = null;
let defaultSelect = null;
let defaultFiltered = null;
let displayInfo = null;

// Populate the initial graph
populateCompare()
