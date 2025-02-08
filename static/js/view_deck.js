const addOrRemoveDeckButton = document.getElementById("button-add-remove-deck");
const buttonText = document.getElementById("add-remove-deck-button-text");
const flashcard = document.getElementById("flashcard");

addButtonPreload()
let currentIndex = 0;


// Event listener for card click to flip it
flashcard.addEventListener("click", flipCard);


// Adding or deleting the deck from user's library
addOrRemoveDeckButton.addEventListener("click", createOrDeleteSavedDeck);

// Event listener for card flipping
document.addEventListener("keydown", function(event) {
    if (event.key === " ") {
        flipCard();
    }
});

// Event listeners for navigation buttons
document.getElementById("nextButton").addEventListener("click", nextCard);
document.getElementById("prevButton").addEventListener("click", prevCard);

// Initialize the first card
updateCard();


async function addButtonPreload() {
    if (!isMyDeck) {
        addOrRemoveDeckButton.style.display = "block";

        const savedDeck = await getSavedDeck(currentUserId, deckId);
        if (!savedDeck.error) {
            buttonText.textContent = savedDeck.data
            ? "Remove from Library"
            : "Add to Library";
        }
    }
}


// Function for card's content updating
function updateCard() {
    const frontSide = document.getElementById("front-side");
    const backSide = document.getElementById("back-side");
    const cardNumber = document.getElementById("cardNumber");

    frontSide.textContent = cards[currentIndex].front;
    backSide.textContent = cards[currentIndex].back;
    cardNumber.textContent = `${currentIndex + 1} / ${cards.length}`;

    // Disable prev button if at the first card
    document.getElementById("prevButton").disabled = currentIndex === 0;
    // Disable next button if at the last card
    document.getElementById("nextButton").disabled = currentIndex === cards.length - 1;
}

// Function to flip the card around the X-axis
function flipCard() {
    const card = document.querySelector(".card");
    card.classList.toggle("flipped");
}

// Function to move to the next card
function nextCard() {
    if (currentIndex < cards.length - 1) {
        currentIndex++;
        const card = document.querySelector(".card");
        card.classList.remove("flipped");
        card.style.transition = "none";  // Disable transition for instant change
        updateCard();
        setTimeout(function() {card.style.transition = "transform 0.6s";}, 50);
    }
}


// Function to move to the previous card
function prevCard() {
    if (currentIndex > 0) {
        currentIndex--;
        const card = document.querySelector(".card");
        card.classList.remove("flipped");
        card.style.transition = "none";  // Disable transition for instant change
        updateCard();
        setTimeout(function() {card.style.transition = "transform 0.6s";}, 50);
    }
}

async function createOrDeleteSavedDeck() {
    if (!isMyDeck){
        try {
            const savedDeck = await getSavedDeck(currentUserId, deckId);

            if (savedDeck.error) {
                console.warn(`${savedDeck.error}`)
                console.error(`Error ${savedDeck.error} while getting SavedDeck: ${savedDeck.message}`);
                return;
            }

            if (savedDeck.data) {
                // If SavedDeck is found, delete it
                console.log("SavedDeck found. Deleting it...", savedDeck.data);
                requestResponse = await deleteSavedDeck(savedDeck.data.id);
                console.log("SavedDeck successfully deleted..");
            } else {
                // If SavedDeck isn't found, add it
                console.log("SavedDeck isn't found. Adding new one...");
                requestResponse = await postSavedDeck(currentUserId, deckId);
                console.log("SavedDeck successfully added.");
            }

            buttonText.textContent = buttonText.textContent === "Add to Library"
            ? "Remove from Library"
            : "Add to Library";
            setTimeout(() => {
                alert(requestResponse.message);
            }, 50);

        }
        catch (error) {
            console.error("Error:", error);
            alert(requestResponse.message);
        }
    }
}

async function getSavedDeck(userId, deckId) {
    try {
        const url = new URL('/api/saved_deck', window.location.origin);
        url.searchParams.append('user_id', userId);
        url.searchParams.append('deck_id', deckId);

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.status === 400) {
            console.error("Error 400: Missing required parameter.");
            return { error: 400, message: "Bad Request", data: null };
        }
        if (response.status === 200) {
            const data = await response.json();
            return { error: null, data };
        }
        if (response.status === 404) {
            return { error: null, data: null };
        }
        if (response.status === 500) {
            console.error("Error 500: API Server Error.");
            return { error: 500, message: "Internal Server Error", data: null };
        }

    } catch (err) {
        console.error("Request error: ", err);
        return { error: 502, message: "Request Failed", data: null };
    }
}


async function postSavedDeck(userId, deckId) {
    try {
        const url = new URL('/api/saved_deck', window.location.origin);
        url.searchParams.append('user_id', userId);
        url.searchParams.append('deck_id', deckId);

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) throw new Error(`Error: ${response.statusText}`);

        // Parse and return the response data
        const requestResponse = await response.json();
        return requestResponse;

    } catch (error) {
        console.error('Error adding saved deck:', error);
        throw error;
    }
}


async function deleteSavedDeck(savedDeckId) {
    try {
        const url = new URL('/api/saved_deck', window.location.origin);
        url.searchParams.append('saved_deck_id', savedDeckId);

        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) throw new Error(`Error: ${response.statusText}`);

        // Parse and return the response data
        const requestResponse = await response.json();
        return requestResponse;

    } catch (error) {
        console.error('Error deleting saved deck:', error);
        throw error;
    }
}
