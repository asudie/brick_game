# src/brick_game/race/game.py
from enum import Enum
import curses
import random
import time

class GameState(Enum):
    START = 1
    RACING = 2
    COLLISION = 3
    GAME_OVER = 4

class RacingGame:
    def __init__(self):
        self.state = GameState.START
        self.track = [[None for _ in range(10)] for _ in range(20)]  # 10x20 game field
        self.player_position = 4  # Start in the middle lane (0-indexed, so 4 is the middle lane)
        self.rival_cars = []
        self.speed = 1  # Initial speed
    
    def start_game(self):
        if self.state == GameState.START:
            self.state = GameState.RACING
            print("Game has started. Use left/right arrows to move.")
    
    def move_player(self, direction):
        if self.state == GameState.RACING:
            if direction == 'left' and self.player_position > 0:
                self.player_position -= 1
            elif direction == 'right' and self.player_position < 9:
                self.player_position += 1
            print(f"Player moved to lane {self.player_position}")
    
    def spawn_rival_car(self):
        # Generate a rival car at a random lane at the top of the track
        lane = random.randint(0, 9)
        self.rival_cars.append([lane, 0])  # Each car is represented as [lane, row]
    
    def update_rival_cars(self):
        if self.state == GameState.RACING:
            for car in self.rival_cars:
                car[1] += self.speed  # Move car down the track
                if car[1] >= 20:
                    self.rival_cars.remove(car)  # Remove car if it moves out of bounds
                elif car[1] == 19 and car[0] == self.player_position:
                    self.state = GameState.COLLISION
                    print("Collision! Game Over.")
                    break
    
    def check_collision(self):
        if self.state == GameState.COLLISION:
            self.state = GameState.GAME_OVER
            print("Game Over.")

# handle input 
def handle_input(stdscr, game):
    stdscr.nodelay(True)
    key = stdscr.getch()

    if key == curses.KEY_LEFT:
        game.move_player('left')
    elif key == curses.KEY_RIGHT:
        game.move_player('right')
    return key

# main game loop
def game_loop(stdscr):
    game = RacingGame()
    game.start_game()
    
    # Timing for periodic updates
    last_time = time.time()
    
    while game.state != GameState.GAME_OVER:
        # Handle player input
        key = handle_input(stdscr, game)
        
        # Increase speed if holding forward arrow
        if key == curses.KEY_UP:
            game.speed = 2
        else:
            game.speed = 1
        
        # Spawn rival cars periodically
        current_time = time.time()
        if current_time - last_time > 1:  # Spawn every second
            game.spawn_rival_car()
            last_time = current_time

        # Update rival cars and check for collisions
        game.update_rival_cars()
        if game.state == GameState.COLLISION:
            game.check_collision()
        
        # Delay to control game speed
        time.sleep(0.1)

    # Game Over message
    stdscr.clear()
    stdscr.addstr(10, 10, "Game Over! Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(game_loop)
