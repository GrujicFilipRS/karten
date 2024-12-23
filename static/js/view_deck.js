// Sample cards data sent by Jinja as JSON

let currentIndex = 0;

// Function to update the card content
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

// Event listener for card click to flip it
document.getElementById("flashcard").addEventListener("click", flipCard);

document.addEventListener("keydown", function(event) {
  if (event.key === " ") {
    flipCard();
  }
});

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

// Event listeners for navigation buttons
document.getElementById("nextButton").addEventListener("click", nextCard);
document.getElementById("prevButton").addEventListener("click", prevCard);

// Initialize the first card
updateCard();