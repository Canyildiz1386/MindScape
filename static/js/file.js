let sign = document.querySelector(".signin");
let login = document.querySelector("#loginform");

document.addEventListener("DOMContentLoaded", function() {

    if (signupOpen) {
        login.classList.add("hidden");
        sign.classList.remove("hidden");
    } else if (loginOpen) {
        sign.classList.add("hidden");
        login.classList.remove("hidden");
    }
    
});

function GoToSignin() {
    login.classList.add("hidden");
    sign.classList.remove("hidden");
}

function GoToLogin() {
    sign.classList.add("hidden");
    login.classList.remove("hidden");
}

