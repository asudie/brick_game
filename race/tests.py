import unittest
from game import GameFSM

class TestFSM(unittest.TestCase):
    def test_state_transition(self):
        fsm = GameFSM()
        fsm.start_game()
        self.assertEqual(fsm.state, "Playing")
        fsm.end_game()
        self.assertEqual(fsm.state, "Game Over")

if __name__ == "__main__":
    unittest.main()
