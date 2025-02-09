let usernameInput = document.getElementById('form-username-field');
let pwdInput = document.getElementById('form-password-field');
let pwdInputConf = document.getElementById('form-confirm-password-field');
let submitButton = document.getElementById('submit-button');

submitButton.disabled = true;

usernameInput.addEventListener('input', onInputChange);
pwdInput.addEventListener('input', onInputChange);
if (formClass === "signup-form") {
    pwdInputConf.addEventListener('input', onInputChange);
}

function onInputChange() {
    if (formClass === "signup-form") {
        onInputChangeSignUp();
    } else if (formClass === "login-form") {
        onInputChangeLogin();
    }
}

function onInputChangeLogin() {
    if (usernameInput.value == '' || pwdInput.value == '') {
        submitButton.disabled = true;
    } else {
        submitButton.disabled = false;
    }
    console.log(submitButton.disabled);
}

function onInputChangeSignUp() {
    if (usernameInput.value == '' || pwdInput.value == '' || pwdInputConf.value == '' || pwdInput.value != pwdInputConf.value) {
        submitButton.disabled = true;
    } else {
        submitButton.disabled = false;
    }
}