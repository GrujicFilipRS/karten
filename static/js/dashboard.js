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

let visibleDeckAmount = 3;
let firstCarouselIndex = 0;
let secondCarouselIndex = 0;

function logicForResizing() {
    if (window.innerWidth > 1400) {
        visibleDeckAmount = 3;
    }
    else if (window.innerWidth > 995) {
        visibleDeckAmount = 2;
    }
    else {
        visibleDeckAmount = 1;
    }
}

// Updates the visible decks onto the carousel
function updateVisible()
{
    // Disable the left button if index is 0 to prevent indexing issues
    if (firstCarouselIndex == 0) {
        document.getElementById('my-c-left').disabled = true;
    } else {
        document.getElementById('my-c-left').disabled = false;
    }

    if (secondCarouselIndex == 0) {
        document.getElementById('other-c-left').disabled = true;
    } else {
        document.getElementById('other-c-left').disabled = false;
    }

    // Gathering both of the decklists to display on the carousel
    let myDecks = [];
    for(let i = firstCarouselIndex; i < visibleDeckAmount + firstCarouselIndex; i++) {
        myDecks.push(decks[i % decks.length]);
    }

    let otherDecks = [];
    for(let i = secondCarouselIndex; i < visibleDeckAmount + secondCarouselIndex; i++) {
        otherDecks.push(decks[i % decks.length]);
    }

    // Displaying the decks
    for (let i = 0; i < visibleDeckAmount; i++) {
        myDeck = myDecks[i];
        otherDeck = otherDecks[i];

        let deckEdited = document.getElementById(`my-deck${i+1}`);
        deckEdited.children[0].innerHTML = myDeck['name'];

        deckEdited = document.getElementById(`other-deck${i+1}`);
        deckEdited.children[0].innerHTML = otherDeck['name'];
    }

    return [myDecks, otherDecks];
}

updateVisible();

function goleft_mine() {
    firstCarouselIndex--;
    console.log(updateVisible());
}

function goright_mine() {
    firstCarouselIndex++;
    console.log(updateVisible());
}

function goleft_other() {
    secondCarouselIndex--;
    console.log(updateVisible());
}

function goright_other() {
    secondCarouselIndex++;
    console.log(updateVisible());
}

window.onresize = logicForResizing;