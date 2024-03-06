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
        self.grabbed_molecules = [self.level.player]

    def reset(self):
        self.__init__()


    def possible_move(self, direction):
        if direction == UP:
            max_y = None
            for molecule in self.grabbed_molecules:
                if molecule.position.x == self.level.player.position.x:
                    if max_y is None or molecule.position.y < max_y:
                        max_y = molecule.position.y
            return self.level.walls[max_y - 1][self.level.player.position.x] == 0

        elif direction == DOWN:
            max_y = None
            for molecule in self.grabbed_molecules:
                if molecule.position.x == self.level.player.position.x:
                    if max_y is None or molecule.position.y > max_y:
                        max_y = molecule.position.y
            return self.level.walls[max_y + 1][self.level.player.position.x] == 0
        elif direction == LEFT:
            left_x = None
            for molecule in self.grabbed_molecules:
                if molecule.position.y == self.level.player.position.y:
                    if left_x is None or molecule.position.x < left_x:
                        left_x = molecule.position.x
            return self.level.walls[self.level.player.position.y][left_x - 1] == 0
        elif direction == RIGHT:
            right_x = None
            for molecule in self.grabbed_molecules:
                if molecule.position.y == self.level.player.position.y:
                    if right_x is None or molecule.position.x > right_x:
                        right_x = molecule.position.x
            return self.level.walls[self.level.player.position.y][right_x + 1] == 0
        return False

    def try_to_move(self,direction):
        if self.possible_move(direction):
            to_add_grababble = []
            for grabbed_mol in self.grabbed_molecules:
                to_add_grababble = to_add_grababble + self.molecule_move(grabbed_mol,direction)
            self.grabbed_molecules = self.grabbed_molecules + to_add_grababble 
            


    def molecule_move(self, molecule, direction):
        new_x = molecule.position.x + direction[0]
        new_y = molecule.position.y + direction[1] 

        new_grababble = []
        print(new_x)
        if self.level.walls[new_x][new_y] == 1:
            print("REMOVE REMOVE")
            self.grabbed_molecules.remove(molecule)
        else:
            grabable_positions = [(new_x, new_y - 1), (new_x, new_y + 1), (new_x - 1, new_y), (new_x + 1, new_y)]
            for pos in grabable_positions:
                for mol in self.level.molecules:
                    if mol not in self.grabbed_molecules:
                        if mol.position.x == pos[0] and mol.position.y == pos[1]:
                            new_grababble.append(mol)
            molecule.position.x = new_x
            molecule.position.y = new_y
        return new_grababble



    def goal_achieved():
        return False


class Molecule():
    def __init__(self, char, x, y):
        self.is_player = False
        if char.isupper():
            self.is_player = True
            char = char.lower()

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

        self.already_moved_this_round = False
    
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
    def __init__(self):
        self.walls = []
        self.molecules = []
        self.player = None
        
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
    def load_level_from_string(self, width, height, string):
        if len(string) < (width*height):
            print ("Level size is incorrect")
            # handle error
        
        self.width = width
        self.height = height

        self.walls = [[0] * width for i in range(0, height)]
        self.molecules = []

        for y in range(0, height):
            for x in range(0, width):
                index = width * y + x

                if string[index] == 'X':
                    self.walls[y][x] = 1
                elif string[index] == 'C':
                    self.player = Molecule(string[index], x, y)
                elif string[index] != ' ':
                    self.molecules.append(Molecule(string[index], x, y))
        self.molecules.append(self.player)

    def get_mol_pos(self, position):
        for molecule in self.molecules:
            if molecule.position == position:
                return molecule
        return None
                
