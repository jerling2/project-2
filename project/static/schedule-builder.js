const schedule_builder_container = document.querySelector(".schedule-builder-content-container");
const schedule_builder_overlay =  document.querySelector(".schedule-builder-content-overlay");
const class_buttons = document.querySelectorAll(".class-selection-class-container");
const time_text =  document.querySelectorAll(".time-text");
const classes = document.querySelectorAll(".schedule-builder-class-container");

const button_clicks = () => {
    class_buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            let class_name = btn.firstElementChild.innerHTML.split(' ').join('-');
            // Theres a bug here.
            let classes = document.querySelectorAll(`.${class_name}`);
            classes.forEach(cls => {
                if (cls.style.display == 'none') {
                    cls.style.display = 'flex';
                } else {
                    cls.style.display = 'none';
                }
            })
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

const get_cell_height = () => {
    let container_styles = window.getComputedStyle(schedule_builder_container);
    let cell_height = container_styles.gridTemplateRows.split(' ')[0];
    return parseFloat(cell_height);
}



window.addEventListener('resize', () => {
    resize_schedule_builder_overlay();
    position_time_text();
});
window.addEventListener('load', () => {
    resize_schedule_builder_overlay();
    position_time_text();
    button_clicks();
});