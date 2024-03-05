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

    def try_to_grab(self, molecule):
        molecule.verify_grabs(self.level.molecules)

        if molecule.grabbed_up != self.level.molecules[molecule.position.y - 1][molecule.position.x] and self.level.molecules[molecule.position.y - 1][molecule.position.x].grabbed_up != molecule:
            molecule.grabbed_up = self.level.molecules[molecule.position.y - 1][molecule.position.x]
            self.level.molecules[molecule.position.y - 1][molecule.position.x].grabbed_up = molecule
        if molecule.grabbed_down != self.level.molecules[molecule.position.y + 1][molecule.position.x] and self.level.molecules[molecule.position.y + 1][molecule.position.x].grabbed_down != molecule:
            molecule.grabbed_down = self.level.molecules[molecule.position.y + 1][molecule.position.x]
            self.level.molecules[molecule.position.y + 1][molecule.position.x].grabbed_down = molecule
        if molecule.grabbed_left != self.level.molecules[molecule.position.y][molecule.position.x - 1] and self.level.molecules[molecule.position.y][molecule.position.x - 1].grabbed_left != molecule:
            molecule.grabbed_left = self.level.molecules[molecule.position.y][molecule.position.x - 1]
            self.level.molecules[molecule.position.y][molecule.position.x - 1].grabbed_left = molecule
        if molecule.grabbed_right != self.level.molecules[molecule.position.y][molecule.position.x + 1] and self.level.molecules[molecule.position.y][molecule.position.x + 1].grabbed_right != molecule:
            molecule.grabbed_right = self.level.molecules[molecule.position.y][molecule.position.x + 1]
            self.level.molecules[molecule.position.y][molecule.position.x + 1].grabbed_right = molecule

    def move_molecule(self, molecule, direction):
        self.level.molecules[molecule.position.y][molecule.position.x] = None
        molecule.position.x += direction[0]
        molecule.position.y += direction[1]
        self.level.molecules[molecule.position.y][molecule.position.x] = molecule

        if molecule.grabbed_up != None and direction != UP:
            self.try_to_move_molecule(molecule.grabbed_up, direction)
        if molecule.grabbed_down != None and direction != DOWN:
            self.try_to_move_molecule(molecule.grabbed_down, direction)
        if molecule.grabbed_left != None and direction != LEFT:
            self.try_to_move_molecule(molecule.grabbed_left, direction)
        if molecule.grabbed_right != None and direction != RIGHT:
            self.try_to_move_molecule(molecule.grabbed_right, direction)
    
    def try_to_move_molecule(self, molecule, direction):
        if (self.level.walls[molecule.position.y + direction[1]][molecule.position.x + direction[0]] == 0):
            next_molecule = self.level.molecules[molecule.position.y + direction[1]][molecule.position.x + direction[0]]
            if (next_molecule != None):
                if not self.try_to_move_molecule(next_molecule, direction):
                    return False
            self.move_molecule(molecule, direction)
            return True
        return False
    
    def try_to_move(self, direction):
        if self.try_to_move_molecule(self.player, direction):
            self.try_to_grab(self.player)


class Molecule():
    def __init__(self, char, x, y):
        self.char = char
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

        self.grabbed_up = None
        self.grabbed_down = None
        self.grabbed_left = None
        self.grabbed_right = None
    
    def verify_grabs(self, molecules):
        if self.grabbed_up != None and self.grabbed_up != molecules[self.position.y - 1][self.position.x]:
            self.grabbed_up.grabbed_down = None
            self.grabbed_up = None
        if self.grabbed_down != None and self.grabbed_down != molecules[self.position.y + 1][self.position.x]:
            self.grabbed_down.grabbed_up = None
            self.grabbed_down = None
        if self.grabbed_left != None and self.grabbed_left != molecules[self.position.y][self.position.x - 1]:
            self.grabbed_left.grabbed_right = None
            self.grabbed_left = None
        if self.grabbed_right != None and self.grabbed_right != molecules[self.position.y][self.position.x + 1]:
            self.grabbed_right.grabbed_left = None
            self.grabbed_right = None

    def count_grabbed(self):
        count = 0
        if self.grabbed_up != None:
            count+=1
        if self.grabbed_down != None:
            count+=1
        if self.grabbed_left != None:
            count+=1
        if self.grabbed_right != None:
            count+=1

        return count

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
