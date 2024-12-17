let navButtons = document.getElementById('nav-btns');
let navButtonsDisabled = true;

function toggleNavBar() {
    navButtonsDisabled = !navButtonsDisabled;
    navButtons.disabled = navButtonsDisabled;
    if (navButtonsDisabled)
        navButtons.style.display = 'none';
    else
        navButtons.style.display = 'flex';
}