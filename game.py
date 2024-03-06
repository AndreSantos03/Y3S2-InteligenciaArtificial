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
        self.grabbed_atoms = []

    def reset(self):
        self.__init__()

    def get_player(self):
        for y in range(0, self.level.height):
            for x in range(0, self.level.width):
                if self.level.temp_atoms[y][x] != None:
                    if self.level.temp_atoms[y][x].is_player:
                        return self.level.temp_atoms[y][x]
        return None


    def try_to_grab(self, atom):
        if atom == None:
            return

        if self.level.temp_atoms[atom.position.y - 1][atom.position.x] != None and atom.grabbed_up != self.level.temp_atoms[atom.position.y - 1][atom.position.x] and self.level.temp_atoms[atom.position.y - 1][atom.position.x].grabbed_down != atom:
            atom.grabbed_up = self.level.temp_atoms[atom.position.y - 1][atom.position.x]
            self.level.temp_atoms[atom.position.y - 1][atom.position.x].grabbed_down = atom
        if self.level.temp_atoms[atom.position.y + 1][atom.position.x] != None and atom.grabbed_down != self.level.temp_atoms[atom.position.y + 1][atom.position.x] and self.level.temp_atoms[atom.position.y + 1][atom.position.x].grabbed_up != atom:
            atom.grabbed_down = self.level.temp_atoms[atom.position.y + 1][atom.position.x]
            self.level.temp_atoms[atom.position.y + 1][atom.position.x].grabbed_up = atom
        if self.level.temp_atoms[atom.position.y][atom.position.x - 1] != None and atom.grabbed_left != self.level.temp_atoms[atom.position.y][atom.position.x - 1] and self.level.temp_atoms[atom.position.y][atom.position.x - 1].grabbed_right != atom:
            atom.grabbed_left = self.level.temp_atoms[atom.position.y][atom.position.x - 1]
            self.level.temp_atoms[atom.position.y][atom.position.x - 1].grabbed_right = atom
        if self.level.temp_atoms[atom.position.y][atom.position.x + 1] != None and atom.grabbed_right != self.level.temp_atoms[atom.position.y][atom.position.x + 1] and self.level.temp_atoms[atom.position.y][atom.position.x + 1].grabbed_left != atom:
            atom.grabbed_right = self.level.temp_atoms[atom.position.y][atom.position.x + 1]
            self.level.temp_atoms[atom.position.y][atom.position.x + 1].grabbed_left = atom

    def move_atom(self, atom, direction):
        if atom.already_moved_this_round:
            return False
        atom.already_moved_this_round = True
        
        self.level.temp_atoms[atom.position.y][atom.position.x] = None
        atom.position.x += direction[0]
        atom.position.y += direction[1]
        self.level.temp_atoms[atom.position.y][atom.position.x] = atom

        if atom.grabbed_up != None and direction != UP:
            self.try_to_move_atom(atom.grabbed_up, direction)
        if atom.grabbed_down != None and direction != DOWN:
            self.try_to_move_atom(atom.grabbed_down, direction)
        if atom.grabbed_left != None and direction != LEFT:
            self.try_to_move_atom(atom.grabbed_left, direction)
        if atom.grabbed_right != None and direction != RIGHT:
            self.try_to_move_atom(atom.grabbed_right, direction)
    
    def try_to_move_atom(self, atom, direction):
        if (self.level.walls[atom.position.y + direction[1]][atom.position.x + direction[0]] == 0):
            next_atom = self.level.temp_atoms[atom.position.y + direction[1]][atom.position.x + direction[0]]
            if (next_atom != None):
                if not self.try_to_move_atom(next_atom, direction):
                    return False
            self.move_atom(atom, direction)
            return True
        return False
    
    def player_try_to_move(self, direction):
        self.level.atoms = self.level.temp_atoms

        player = self.get_player()
        if self.try_to_move_atom(self.get_player(), direction):
            player.verify_grabs(self.level.temp_atoms)
            self.try_to_grab(player)
            for y in range(0, self.level.height):
                for x in range(0, self.level.width):
                    if self.level.temp_atoms[y][x] != None:
                        self.level.temp_atoms[y][x].already_moved_this_round = False
                        self.level.temp_atoms[y][x].verify_grabs(self.level.temp_atoms)
                        self.try_to_grab(self.level.temp_atoms[y][x])



    def is_goal_achieved(self):
        for y in range(0, self.level.height):
            for x in range(0, self.level.width):
                atom = self.level.temp_atoms[y][x]
                if atom != None:
                    if atom.grabbed_up != None or atom.grabbed_down != None or atom.grabbed_left != None or atom.grabbed_right != None:
                        return True
        return False


class Atom():
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
    
    def verify_grabs(self, atoms):
        if self.grabbed_up != None and self.grabbed_up != atoms[self.position.y - 1][self.position.x]:
            self.grabbed_up.grabbed_down = None
            self.grabbed_up = None
        if self.grabbed_down != None and self.grabbed_down != atoms[self.position.y + 1][self.position.x]:
            self.grabbed_down.grabbed_up = None
            self.grabbed_down = None
        if self.grabbed_left != None and self.grabbed_left != atoms[self.position.y][self.position.x - 1]:
            self.grabbed_left.grabbed_right = None
            self.grabbed_left = None
        if self.grabbed_right != None and self.grabbed_right != atoms[self.position.y][self.position.x + 1]:
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
        self.atoms = [[None] * width for i in range(0, height)]

        for y in range(0, height):
            for x in range(0, width):
                index = width * y + x

                if string[index] == 'X':
                    self.walls[y][x] = 1
                elif string[index] != ' ':
                    self.atoms[y][x] = Atom(string[index], x, y)
        
        self.temp_atoms = self.atoms

                    
    def __init__(self):
        self.walls = []
        self.atoms = []
        self.temp_atoms = []

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
