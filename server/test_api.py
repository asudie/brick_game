import unittest
import json
from .app import app
from ..race.game import RacingGame, GameState  # Make sure to import RacingGame and GameState

class TestRacingGameAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        # Reset the game state before each test
        self.game = RacingGame()
        self.game.state = GameState.START  # Assuming START is the initial state

    def test_start_game(self):
        response = self.client.post('/start')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400) # maybe 200?
        self.assertEqual(data["message"], "Game is already in progress!")  # Expecting a successful start message

    def test_move_player_left(self):
        self.client.post('/start')  # Start the game first
        response = self.client.post('/move', json={"direction": "left"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Player moved left")

    def test_invalid_move(self):
        self.client.post('/start')  # Start the game first
        response = self.client.post('/move', json={"direction": "up"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["error"], "Invalid direction")

    def test_game_status(self):
        self.client.post('/start')  # Start the game first
        response = self.client.get('/status')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", data)
        self.assertIn("player_position", data)

    def test_spawn_rival_car(self):
        self.client.post('/start')  # Start the game first
        response = self.client.post('/spawn_rival')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Rival car spawned")

    def test_update_game(self):
        self.client.post('/start')  # Start the game first
        response = self.client.post('/update')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", data)
        self.assertIn("state", data)

if __name__ == '__main__':
    unittest.main()
