document.getElementById('start-game').addEventListener('click', function() {
    fetch('/start', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            document.getElementById('game-status').innerText = data.message;
        })
        .catch(error => console.error('Error:', error));
});

document.getElementById('move-left').addEventListener('click', function() {
    fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ direction: 'left' })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('game-status').innerText = data.message || data.error;
    })
    .catch(error => console.error('Error:', error));
});

// Add similar event listeners for other buttons (move-right, spawn-rival, update-game)
