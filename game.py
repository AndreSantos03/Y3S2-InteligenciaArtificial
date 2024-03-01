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

        adjacent_positions = [
            Position(self.player.position.x, self.player.position.y - 1),
            Position(self.player.position.x, self.player.position.y + 1),
            Position(self.player.position.x - 1, self.player.position.y),
            Position(self.player.position.x + 1, self.player.position.y),
        ]

        for y in range(self.level.height):
            for x in range(self.level.width):
                molecule = self.level.molecules[y][x]
                if molecule and any(molecule.position == pos for pos in adjacent_positions):
                    print("Connection done")
                    new_grabbed_molecules.append(molecule)

        self.grabbed_molecules = new_grabbed_molecules
    
    def try_to_move_molecule(self, molecule, direction):
        if (self.level.walls[molecule.position.y + direction[1]][molecule.position.x + direction[0]] == 0):
            next_molecule = self.level.molecules[molecule.position.y + direction[1]][molecule.position.x + direction[0]]
            print (self.level.molecules[molecule.position.y + direction[1]][molecule.position.x + direction[0]])
            if (next_molecule != None):
                if not self.try_to_move_molecule(next_molecule, direction):
                    return False
            molecule.position.x += direction[0]
            molecule.position.y += direction[1]
            return True
        return False
    
    def update_molecule_positions(self):
        for molecule in self.grabbed_molecules:
            # Calculate new position based on movement direction
            new_x, new_y = self.calculate_new_position(molecule.position, direction)
            # Update the grid or list tracking molecule positions
            self.level.molecules[molecule.position.y][molecule.position.x] = None  # Clear old position
            molecule.position.x, molecule.position.y = new_x, new_y  # Update molecule object
            self.level.molecules[new_y][new_x] = molecule  # Update new position in tracking structure

    def calculate_new_position(self, current_position, direction):
        # Returns the new position based on the current position and direction of movement
        return current_position.x + direction[0], current_position.y + direction[1]

    def try_to_move(self, direction):
        new_player_x = self.player.position.x + direction[0]
        new_player_y = self.player.position.y + direction[1]

        self.player.position.x = new_player_x
        self.player.position.y = new_player_y

        for molecule in self.grabbed_molecules:
            new_mol_x = molecule.position.x + direction[0]
            new_mol_y = molecule.position.y + direction[1]

            self.level.molecules[molecule.position.y][molecule.position.x] = None
            molecule.position.x = new_mol_x
            molecule.position.y = new_mol_y
            self.level.molecules[new_mol_y][new_mol_x] = molecule 
            
        self.try_to_grab()
        #if self.try_to_move_molecule(self.player, direction):
        #    pass
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
