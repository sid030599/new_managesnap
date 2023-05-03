var all = document.getElementsByClassName('all-table')[0]
var toptarget = document.getElementsByClassName('toptarget-table')[0]

var all_tab = document.getElementsByClassName('all')[0]
var toptarget_tab = document.getElementsByClassName('top-target')[0]

all_tab.addEventListener("click", () => {
    all.style.display = "block"
    toptarget.style.display = "none"
    //underline
    all_tab.className = "tab rel current"
    toptarget_tab.className = "tab dra not-current"
})
toptarget_tab.addEventListener("click", () => {
    all.style.display = "none"
    toptarget.style.display = "block"
    //underline
    all_tab.className = "tab rel not-current"
    toptarget_tab.className = "tab dra current"
})