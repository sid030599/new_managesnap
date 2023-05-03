var default_btn = document.getElementsByClassName('default')[0]
var private_btn = document.getElementsByClassName('private')[0]
var public_btn = document.getElementsByClassName('public')[0]

var default_table = document.getElementsByClassName('default-table')[0]
var private_table = document.getElementsByClassName('private-table')[0]
var public_table = document.getElementsByClassName('public-table')[0]

var default_hov = document.getElementsByClassName('default')[0]
var private_hov = document.getElementsByClassName('private')[0]
var public_hov = document.getElementsByClassName('public')[0]

var default_table = document.getElementsByClassName('default-table')[0]
var private_table = document.getElementsByClassName('private-table')[0]
var public_table = document.getElementsByClassName('public-table')[0]

var default_tab = document.getElementsByClassName('default-tab')[0]
var private_tab = document.getElementsByClassName('private-tab')[0]
var public_tab = document.getElementsByClassName('public-tab')[0]

var view_btn_text = document.getElementById('view-type')
var view_btn = document.getElementsByClassName('view')[0]
var table = document.getElementsByClassName('table-view')[0]
var tabs = document.getElementsByClassName('tabs-view')[0]

var view_icon = document.getElementsByClassName('view-icon')[0]

var current = "default"

private_btn.addEventListener("click", () => {
    current = "private"
    //underline
    private_hov.className = "tab private current"
    public_hov.className = "tab public not-current"
    default_hov.className = "tab default not-current"
    //for tables
    if(view_btn_text.textContent === "Tab View")
    {
        private_table.style.display = "block"
        public_table.style.display = "none"
        default_table.style.display = "none"
        private_tab.style.display = "none"
        public_tab.style.display = "none"
        default_tab.style.display = "none"
    }
    //for list
    else
    {
        public_table.style.display = "none"
        default_table.style.display = "none"
        private_table.style.display = "none"
        private_tab.style.display = "grid"
        public_tab.style.display = "none"
        default_tab.style.display = "none"
    }
})

public_btn.addEventListener("click", () => {
    current = "public"
    //underline
    private_hov.className = "tab private not-current"
    public_hov.className = "tab public current"
    default_hov.className = "tab default not-current"
    //for tables
    if(view_btn_text.textContent === "Tab View")
    {
        private_table.style.display = "none"
        public_table.style.display = "block"
        default_table.style.display = "none"
        private_tab.style.display = "none"
        public_tab.style.display = "none"
        default_tab.style.display = "none"
    }
    //for list
    else
    {
        private_table.style.display = "none"
        public_table.style.display = "none"
        default_table.style.display = "none"
        private_tab.style.display = "none"
        public_tab.style.display = "grid"
        default_tab.style.display = "none"
    }
})

default_btn.addEventListener("click", () => {
    current = "default"
    //underline
    private_hov.className = "tab private not-current"
    public_hov.className = "tab public not-current"
    default_hov.className = "tab default current"
    //for tables
    if(view_btn_text.textContent === "Tab View")
    {
        private_table.style.display = "none"
        public_table.style.display = "none"
        default_table.style.display = "block"
        private_tab.style.display = "none"
        public_tab.style.display = "none"
        default_tab.style.display = "none"
    }
    //for list
    else
    {
        private_table.style.display = "none"
        public_table.style.display = "none"
        default_table.style.display = "none"
        private_tab.style.display = "none"
        public_tab.style.display = "none"
        default_tab.style.display = "grid"
    }
})

view_btn.addEventListener("click", () => {
    if(view_btn_text.textContent === "Tab View")
    {
        view_btn_text.innerHTML = "List View"
        view_icon.style.content = "url('rsc/icons8-list-24.png')"
        if(current === "default")
        {
            default_tab.style.display = "grid"
            default_table.style.display = "none"
        }
        if(current === "private")
        {
            private_tab.style.display = "grid"
            private_table.style.display = "none"
        }
        if(current === "public")
        {
            public_tab.style.display = "grid"
            public_table.style.display = "none"
        }
    }
    else
    {
        view_btn_text.innerHTML = "Tab View"
        view_icon.style.content = "url('rsc/icons8-table-24.png')"
        if(current === "default")
        {
            default_tab.style.display = "none"
            default_table.style.display = "block"
        }
        if(current === "private")
        {
            private_tab.style.display = "none"
            private_table.style.display = "block"
        }
        if(current === "public")
        {
            public_tab.style.display = "none"
            public_table.style.display = "block"
        }
    }
})



