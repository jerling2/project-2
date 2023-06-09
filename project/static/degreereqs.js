/*
File: degreereqs.js
Description: Function to send course info to courses page for displaying
Creation Date: 6/9/23
Author: Sterling
*/

function redirect(node) {
  // Get the text from the text-data attribute of the clicked node
  var text = node.getAttribute("text-data");

  // Store the text in the localStorage
  localStorage.setItem("text", text);

  // Redirect to courses
  window.location.href= "/courses";
}