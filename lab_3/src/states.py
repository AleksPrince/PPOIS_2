from enum import Enum

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    SCOREBOARD = 3
    HELP = 4
    QUIT = 5