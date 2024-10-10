# src/brick_game/race/test_game.py

import unittest
from .game import RacingGame, GameState

class TestRacingGame(unittest.TestCase):

    def setUp(self):
        self.game = RacingGame()

    def test_initial_state(self):
        self.assertEqual(self.game.state, GameState.START)
        self.assertEqual(self.game.player_position, 4)
        self.assertEqual(self.game.rival_cars, [])
        self.assertEqual(self.game.speed, 1)

    def test_start_game(self):
        self.game.start_game()
        self.assertEqual(self.game.state, GameState.RACING)

    def test_move_player_left(self):
        self.game.start_game()
        self.game.move_player('left')
        self.assertEqual(self.game.player_position, 3)

    def test_move_player_right(self):
        self.game.start_game()
        self.game.move_player('right')
        self.assertEqual(self.game.player_position, 5)

    def test_spawn_rival_car(self):
        self.game.start_game()
        self.game.spawn_rival_car()
        self.assertEqual(len(self.game.rival_cars), 1)
        self.assertTrue(0 <= self.game.rival_cars[0][0] <= 9)  # Lane is between 0 and 9
        self.assertEqual(self.game.rival_cars[0][1], 0)  # Car starts at row 0

    def test_update_rival_cars(self):
        self.game.start_game()
        self.game.spawn_rival_car()
        self.game.update_rival_cars()
        self.assertEqual(self.game.rival_cars[0][1], 1)  # Car should move to row 1

    def test_collision_detection(self):
        self.game.state = GameState.RACING
        self.game.player_position = 3  # Set player position to lane 3
        
        # Simulate a rival car at the same lane and the last row before collision
        self.game.rival_cars = [[3, 18]]  # Rival in the same lane as player
        
        self.game.update_rival_cars()  # This should trigger the collision
        
        self.assertEqual(self.game.state, GameState.COLLISION)


    def test_game_over_after_collision(self):
        self.game.state = GameState.COLLISION
        self.game.check_collision()
        self.assertEqual(self.game.state, GameState.GAME_OVER)

if __name__ == '__main__':
    unittest.main()
