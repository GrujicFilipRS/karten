class Deck {
    constructor(id, userCreatedId, name, timeChanged, description) {
        this.id = id;
        this.userCreatedId = userCreatedId;
        this.name = name;
        this.timeChanged = timeChanged;
        this.description = description;
    }
}

let myDecksStr = document.getElementById('my-decks-info').getAttribute('data').replaceAll('\'', '"');
let otherDecksStr = document.getElementById('other-decks-info').getAttribute('data').replaceAll('\'', '"');

function parseJsonObjects(jsonString) {
    try {
        const jsonArray = JSON.parse(jsonString);
        
        if (Array.isArray(jsonArray) && jsonArray.every(obj => typeof obj === 'object' && obj !== null)) {
            return jsonArray;
        } else {
            throw new Error("Input is not a valid list of JSON objects.");
        }
    } catch (error) {
        console.error("Error parsing JSON string:", error.message);
        return null;
    }
}

let myDecks = parseJsonObjects(myDecksStr);
let otherDecks = parseJsonObjects(otherDecksStr);