const signUpButton = document.getElementById('sign_Up');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');


signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");
});


signUpButton.addEventListener('click', () => {
    container.classList.add("right-panel-active");
});
