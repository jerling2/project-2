  function sortByName() {
    console.log("Sorting courses by name");

    // Get the sidebar sort button element
    var sortButton = document.querySelector('.sidebar-sort-by-button-input');

    // Get the current sort order class
    var currentSortOrder = sortButton.classList[1];

    // Toggle the sort order class
    if (currentSortOrder === 'sort-order-0') {
      sortButton.classList.remove('sort-order-0');
      sortButton.classList.add('sort-order-1');
    } else if (currentSortOrder === 'sort-order-1') {
      sortButton.classList.remove('sort-order-1');
      sortButton.classList.add('sort-order-2');
    } else if (currentSortOrder === 'sort-order-2') {
      sortButton.classList.remove('sort-order-2');
      sortButton.classList.add('sort-order-1');
    } else {
      // Default sort order
      sortButton.classList.add('sort-order-1');
    }

    // Get the updated sort order class
    var updatedSortOrder = sortButton.classList[1];

    var courseContainers = document.getElementsByClassName('course-container');
    var courseArray = Array.from(courseContainers);

    courseArray.sort(function(a, b) {
      var nameA = a.querySelector('.course-title-text').textContent.trim();
      var nameB = b.querySelector('.course-title-text').textContent.trim();

      // Determine the sorting order based on the updated sort order class
      if (updatedSortOrder === 'sort-order-1') {
        return nameA.localeCompare(nameB);
      } else if (updatedSortOrder === 'sort-order-2') {
        return nameB.localeCompare(nameA);
      } else {
        // Default sorting order (sort-order-0 or other unrecognized class)
        return nameA.localeCompare(nameB);
      }
    });

    var coursesContainer = document.getElementsByClassName('column-for-courses')[0];
    courseArray.forEach(function(course) {
      coursesContainer.appendChild(course);
    });
  }