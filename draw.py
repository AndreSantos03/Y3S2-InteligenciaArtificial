import pygame

def draw_player(gamestate, surface):
    pass

def draw_walls(gamestate, surface):
    for y in range(0, gamestate.level.height):
        for x in range(0, gamestate.level.width):
            if gamestate.level.walls[y][x] != 0:
                pygame.draw.rect(surface, (20,20,200), (x*50, y*50, 50,50))

def draw_molecules(gamestate, surface):
    for molecule in gamestate.level.molecules:
        # Access the position of the molecule
        molecule_position = molecule.position
        pos_x = molecule_position.x * 50 + 25
        pos_y = molecule_position.y * 50 + 25
                
        if molecule.is_player:
            pygame.draw.circle(surface, (200,200,20), (pos_x, pos_y), 20)
            pygame.draw.rect(surface, (0,0,0), (pos_x - 25, pos_y - 25, 50, 50), 1)
        else:
            pygame.draw.circle(surface, (200,20,20), (pos_x, pos_y), 20)
                
        if molecule.grabbed_up is not None:
            pygame.draw.rect(surface, (0,0,0), (pos_x + 20, pos_y - 30, 10, 30))
        if molecule.grabbed_down is not None:
            pygame.draw.rect(surface, (0,0,0), (pos_x + 20, pos_y, 10, 30))
        if molecule.grabbed_left is not None:
            pygame.draw.rect(surface, (0,0,0), (pos_x - 30, pos_y + 20, 30, 10))
        if molecule.grabbed_right is not None:
            pygame.draw.rect(surface, (0,0,0), (pos_x, pos_y + 20, 30, 10))

def draw_screen(gamestate, surface):
    draw_walls(gamestate, surface)
    draw_molecules(gamestate, surface)
    draw_player(gamestate, surface)