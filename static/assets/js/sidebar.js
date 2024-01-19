// window.onload = function(){
//     const sidebar =  document.querySelector(".sidebar");
//     const toggle =  document.querySelector(".toggle");
//
//     toggle.addEventListener("click", function(){
//         sidebar.classList.toggle("open")
//         menuSidebarChange()
//     })
//
//     function menuSidebarChange(){
//         if(sidebar.classList.contains("open")) {
//             toggle.classList.replace("icon", "sidebar")
//         }
//         else{
//             toggle.classList.replace("sidebar", "icon")
//         }
//     }
// }







const toggle =  document.querySelector(".open-menu");
const sidebar =  document.querySelector(".sidebar");

toggle.addEventListener("click", ()=>{
    toggle.classList.toggle("active");
    sidebar.classList.toggle("active");
})

document.querySelectorAll('.sidebar').forEach(n=>n.
addEventListener("click", ()=>{
    toggle.classList.remove("active");
    sidebar.classList.remove("active");
}))

toggle.addEventListener("click", ()=>{
    sidebar.classList.toggle("close");
});


