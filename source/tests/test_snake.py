import curses
from snake import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def game():
    with patch('snake_game.curses') as curses_mock:
        # Mocking window methods and variables
        curses_mock.initscr.return_value.getmaxyx.return_value = (20, 20)
        window_mock = MagicMock()
        curses_mock.newwin.return_value = window_mock
        game_instance = game()
    return game_instance, window_mock

def test_snake_movement(game):
    game_instance, window_mock = game
    # Mock key inputs for moving right
    window_mock.getch.side_effect = [curses.KEY_RIGHT, -1]
    game_instance.main_loop() # This would be your main game loop that you'd need to adapt to be testable
    assert game_instance.snake[0] == [game_instance.snk_y, game_instance.snk_x + 1] # Assuming snake's initial position is (snk_y, snk_x)

def test_food_consumption(game):
    game_instance, window_mock = game
    # Setup the game state to simulate eating food
    game_instance.food = game_instance.snake[0] # Place food at snake's head position
    game_instance.main_loop() # Run one iteration of the game loop
    assert game_instance.food != game_instance.snake[0] # Food should be repositioned

def test_collision_detection(game):
    game_instance, window_mock = game
    # Direct the snake to collide with the wall
    game_instance.snake[0] = [0, 0] # Assume this position is a collision
    with pytest.raises(SystemExit): # Assuming your game exits on collision
        game_instance.main_loop()
