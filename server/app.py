# src/brick_game/server/app.py
from race.game import RacingGame, GameState
from flask import Flask, jsonify, request, send_from_directory
import logging

# Initialize Flask app
app = Flask(__name__, static_folder='../web_gui', static_url_path='')  # static_url_path set to serve from root

# Initialize the game
game = RacingGame()

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def front():
    return send_from_directory(app.static_folder, 'front.html')  # Serve front.html from web_gui

@app.route('/start', methods=['POST'])
def start_game():
    logging.info(f"Current game state: {game.state}")
    if game.state == GameState.START:
        try:
            game.start_game()
            logging.info("Game started successfully.")
            return jsonify({"message": "Game started!"}), 200  # Return a 200 status code
        except Exception as e:
            logging.error(f"Error starting game: {str(e)}")
            return jsonify({"error": "Failed to start the game"}), 500  # Return a 500 status code for server error
    else:
        logging.warning("Game is already in progress!")
        return jsonify({"error": "Game is already in progress!"}), 400  # Return a 400 status code

@app.route('/move', methods=['POST'])
def move_player():
    if game.state == GameState.GAME_OVER:
        logging.warning("Attempt to move after game over.")
        return jsonify({"error": "Game Over"}), 400  # Return a 400 status code for game over
    
    if game.state == GameState.START:
        logging.warning("Attempt to move before game start.")
        return jsonify({"error": "Game has not started yet."}), 400
    
    data = request.get_json()
    direction = data.get('direction')

    if direction in ['left', 'right']:
        game.move_player(direction)
        logging.info(f"Player moved {direction}. Current position: {game.player_position}")
        return jsonify({
            "message": f"Player moved {direction}",
            "player_position": game.player_position,
            "rival_cars": game.rival_cars  # Include the current state of rival cars
        }), 200  # Return a 200 status code
    else:
        logging.warning(f"Invalid direction: {direction}")
        return jsonify({"error": "Invalid direction"}), 400  # Return a 400 status code for invalid direction

@app.route('/status', methods=['GET'])
def game_status():
    if game.state == GameState.GAME_OVER:
        logging.info("Game over status requested.")
        return jsonify({"status": "Game Over"}), 200  # Return a 200 status code
    
    logging.info("Returning current game status.")
    return jsonify({
        "status": str(game.state),
        "player_position": game.player_position,
        "rival_cars": game.rival_cars
    }), 200  # Return a 200 status code

@app.route('/spawn_rival', methods=['POST'])
def spawn_rival():
    if game.state == GameState.GAME_OVER:
        logging.warning("Attempt to spawn rival after game over.")
        return jsonify({"error": "Game Over"}), 400  # Return a 400 status code for game over
    
    try:
        game.spawn_rival_car()
        logging.info("Rival car spawned.")
        return jsonify({"message": "Rival car spawned"}), 200  # Return a 200 status code
    except Exception as e:
        logging.error(f"Error spawning rival car: {str(e)}")
        return jsonify({"error": "Failed to spawn rival car"}), 500  # Return a 500 status code for server error

@app.route('/update', methods=['POST'])
def update_game():
    if game.state == GameState.GAME_OVER:
        logging.warning("Attempt to update after game over.")
        return jsonify({"error": "Game Over"}), 400  # Return a 400 status code for game over
    
    try:
        game.update_rival_cars()
        collision_occurred = game.check_collision()  # This will check for collisions
        if collision_occurred:
            logging.info("Collision detected. Game over.")
            game.state = GameState.GAME_OVER  # Update the game state if needed
            
        return jsonify({
            "message": "Game updated",
            "state": str(game.state),
            "player_position": game.player_position,
            "rival_cars": game.rival_cars
        }), 200  # Return a 200 status code
    except Exception as e:
        logging.error(f"Error updating game: {str(e)}")
        return jsonify({"error": "Failed to update the game"}), 500  # Return a 500 status code for server error

if __name__ == '__main__':
    app.run(debug=True)
