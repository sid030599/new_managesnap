var add_btn = document.getElementsByClassName('add-btn')
var add_popup = document.getElementsByClassName('add-popup')[0]
var body = document.getElementsByClassName('body')[0]
var navi = document.getElementsByClassName("navigation")[0]
var cancel_btn1 = document.getElementsByClassName('cancel')[0]
var cancel_icon1 = document.getElementsByClassName('cancel-icon')[0]
var cancel_btn2 = document.getElementsByClassName('cancel')[1]
var cancel_icon2 = document.getElementsByClassName('cancel-icon')[1]
var panel = document.getElementsByClassName("side-panel-container")[0]
var edit_btn = document.getElementsByClassName("edit-btn")[0]
var edit_popup = document.getElementsByClassName("edit-popup")[0]

for(var i = 0; i < 2; i++)
{
    add_btn[i].addEventListener("click", () => {
        add_popup.style.display = "block"
        body.style.filter = "blur(10px)"
        navi.style.filter = "blur(10px)"
        panel.style.filter = "blur(10px)"
        document.body.style.position = "fixed"
    })
}

cancel_btn1.addEventListener("click", () => {
    add_popup.style.display = "none"
    body.style.filter = "none"
    navi.style.filter = "none"
    panel.style.filter = "none"
    document.body.style.position = "relative"
})
cancel_icon1.addEventListener("click", () => {
    add_popup.style.display = "none"
    body.style.filter = "none"
    navi.style.filter = "none"
    panel.style.filter = "none"
    document.body.style.position = "relative"
})

cancel_btn2.addEventListener("click", () => {
    edit_popup.style.display = "none"
    body.style.filter = "none"
    navi.style.filter = "none"
    panel.style.filter = "none"
    document.body.style.position = "relative"
})

cancel_icon2.addEventListener("click", () => {
    edit_popup.style.display = "none"
    body.style.filter = "none"
    navi.style.filter = "none"
    panel.style.filter = "none"
    document.body.style.position = "relative"
})

edit_btn.addEventListener("click", () => {
    edit_popup.style.display = "block"
    body.style.filter = "blur(10px)"
    navi.style.filter = "blur(10px)"
    panel.style.filter = "blur(10px)"
    document.body.style.position = "fixed"
})

document.getElementsByClassName('textarea')[0].defaultValue = "Announcement-1"
document.getElementsByClassName('textarea')[1].defaultValue = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Animi blanditiis hic atque quisquam consequatur numquam illo tenetur nostrum quibusdam impedit eligendi doloribus ea ab fugit iure veritatis, debitis perferendis sint provident deserunt ex reiciendis omnis deleniti!"
