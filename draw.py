import pygame

def draw_player(gamestate, surface):
    pass

def draw_walls(gamestate, surface):
    for y in range(0, gamestate.board_height):
        for x in range(0, gamestate.board_width):
            if gamestate.walls[y][x] != 0:
                pygame.draw.rect(surface, (20,20,200), (x*50, y*50, 50,50))

def draw_atoms(gamestate, surface):
    for y in range(0, gamestate.board_height):
        for x in range(0, gamestate.board_width):
            if gamestate.atoms[y][x] != None:
                atom = gamestate.atoms[y][x]
                if gamestate.atoms[y][x].is_player:
                    pygame.draw.circle(surface, (200,200,20), (x*50 + 25, y*50 + 25), 20)

                    pygame.draw.rect(surface, (0,0,0), (x*50, y*50 - 50, 50,50), 1)
                    pygame.draw.rect(surface, (0,0,0), (x*50, y*50 + 50, 50,50), 1)
                    pygame.draw.rect(surface, (0,0,0), (x*50 - 50, y*50, 50,50), 1)
                    pygame.draw.rect(surface, (0,0,0), (x*50 + 50, y*50, 50,50), 1)
                else:
                    pygame.draw.circle(surface, (200,20,20), (x*50 + 25, y*50 + 25), 20)

                if atom.grabbed_up != None:
                    pygame.draw.rect(surface, (0,0,0), (x*50 + 20, y*50 - 20, 10, 30))
                if atom.grabbed_down != None:
                    pygame.draw.rect(surface, (0,0,0), (x*50 + 20, y*50 + 30, 10, 30))
                if atom.grabbed_left != None:
                    pygame.draw.rect(surface, (0,0,0), (x*50 - 20, y*50 + 20, 30, 10))
                if atom.grabbed_right != None:
                    pygame.draw.rect(surface, (0,0,0), (x*50 + 30, y*50 + 20, 30, 10))

def draw_screen(gamestate, surface):
    draw_walls(gamestate, surface)
    draw_atoms(gamestate, surface)
    draw_player(gamestate, surface)