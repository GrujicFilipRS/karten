const cardsContainer = document.getElementById("cards-container");

initializePage()

document.getElementById("add-card").addEventListener("click", addNewCard);
document.getElementById("submit-deck").addEventListener("click", submitDeck);

function initializePage() {
    while (cardsContainer.children.length < 5) {
        addNewCard();
    }
}

function addNewCard() {
    const index = cardsContainer.children.length;

    const cardDiv = document.createElement("div");
    cardDiv.className = "card";
    cardDiv.dataset.index = index;

    cardDiv.innerHTML = `
        <input type="text" placeholder="Front" class="front">
        <input type="text" placeholder="Back" class="back">
        <button class="move-up">↑</button>
        <button class="move-down">↓</button>
        <button class="delete-card">X</button>
    `;

    cardDiv.querySelector(".delete-card").addEventListener("click", () => deleteCard(cardDiv));
    cardDiv.querySelector(".move-up").addEventListener("click", () => moveCardUp(cardDiv));
    cardDiv.querySelector(".move-down").addEventListener("click", () => moveCardDown(cardDiv));

    cardsContainer.appendChild(cardDiv);
}

function deleteCard(card) {
    if (cardsContainer.children.length > 1) {
        card.remove();
        updateCardIndexes();
    }
}

function moveCardUp(card) {
    if (card.previousElementSibling) {
        card.parentNode.insertBefore(card, card.previousElementSibling);
        updateCardIndexes();
    }
}

function moveCardDown(card) {
    if (card.nextElementSibling) {
        card.parentNode.insertBefore(card.nextElementSibling, card);
        updateCardIndexes();
    }
}

function updateCardIndexes() {
    [...cardsContainer.children].forEach((card, i) => {
        card.dataset.index = i;
    });
}

async function submitDeck() {
    const deck_name = document.getElementById("deck-name").value.trim();
    const description = document.getElementById("deck-description").value.trim();
    const cards = [...cardsContainer.children].map(card => ({
        front: card.querySelector(".front").value.trim(),
        back: card.querySelector(".back").value.trim()
    }));

    if (!deck_name) {
        showError("Deck name is required!");
        return;
    }

    if (cards.length < 5) {
        showError("Deck must contain 5 cards minimum.");
        return;
    }

    const incompleteCardIndex = cards.findIndex(card => (!card.front || !card.back));
    if (incompleteCardIndex !== -1) {
        showError(`Card ${incompleteCardIndex + 1} must have both front and back filled.`);
        return;
    }

    try {
        response = await postDeck(deck_name, description, cards);
        console.log(response);
        console.log("LOL");
        window.location.href = "/dashboard";

    } catch(error) {
        console.error("An error occurred:", error);
        return;
    }
}

async function postDeck(deck_name, description, cards) {
    try {
        const url = new URL('/api/create_deck', window.location.origin);

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ deck_name, description, cards })
        });
        const responseData = await response.json();

        if (!response.ok) throw new Error(responseData.error || "Unknown error occurred");

        return responseData;

    } catch (error) {
        console.error('Internal server error deck:', error);
        showError(`Internal server error: ${error}`)
        throw new Error(error);
    }
}

function showError(message) {
    const errorContainer = document.getElementById("error-message");
    errorContainer.textContent = message;
}
