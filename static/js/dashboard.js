let visibleDeckAmount = 3;
let firstCarouselIndex = 0;
let secondCarouselIndex = 0;

function logicForResizing() {
    if (window.innerWidth > 1400) {
        visibleDeckAmount = 3;
    } else if (window.innerWidth > 995) {
        visibleDeckAmount = 2;
    } else {
        visibleDeckAmount = 1;
    }

    updateVisible();
}

// Updates the visible decks onto the carousel
function updateVisible() {
    let myDecksToShow = myDecks.slice(firstCarouselIndex, firstCarouselIndex + visibleDeckAmount);
    let otherDecksToShow = otherDecks.slice(secondCarouselIndex, secondCarouselIndex + visibleDeckAmount);

    // Show/hide controls if necessary
    const myDecksControls = document.getElementById('my-decks-controls');
    const otherDecksControls = document.getElementById('other-decks-controls');

    if (myDecks.length > visibleDeckAmount) {
        myDecksControls.style.display = 'flex';
    } else {
        myDecksControls.style.display = 'none';
    }

    if (otherDecks.length > visibleDeckAmount) {
        otherDecksControls.style.display = 'flex';
    } else {
        otherDecksControls.style.display = 'none';
    }

    // Show decks and update buttons
    for (let i = 0; i < visibleDeckAmount; i++) {
        let myDeck = myDecksToShow[i];
        let otherDeck = otherDecksToShow[i];

        // Show the decks if they exist
        let myDeckElement = document.getElementById(`my-deck${i + 1}`);
        let otherDeckElement = document.getElementById(`other-deck${i + 1}`);

        if (myDeck) {
            myDeckElement.style.display = 'block';
            myDeckElement.querySelector('.title').innerHTML = myDeck.deck_name;
            myDeckElement.querySelector('.desc').innerHTML = myDeck.description;
            myDeckElement.querySelector('.deck-btns .practice-btn').setAttribute('href', `./deck/${myDeck.deck_id}`);
            myDeckElement.querySelector('.deck-btns .edit-btn').setAttribute('href', `./deck/${myDeck.deck_id}/edit`);
        } else {
            myDeckElement.style.display = 'none';
        }

        if (otherDeck) {
            otherDeckElement.style.display = 'block';
            otherDeckElement.querySelector('.title').innerHTML = otherDeck.deck_name;
            otherDeckElement.querySelector('.desc').innerHTML = otherDeck.description;
            otherDeckElement.querySelector('.deck-btns .practice-btn').setAttribute('href', `./deck/${otherDeck.deck_id}`);
        } else {
            otherDeckElement.style.display = 'none';
        }
    }

    // Disable/enable carousel navigation buttons
    document.getElementById('my-c-left').disabled = firstCarouselIndex <= 0;
    document.getElementById('my-c-right').disabled = firstCarouselIndex + visibleDeckAmount >= myDecks.length;

    document.getElementById('other-c-left').disabled = secondCarouselIndex <= 0;
    document.getElementById('other-c-right').disabled = secondCarouselIndex + visibleDeckAmount >= otherDecks.length;
}

function goleft_mine() {
    if (firstCarouselIndex > 0) {
        firstCarouselIndex--;
        updateVisible();
    }
}

function goright_mine() {
    if (firstCarouselIndex + visibleDeckAmount < myDecks.length) {
        firstCarouselIndex++;
        updateVisible();
    }
}

function goleft_other() {
    if (secondCarouselIndex > 0) {
        secondCarouselIndex--;
        updateVisible();
    }
}

function goright_other() {
    if (secondCarouselIndex + visibleDeckAmount < otherDecks.length) {
        secondCarouselIndex++;
        updateVisible();
    }
}

window.onresize = logicForResizing;

updateVisible();
