
var update_lesson_btn = document.getElementsByClassName('update-lesson-btn')

var update_lesson = document.getElementsByClassName('update-lesson')[0]
var body = document.getElementsByClassName('body')[0]
var navi = document.getElementsByClassName("navigation")[0]
var cancel_btn = document.getElementsByClassName('cancel')[0]
var cancel_icon = document.getElementsByClassName('cancel-icon')[0]
var panel = document.getElementsByClassName("side-panel-container")[0]

for(var i = 0; i < 2; i++)
{
    update_lesson_btn[i].addEventListener("click", () => {
        update_lesson.style.display = "block"
        body.style.filter = "blur(10px)"
        navi.style.filter = "blur(10px)"
        panel.style.filter = "blur(10px)"
        document.body.style.position = "fixed"
    })
}

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

