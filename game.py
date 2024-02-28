UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other): 
        if not isinstance(other, Position):
            return NotImplemented

        return (self.x == other.x) and (self.y == other.y)

class GameState:
    def __init__(self):
        self.level = Level()
        self.player = self.level.player_start
        self.grabbed_molecules = []

    def reset(self):
        self.__init__()
    
    def try_to_move(self, direction):
        new_player = Position(self.player.x + direction[0], self.player.y + direction[1])

        for wall in self.level.walls:
            if wall == new_player:
                return
            
        self.player = new_player



class Level:
    def load_level_from_string(self, width, height, string):
        if len(string) < (width*height):
            print ("Level size is incorrect")
            # handle error

        for y in range(0, height):
            for x in range(0, width):
                index = width * y + x

                if string[index] == 'X':
                     self.walls.append(Position(x, y))
                elif string[index] == 'P':
                     self.player_start = Position(x, y)
                elif string[index] == 'M':
                     self.molecules.append(Position(x, y))
                    
    def __init__(self):
        self.player_start = Position(0,0)
        self.walls = []
        self.molecules = []

        self.load_level_from_string(13, 13,  "XXXXXXXXXXXXX"
                                             "XXXXXX XXXXXX"
                                             "XXXXX P XXXXX"
                                             "XXXX     XXXX"
                                             "XXX       XXX"
                                             "XX  M   M  XX"
                                             "X           X"
                                             "XX         XX"
                                             "XXX M   M XXX"
                                             "XXXX     XXXX"
                                             "XXXXX   XXXXX"
                                             "XXXXXX XXXXXX"
                                             "XXXXXXXXXXXXX")
