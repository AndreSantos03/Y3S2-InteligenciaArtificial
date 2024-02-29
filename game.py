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

        grab_pos_up = Position(self.player.position.x, self.player.position.y - 1)
        grab_pos_down = Position(self.player.position.x, self.player.position.y + 1)
        grab_pos_left = Position(self.player.position.x - 1, self.player.position.y)
        grab_pos_right = Position(self.player.position.x + 1, self.player.position.y)

        for molecule_index in range(0, len(self.level.molecules)):
            molecule = self.level.molecules[molecule_index]
            if molecule == grab_pos_up or molecule == grab_pos_down or molecule == grab_pos_left or molecule == grab_pos_right:
                new_grabbed_molecules.append(molecule_index)

        self.grabbed_molecules = new_grabbed_molecules
    
    def try_to_move_molecule(self, molecule, direction):
        print (0)
        if (self.level.walls[molecule.position.y + direction[1]][molecule.position.x + direction[0]] == 0):
            print (1)
            if (self.level.molecules[molecule.position.y + direction[1]][molecule.position.x + direction[0]] == None):
                molecule.position.x += direction[0]
                molecule.position.y += direction[1]
                print (2)
    
    def try_to_move(self, direction):
        if self.try_to_move_molecule(self.player, direction):
            pass
            # self.try_to_grab()


        # collision_pos = Position(self.player.position.x, self.player.position.y)
        # collision_index = -1 # -1=looking 0=found_empty 1=found_wall

        # while collision_index == -1:
        #     collision_index = 0

        #     collision_pos.x += direction[0]
        #     collision_pos.y += direction[1]

        #     for molecule in self.level.molecules:
        #         if molecule == collision_pos:
        #             collision_index = -1
        #             break

        #     for wall in self.level.walls:
        #         if wall == collision_pos:
        #             collision_index = 1
        #             break
            
        # if collision_index == 0:
        #     self.player.position.x += direction[0]
        #     self.player.position.y += direction[1]

        #     for grabbed_molecule_index in self.grabbed_molecules:
        #         self.level.molecules[grabbed_molecule_index].x += direction[0]
        #         self.level.molecules[grabbed_molecule_index].y += direction[1]

        #     self.try_to_grab()


class Molecule():
    def __init__(self, char, x, y):
        self.position = Position(x,y)
        
        self.max_grab = 0
        if char == 'h':
            self.max_grab = 1
        elif char == 'o':
            self.max_grab = 2
        elif char == 'n':
            self.max_grab = 3
        elif char == 'c':
            self.max_grab = 4

        self.grabbed = []

class Level:
    def load_level_from_string(self, width, height, string):
        if len(string) < (width*height):
            print ("Level size is incorrect")
            # handle error
        
        self.width = width
        self.height = height

        self.walls = [[0] * width for i in range(0, height)]
        self.molecules = [[None] * width for i in range(0, height)]

        for y in range(0, height):
            for x in range(0, width):
                index = width * y + x

                if string[index] == 'X':
                    self.walls[y][x] = 1
                elif string[index] != ' ':
                    molecule = Molecule(string[index], x, y)
                    if string[index].isupper():
                        self.player_start = molecule
                    else:
                        self.molecules[y][x] = molecule

                    
    def __init__(self):
        self.player_start = Molecule('h', 0, 0)

        self.walls = []
        self.molecules = []

        self.width = 0
        self.height = 0

        self.load_level_from_string(13, 13,  "XXXXXXXXXXXXX"
                                             "XXXXXX XXXXXX"
                                             "XXXXX C XXXXX"
                                             "XXXX     XXXX"
                                             "XXX       XXX"
                                             "XX  h   h  XX"
                                             "X           X"
                                             "XX   X     XX"
                                             "XXX h   h XXX"
                                             "XXXX     XXXX"
                                             "XXXXX   XXXXX"
                                             "XXXXXX XXXXXX"
                                             "XXXXXXXXXXXXX")
