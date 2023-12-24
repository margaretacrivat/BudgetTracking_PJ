function myFunction(){
    const navbarMenu = document.querySelector('.navbar-menu');
    navbarMenu.classList.toggle('show');

    document.querySelectorAll(".navbar-menu") .forEach(
    n=> n.addEventListener("click", () => {
    navbarMenu.classList.remove("show");
}))
}








