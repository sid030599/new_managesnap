const second_header = document.body.querySelector(".second-header");
const home = document.body.querySelector('.home');

const selectTab = element => {
    let c = second_header.querySelector('.nav-bar');
    let active = c.querySelector('.active');

    let visible = home.querySelector('.content-visible');
    let tabContent = document.getElementById(element.href.split('#')[1]);
    if (active) {
      active.classList.remove('active');
    }
    element.classList.add('active');
    if (visible) {
      visible.classList.remove('content-visible');
    }
    tabContent.classList.add('content-visible');
  }
  document.addEventListener('click', event => {
    if (event.target.matches('.tab-item a')) {
      selectTab(event.target);
    }
  }, false);