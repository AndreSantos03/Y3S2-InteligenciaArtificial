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

    def try_to_grab(self):
        new_grabbed_molecules = []

        grab_pos_up = Position(self.player.x, self.player.y - 1)
        grab_pos_down = Position(self.player.x, self.player.y + 1)
        grab_pos_left = Position(self.player.x - 1, self.player.y)
        grab_pos_right = Position(self.player.x + 1, self.player.y)

        for molecule_index in range(0, len(self.level.molecules)):
            molecule = self.level.molecules[molecule_index]
            if molecule == grab_pos_up or molecule == grab_pos_down or molecule == grab_pos_left or molecule == grab_pos_right:
                new_grabbed_molecules.append(molecule_index)

        self.grabbed_molecules = new_grabbed_molecules
    
    def try_to_move(self, direction):
        collision_pos = Position(self.player.x, self.player.y)
        collision_index = 0 # 0=looking 1=found_empty 2=found_wall

        while collision_index == 0:
            collision_index = 1

            collision_pos.x += direction[0]
            collision_pos.y += direction[1]

            for molecule in self.level.molecules:
                if molecule == collision_pos:
                    collision_index = 0
                    break

            for wall in self.level.walls:
                if wall == collision_pos:
                    collision_index = 2
                    break
            
        if collision_index == 1:
            self.player.x += direction[0]
            self.player.y += direction[1]

            for grabbed_molecule_index in self.grabbed_molecules:
                self.level.molecules[grabbed_molecule_index].x += direction[0]
                self.level.molecules[grabbed_molecule_index].y += direction[1]

            self.try_to_grab()



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
                                             "XX   X     XX"
                                             "XXX M   M XXX"
                                             "XXXX     XXXX"
                                             "XXXXX   XXXXX"
                                             "XXXXXX XXXXXX"
                                             "XXXXXXXXXXXXX")
