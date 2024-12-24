let usernameInput = document.getElementById('user');
let pwdInput = document.getElementById('pwd');
let loginBtn = document.getElementById('login-btn');

usernameInput.addEventListener('input', function() {
    onInputChange();
});

pwdInput.addEventListener('input', function() {
    onInputChange();
});

loginBtn.disabled = true;

function onInputChange() {
    if (usernameInput.value == '' || pwdInput.value == '') {
        loginBtn.disabled = true;
    } else {
        loginBtn.disabled = false;
    }
}