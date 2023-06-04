// Get the view buttons list.
const view_button_node_list = document.querySelectorAll(".course-view-details-button");

/* Detect if the user clicks on 'view/hide details' and either display or hide the extra details. */
view_button_node_list.forEach(view_button => {
    view_button.addEventListener("click", () => {
        const course_container = view_button.parentNode.parentNode; // go to parents up.
        const details_container = course_container.querySelector(".course-shown-details-container");
        if (details_container.classList.contains("hidden")) {
            view_button.textContent = "hide details";
            details_container.classList.remove("hidden");
        } else {
            view_button.textContent = "view details";
            details_container.classList.add("hidden");
        }

        console.log(details_container);
    });
});