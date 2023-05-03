var released = document.getElementsByClassName('released-container')[0]
var drafts = document.getElementsByClassName('drafts-container')[0]

var released_tab = document.getElementsByClassName('rel')[0]
var drafts_tab = document.getElementsByClassName('dra')[0]

released_tab.addEventListener("click", () => {
    released.style.display = "block"
    drafts.style.display = "none"
    //underline
    released_tab.className = "tab rel current"
    drafts_tab.className = "tab dra not-current"
})

drafts_tab.addEventListener("click", () => {
    released.style.display = "none"
    drafts.style.display = "block"
    //underline
    released_tab.className = "tab rel not-current"
    drafts_tab.className = "tab dra current"
})