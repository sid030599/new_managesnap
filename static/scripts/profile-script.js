var personal_btn = document.getElementsByClassName('personal')[0]
var education_btn = document.getElementsByClassName('education')[0]
var experience_btn = document.getElementsByClassName('experience')[0]

var personal = document.getElementsByClassName('personal-info')[0]
var education = document.getElementsByClassName('education-info')[0]
var experience = document.getElementsByClassName('experience-info')[0]


education_btn.addEventListener("click", () => {
    education.style.display = "block"
    personal.style.display = "none"
    experience.style.display = "none"
    //underline
    education_btn .className = "tab education current"
    experience_btn.className = "tab experience not-current"
    personal_btn.className = "tab personal not-current"
})

experience_btn.addEventListener("click", () => {
    education.style.display = "none"
    personal.style.display = "none"
    experience.style.display = "block"
    //underline
    education_btn .className = "tab education not-current"
    experience_btn.className = "tab experience current"
    personal_btn.className = "tab personal not-current"
})

personal_btn.addEventListener("click", () => {
    education.style.display = "none"
    personal.style.display = "block"
    experience.style.display = "none"
    //underline
    education_btn .className = "tab education not-current"
    experience_btn.className = "tab experience not-current"
    personal_btn.className = "tab personal current"
})