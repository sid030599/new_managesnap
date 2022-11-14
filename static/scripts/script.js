var arrow = document.getElementById('arrow')
var heading = document.getElementsByClassName('panel-heading')[0]
var details = document.getElementsByClassName('details')[0]

heading.addEventListener("click", () => {
    if(arrow.className === "down")
    {
        arrow.className = "up"
        details.style.display = "none"
        arrow.style.content = "url('rsc/icons8-chevron-up-30.png')"
    }
    else
    {
        arrow.className = "down"
        details.style.display = "block"
        arrow.style.content = "url('rsc/icons8-chevron-down-30.png')"
    }

})

var menu = document.getElementById('menu')
var panel = document.getElementsByClassName('side-panel-container')[0]
var close = document.getElementById('close')
var body = document.getElementsByClassName("body")[0]
var navi = document.getElementsByClassName("navigation")[0]

menu.addEventListener("click", () => {
    panel.style.display = "block"
    body.style.filter = "blur(10px)"
    navi.style.filter = "blur(10px)"
    document.body.style.overflow = "hidden"
})

close.addEventListener("click", () => {
    panel.style.display = "none"
    body.style.filter = "none"
    navi.style.filter = "none"
    document.body.style.overflow = "scroll"
})

var noti = document.getElementsByClassName('noti-icon')[0]
var noti_list = document.getElementsByClassName('notification-list-container')[0]

var profile = document.getElementsByClassName('image')[0]
var prof_list = document.getElementsByClassName('profile-container')[0]

noti.addEventListener("click", () => {
    if(noti_list.className === "notification-list-container noti-notdisplay")
    {
        noti_list.className = "notification-list-container noti-display"
        // noti.style.content = "url('rsc/icons8-notification.gif')"
        prof_list.className = "profile-container prof-notdisplay"
        // profile.style.border = "none"
    }
    else
    {
        noti_list.className = "notification-list-container noti-notdisplay"
        // noti.style.content = "url('rsc/icons8-notification-48\ \(1\).png')"
    }
})

profile.addEventListener("click", () => {
    if(prof_list.className === "profile-container prof-notdisplay")
    {
        prof_list.className = "profile-container prof-display"
        // profile.style.border = "3px solid #ffc824"
        noti_list.className = "notification-list-container noti-notdisplay"
        // noti.style.content = "url('rsc/icons8-notification-48\ \(1\).png')"
    }
    else
    {
        prof_list.className = "profile-container prof-notdisplay"
        // profile.style.border = "none"
    }
})

body.addEventListener("click", () => {
    if(noti_list.className === "notification-list-container noti-display")
    {
        noti_list.className = "notification-list-container noti-notdisplay"
    }
    if(prof_list.className === "profile-container prof-display")
    {
        prof_list.className = "profile-container prof-notdisplay"
    }
})
