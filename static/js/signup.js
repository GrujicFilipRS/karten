let usernameInput = document.getElementById('user');
let pwdInput = document.getElementById('pwd');
let loginBtn = document.getElementById('login-btn');
let pwdInputConf = document.getElementById('pwd_conf');

usernameInput.addEventListener('input', function() {
    onInputChange();
});

pwdInput.addEventListener('input', function() {
    onInputChange();
});

pwdInputConf.addEventListener('input', function() {
    onInputChange();
});

function onInputChange() {
    if (usernameInput.value == '' || pwdInput.value == '' || pwdInputConf.value == '' || pwdInput.value != pwdInputConf.value) {
        loginBtn.disabled = true;
    } else {
        loginBtn.disabled = false;
    }
}