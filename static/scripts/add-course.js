var add_course_btn = document.getElementById('add-course-btn')
var add_course = document.getElementsByClassName('add-course')[0]
var body = document.getElementsByClassName('body')[0]
var navi = document.getElementsByClassName("navigation")[0]
var cancel_btn = document.getElementsByClassName('cancel')[0]
var cancel_icon = document.getElementsByClassName('cancel-icon')[0]
var panel = document.getElementsByClassName("side-panel-container")[0]

add_course_btn.addEventListener("click", () => {
    add_course.style.display = "block"
    body.style.filter = "blur(10px)"
    navi.style.filter = "blur(10px)"
    panel.style.filter = "blur(10px)"
    document.body.style.position = "fixed"
})

cancel_btn.addEventListener("click", () => {
    add_course.style.display = "none"
    body.style.filter = "none"
    navi.style.filter = "none"
    panel.style.filter = "none"
    document.body.style.position = "relative"
})

cancel_icon.addEventListener("click", () => {
    add_course.style.display = "none"
    body.style.filter = "none"
    navi.style.filter = "none"
    panel.style.filter = "none"
    document.body.style.position = "relative"
})