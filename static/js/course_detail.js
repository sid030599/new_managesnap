// my-courses-container

const main_content = content.querySelector(".main-content");
let coll = main_content.getElementsByClassName("collapsible");
let i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle(".active");
    let Dowm = this.querySelector('.fa-angle-down');
    let Up = this.querySelector('.fa-angle-up');

    if(this.classList.contains('.active'))
    {
      Dowm.style.display = "none";
      Up.style.display = "inline";
    }
    else
    {
      Dowm.style.display = "inline";
      Up.style.display = "none";
    }

    let content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
      content.style.display = "none";
    } else {
      content.style.display = "block";
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}

const course_content_container = main_content.querySelector('.course-content-container');

const course_content = course_content_container.querySelector('.content');

const course_list = course_content.querySelector('.course-list');

const course_cards = course_list.getElementsByClassName('course-card');

console.log(course_cards);
for(i = 0; i < course_cards.length; i++)
{
  let progress_bar = course_cards[i].querySelector('.completed');

  let prog_count = course_cards[i].querySelector('.prog-count');

  let count = parseInt(prog_count.innerText);
  console.log(count);

  progress_bar.style.width = count + "%";
}
