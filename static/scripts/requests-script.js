var default_btn = document.getElementsByClassName('default')[0]
var private_btn = document.getElementsByClassName('private')[0]
var public_btn = document.getElementsByClassName('public')[0]

var default_table = document.getElementsByClassName('default-table')[0]
var private_table = document.getElementsByClassName('private-table')[0]
var public_table = document.getElementsByClassName('public-table')[0]

var default_hov = document.getElementsByClassName('default')[0]
var private_hov = document.getElementsByClassName('private')[0]
var public_hov = document.getElementsByClassName('public')[0]

private_btn.addEventListener("click", () => {
    private_table.style.display = "block"
    default_table.style.display = "none"
    public_table.style.display = "none"
    //underline
    private_hov.className = "tab private current"
    public_hov.className = "tab public not-current"
    default_hov.className = "tab default not-current"
})

public_btn.addEventListener("click", () => {
    private_table.style.display = "none"
    default_table.style.display = "none"
    public_table.style.display = "block"
    //underline
    private_hov.className = "tab private not-current"
    public_hov.className = "tab public current"
    default_hov.className = "tab default not-current"
})

default_btn.addEventListener("click", () => {
    private_table.style.display = "none"
    default_table.style.display = "block"
    public_table.style.display = "none"
    //underline
    private_hov.className = "tab private not-current"
    public_hov.className = "tab public not-current"
    default_hov.className = "tab default current"
})