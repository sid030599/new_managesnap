const menu = document.querySelector("#mobile-menu");
menu.addEventListener('click', function() {
  if(window.innerWidth <= 800)
  {
    menu.classList.toggle('is-active');
      sidebar.classList.toggle("close");
      sidebar.classList.toggle("clicked");

      home_section.classList.toggle('disable');
    }
})

const header = document.querySelector('.header');
const right_header = header.querySelector('.right-header');

const notification_container = right_header.querySelector('.notification-container');
const notify = notification_container.querySelector('.notify-icon');
const notifi_dropdown = notification_container.querySelector('.dropdown');


const profile_container = header.querySelector('.profile-container');
const profile_dropdown = profile_container.querySelector('.dropdown-content');

const profile = profile_container.querySelector('.profile-icon');

notify.addEventListener('click', function() {
    profile_dropdown.classList.remove('active');
    notifi_dropdown.classList.toggle('active');
})

profile.addEventListener('click', function() {
  notifi_dropdown.classList.remove('active');
  profile_dropdown.classList.toggle('active');
})


const content = document.querySelector('.content-container'),
sidebar = content.querySelector('nav'),
home_section = content.querySelector('.home'),
toggle = content.querySelector(".toggle"),
searchBtn = content.querySelector(".search-box"),
modeSwitch = content.querySelector(".toggle-switch"),
modeText = content.querySelector(".mode-text");
menubar = sidebar.querySelector(".menu-bar");


// For closing the notification and profile dropdown
content.addEventListener('click', function() {
  notifi_dropdown.classList.remove('active');
  profile_dropdown.classList.remove('active');
})

// delays in milliseconds
let showDelay = 600, hideDelay = 100;
// holding variables for timers
let menuEnterTimer, menuLeaveTimer;

menubar.addEventListener("mouseenter", function() {
    if(window.innerWidth > 800)
    {
      if(!sidebar.classList.contains("clicked")){
        clearTimeout(menuLeaveTimer);
        
        menuEnterTimer = setTimeout(function() {
            sidebar.classList.remove("close");
        }, showDelay);
      }
    }
});

menubar.addEventListener("mouseleave", () => {
    if(window.innerWidth > 800) 
    {
      if(!sidebar.classList.contains("clicked")) {
        clearTimeout(menuEnterTimer);

        menuLeaveTimer = setTimeout(function() {
          sidebar.classList.add("close");
        }, hideDelay);
      }
    }
});

toggle.addEventListener("click" , () =>{
    sidebar.classList.toggle("close");
    sidebar.classList.toggle("clicked");

    menu.classList.remove('is-active');
    home_section.classList.remove('disable');
});

modeSwitch.addEventListener("click" , () =>{
    content.classList.toggle("dark");
    document.body.classList.toggle("dark");
    
    if(content.classList.contains("dark")){
        modeText.innerText = "Light mode";
    }else{
        modeText.innerText = "Dark mode";
    }
});