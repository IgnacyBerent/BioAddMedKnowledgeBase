const navbar_Button=document.querySelector(".navbar-button");
const navbar=document.querySelector(".navbar");
navbar_Button.addEventListener('click',()=>{
  if(!navbar.classList.contains("open")){
    navbar.classList.add("open");
    navbar_Button.classList.add("clicked");
  }else{
    navbar.classList.remove("open");
    navbar_Button.classList.remove("clicked");
  }
})
