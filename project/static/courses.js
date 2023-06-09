/*
File: courses.js
Description: Function to filter course results to show only the selected course from degreereqs page.
Creation Date: 6/9/23
Author: Sterling
*/


// Limit displayed courses to show selected course from degreereqs page.
document.addEventListener("DOMContentLoaded", function() {

  // Retrieve stored text from localStorage
  var storedText = localStorage.getItem("text");

  // Get search box element
  var inputElement = document.querySelector(".sidebar-search-text-input");

  if (storedText !== null) {

    // Set the value of the search box to the stored text
    inputElement.value = storedText;

    // Call search function (defined in courses in-line JavaScript)
    search();

    // Clear the stored text from localStorage
    localStorage.removeItem("text");
  }
});