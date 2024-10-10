# src/brick_game/server/app.py
from flask import Flask, jsonify, request, send_from_directory
from race.game import RacingGame, GameState

app = Flask(__name__, static_folder='../web_gui')  # Set static folder to point to web_gui

# Initialize the game
game = RacingGame()

@app.route('/')
def front():
    return send_from_directory(app.static_folder, 'front.html')  # Serve front.html from web_gui

@app.route('/start', methods=['POST'])
def start_game():
    if game.state == GameState.START:
        return jsonify({"message": "Game is already in progress!"}), 400  # Return a 400 status code
    game.start_game()
    return jsonify({"message": "Game started!"}), 200  # Return a 200 status code

@app.route('/move', methods=['POST'])
def move_player():
    if game.state == GameState.GAME_OVER:
        return jsonify({"error": "Game Over"}), 400  # Return a 400 status code for game over
    data = request.get_json()
    direction = data.get('direction')
    if direction in ['left', 'right']:
        game.move_player(direction)
        return jsonify({"message": f"Player moved {direction}"}), 200  # Return a 200 status code
    return jsonify({"error": "Invalid direction"}), 400  # Return a 400 status code for invalid direction

@app.route('/status', methods=['GET'])
def game_status():
    if game.state == GameState.GAME_OVER:
        return jsonify({"status": "Game Over"}), 200  # Return a 200 status code
    return jsonify({
        "status": str(game.state),
        "player_position": game.player_position,
        "rival_cars": game.rival_cars
    }), 200  # Return a 200 status code

@app.route('/spawn_rival', methods=['POST'])
def spawn_rival():
    if game.state == GameState.GAME_OVER:
        return jsonify({"error": "Game Over"}), 400  # Return a 400 status code for game over
    game.spawn_rival_car()
    return jsonify({"message": "Rival car spawned"}), 200  # Return a 200 status code

@app.route('/update', methods=['POST'])
def update_game():
    if game.state == GameState.GAME_OVER:
        return jsonify({"error": "Game Over"}), 400  # Return a 400 status code for game over
    game.update_rival_cars()
    game.check_collision()  # This will check for collisions
    return jsonify({
        "message": "Game updated",
        "state": str(game.state)
    }), 200  # Return a 200 status code

if __name__ == '__main__':
    app.run(debug=True)
