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

    if (myDecks.length <= visibleDeckAmount)
        document.getElementsByClassName('controls')[0].style['display'] = 'none';
    else
        document.getElementsByClassName('controls')[0].style['display'] = 'flex';

    if (otherDecks.length <= visibleDeckAmount)
        document.getElementsByClassName('controls')[1].style['display'] = 'none';
    else
        document.getElementsByClassName('controls')[1].style['display'] = 'flex';
}

// Displaying of none to decks that don't exist because len(myDecks) or len(otherDecks) is too small
if (myDecks.length <= 2) {
    document.getElementsByClassName('deck3')[0].style['display'] = 'none';
}

if (myDecks.length <= 1) {
    document.getElementsByClassName('deck2')[0].style['display'] = 'none';
    document.getElementsByClassName('controls')[0].style['display'] = 'none';
}

if(myDecks.length == 0) {
    document.getElementsByClassName('deck1')[0].style['display'] = 'none';
}

if (otherDecks.length <= 2) {
    document.getElementsByClassName('deck3')[1].style['display'] = 'none';
}

if (otherDecks.length <= 1) {
    document.getElementsByClassName('deck2')[1].style['display'] = 'none';
    document.getElementsByClassName('controls')[1].style['display'] = 'none';
}

if(otherDecks.length == 0) {
    document.getElementsByClassName('deck1')[1].style['display'] = 'none';
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
    let myDecksToShow = [];
    for(let i = firstCarouselIndex; i < visibleDeckAmount + firstCarouselIndex; i++) {
        myDecksToShow.push(myDecks[i % myDecks.length]);
    }

    let otherDecksToShow = [];
    for(let i = secondCarouselIndex; i < visibleDeckAmount + secondCarouselIndex; i++) {
        otherDecksToShow.push(otherDecks[i % otherDecks.length]);
    }

    // Displaying the decks
    for (let i = 0; i < visibleDeckAmount; i++) {
        myDeck = myDecksToShow[i];
        otherDeck = otherDecksToShow[i];
        
        // Try block is here in case of the user having less than visibleDeckAmount number of decks
        try {
            let deckEdited = document.getElementById(`my-deck${i+1}`);
            deckEdited.children[0].innerHTML = myDeck['deck_name'];
            deckEdited.children[1].innerHTML = myDeck['description'];
    
            deckEdited = document.getElementById(`other-deck${i+1}`);
            deckEdited.children[0].innerHTML = otherDeck['deck_name'];
            deckEdited.children[1].innerHTML = otherDeck['description'];
        }
        catch(e) {
            console.log(`Error caught: ${e}`)
        }
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