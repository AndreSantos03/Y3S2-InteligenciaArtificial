UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GameState:
    def __init__(self):
        self.level = Level()
        self.player_pos = self.level.player_start_pos

    def reset(self):
        self.__init__()
    
    def try_to_move(self, direction):
        self.player_pos.x += direction[0]
        self.player_pos.y += direction[1]

class Level:
    def __init__(self):
        self.player_start_pos = Position(6,6)
        self.walls = [Position(0,0),Position(0,1)]