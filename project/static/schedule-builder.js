/*
File: schedule-builder.js
Description: scripting for the schedule builder page.
Creation Date: 6/7/23
Author(s): Joseph
*/

const schedule_builder_container = document.querySelector(".schedule-builder-content-container");
const schedule_builder_overlay =  document.querySelector(".schedule-builder-content-overlay");
const class_selection_container = document.querySelector(".class-selection-classes-container");
const class_buttons = document.querySelectorAll(".class-selection-class-container");
const time_text =  document.querySelectorAll(".time-text");


/* This function hides or displays the courses on the schedule builder when the user clicks on the
   corresponding class button in the class selection bar.
 */
class_button_hide_or_display = () => {
    class_buttons.forEach(btn => {
        btn.addEventListener("click", () => {

            // Dynamically create the class name based on the innerHTML of the button.           
            let class_name = btn.firstElementChild.innerHTML;
            class_name = class_name.replace(/^\s+|\s+$/g, '');
            class_name = class_name.split(' ').join('-');
            console.log(`you clicked on ${class_name}`)
            // Get all the courses on the schedule builder with that class name.

            const classes = document.querySelectorAll(`.${class_name}`);

            // Iterate through each class element.
            classes.forEach(cls => {
                // display = '' is how javascript interprets display: none;
                if (cls.style.display == '') {
                    cls.style.display = 'flex';
                } else {
                    cls.style.display = '';
                }
            });
        });
    });
}


const position_time_text = () => {
    let cell_height = get_cell_height();
    let half_height = cell_height / 2;
    cell_height += 'px';
    half_height += half_height / 2;
    half_height += 'px';
    console.log(cell_height);
    time_text.forEach(function(element) {
        element.style.transform = `translateX(-3.25em) translateY(${half_height})`;
    });
};

const resize_schedule_builder_overlay = () => {
    let container_styles = window.getComputedStyle(schedule_builder_container);    
    schedule_builder_overlay.style.width = container_styles.width;
    schedule_builder_overlay.style.height = container_styles.height;
};

const resize_class_schedule_container = () => {
    let container_styles = window.getComputedStyle(schedule_builder_container);    
    // class_selection_container.style.width = container_styles.width;
    class_selection_container.style.height = container_styles.height;
}

const get_cell_height = () => {
    let container_styles = window.getComputedStyle(schedule_builder_container);
    let cell_height = container_styles.gridTemplateRows.split(' ')[0];
    return parseFloat(cell_height);
}



window.addEventListener('resize', () => {
    resize_schedule_builder_overlay();
    resize_class_schedule_container();
    position_time_text();
});

window.addEventListener('load', () => {
    resize_schedule_builder_overlay();
    resize_class_schedule_container();
    position_time_text();
    
    // add event listeners to the class buttons.
    class_button_hide_or_display();
});