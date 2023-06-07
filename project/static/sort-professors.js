  function sortByName() {
    console.log("Sorting professors by name");
    // Get the sidebar sort button element
    var sortButton = document.querySelector('.sidebar-sort-by-button-input');

    var sidebar = document.querySelector('.sidebar-sort-by-order-input');

    // Get the current sort order class
    var currentSortOrder = sortButton.classList[1];

    // Toggle the sort order class
    // Sort order 0: Unsorted
    // Sort order 1: Sorted A-Z
    // Sort order 2: Sorted Z-A
    if (currentSortOrder === 'sort-order-0') {
      sortButton.classList.remove('sort-order-0');
      sortButton.classList.add('sort-order-1');
      sidebar.classList.remove('down_arrow');
      sidebar.classList.add('up_arrow');
    } else if (currentSortOrder === 'sort-order-1') {
      sortButton.classList.remove('sort-order-1');
      sortButton.classList.add('sort-order-2');
      sidebar.classList.remove('up_arrow');
      sidebar.classList.add('down_arrow');
    } else if (currentSortOrder === 'sort-order-2') {
      sortButton.classList.remove('sort-order-2');
      sortButton.classList.add('sort-order-1');
      sidebar.classList.remove('down_arrow');
      sidebar.classList.add('up_arrow');
    } else {
      // Default sort order
      sortButton.classList.add('sort-order-1');
      sidebar.classList.remove('down_arrow');
      sidebar.classList.add('up_arrow');
    }

    // Get the updated sort order class
    var updatedSortOrder = sortButton.classList[1];

    var professorContainers = document.getElementsByClassName('prof-container');
    var professorArray = Array.from(professorContainers);

    professorArray.sort(function(a, b) {
      var nameA = a.querySelector('.prof-name-text').textContent.trim();
      var nameB = b.querySelector('.prof-name-text').textContent.trim();

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

    var professorsContainer = document.getElementsByClassName('column-for-prof')[0];
    professorArray.forEach(function(professor) {
      professorsContainer.appendChild(professor);
    });
  }