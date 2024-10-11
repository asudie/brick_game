// Initialize the grid when the page loads
document.addEventListener('DOMContentLoaded', function () {
    createGrid();
    fetchStatus();  // Fetch initial status when the page loads
});

// Create the game grid
function createGrid() {
    const grid = document.getElementById('game-grid');
    // Create 200 grid cells (10x20)
    for (let i = 0; i < 200; i++) {
        const cell = document.createElement('div');
        cell.classList.add('cell');
        grid.appendChild(cell);
    }
}

// Function to update the grid based on player and rivals' positions
function updateGrid(playerPosition, rivalCars) {
    const cells = document.querySelectorAll('.cell');

    // Clear the grid first (remove all player and rival classes)
    cells.forEach(cell => cell.classList.remove('player', 'rival'));

    // Set the player position
    if (playerPosition >= 0 && playerPosition < cells.length) {
        cells[playerPosition].classList.add('player');
    }

    // Set the rival cars' positions
    rivalCars.forEach(pos => {
        if (pos >= 0 && pos < cells.length) {
            cells[pos].classList.add('rival');
        }
    });
}

// General function to update game status on the UI
function updateStatusMessage(message) {
    document.getElementById('game-status').innerText = message;  // Default message if none provided
}

// Function to handle fetch requests
function handleFetch(url, options, successCallback) {
    updateStatusMessage('Processing request...');  // Indicate processing

    fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);  // Throw error for bad responses
            }
            return response.json();
        })
        .then(data => {
            const message = data.message || data.error;
            updateStatusMessage(message);  // Show the server response message
            if (successCallback) {
                successCallback(data);  // Optional callback for specific actions
            }
        })
        .catch(error => {
            console.error('Error:', error);
            updateStatusMessage('An error occurred. Please try again.');
        });
}

// Start the game
document.getElementById('start-game').addEventListener('click', function () {
    updateStatusMessage('Starting game...');
    handleFetch('/start', { method: 'POST' }, fetchStatus);
});

// Move Left
document.getElementById('move-left').addEventListener('click', function () {
    updateStatusMessage('Moving player left...');
    handleFetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ direction: 'left' })
    }, fetchStatus);
});

// Move Right
document.getElementById('move-right').addEventListener('click', function () {
    updateStatusMessage('Moving player right...');
    handleFetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ direction: 'right' })
    }, fetchStatus);
});

// Fetch the game status from the server and update the grid
function fetchStatus() {
    handleFetch('/status', { method: 'GET' }, function (data) {
        const playerPosition = data.player_position;
        const rivalCars = data.rival_cars;
        updateGrid(playerPosition, rivalCars);  // Update the grid with new positions
    });
}

// Spawn a rival car
document.getElementById('spawn-rival').addEventListener('click', function () {
    updateStatusMessage('Spawning rival car...');
    handleFetch('/spawn_rival', { method: 'POST' }, fetchStatus);
});

// Update the game (move rivals, check for collisions)
document.getElementById('update-game').addEventListener('click', function () {
    updateStatusMessage('Updating game...');
    handleFetch('/update', { method: 'POST' }, fetchStatus);
});
