import pygame

def draw_player(gamestate, surface):
    pygame.draw.circle(surface, (200,200,20), (gamestate.player.x*50 + 25, gamestate.player.y*50 + 25), 20)

    pygame.draw.rect(surface, (0,0,0), (gamestate.player.x*50, gamestate.player.y*50 - 50, 50,50), 1)
    pygame.draw.rect(surface, (0,0,0), (gamestate.player.x*50, gamestate.player.y*50 + 50, 50,50), 1)
    pygame.draw.rect(surface, (0,0,0), (gamestate.player.x*50 - 50, gamestate.player.y*50, 50,50), 1)
    pygame.draw.rect(surface, (0,0,0), (gamestate.player.x*50 + 50, gamestate.player.y*50, 50,50), 1)

def draw_walls(gamestate, surface):
    for wall in gamestate.level.walls:
        pygame.draw.rect(surface, (20,20,200), (wall.x*50, wall.y*50, 50,50))

def draw_molecules(gamestate, surface):
    for molecule in gamestate.level.molecules:
        pygame.draw.circle(surface, (200,20,20), (molecule.x*50 + 25, molecule.y*50 + 25), 20)

def draw_screen(gamestate, surface):
    draw_walls(gamestate, surface)
    draw_molecules(gamestate, surface)
    draw_player(gamestate, surface)