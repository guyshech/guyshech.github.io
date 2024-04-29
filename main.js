
// Pre-loader

window.onload = () => {
    setTimeout(() => {
      document.querySelector("body").classList.add("display");
    }, 4000);
  };



// Hamburger 

document.querySelector(".hamburger-menu").addEventListener("click", () => {
    document.querySelector(".container").classList.toggle("change");
  });


//swiper 
