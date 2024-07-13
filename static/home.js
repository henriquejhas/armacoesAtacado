// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

const elementos = document.querySelectorAll('.elemento-a-surgir');
const elementos2 = document.querySelectorAll('.elemento-a-surgir2');
const elementos3 = document.querySelectorAll('.elemento-a-surgir3');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('surgido');
    }
  });
}, { threshold: 0.4 }); // 0.5 significa que o elemento deve estar 50% visível

elementos.forEach(elemento => {
  observer.observe(elemento);
});

elementos2.forEach(elemento => {
  observer.observe(elemento);
});

elementos3.forEach(elemento => {
  observer.observe(elemento);
});

//novo site

function fecharMenu(){
    $("aside").css("width", "0px");
    $(".fundo").css("transition", "width 0s ease 0.5s, opacity 0.5s ease");
    $(".fundo").css("opacity", "0");
    $(".fundo").css("width", "0");
}

function login(){
    $("#id01").css("display", "block");
    fecharMenu();
}

$(".btAmburgue").click(function(){
    $("aside").css("width", "250px");
    $(".fundo").css("transition", "opacity 0.5s ease");
    $(".fundo").css("opacity", "1");
    $(".fundo").css("width", "100%");
});