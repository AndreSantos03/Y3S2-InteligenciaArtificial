import pygame

def draw_player(gamestate, surface):
    pygame.draw.circle(surface, (200,200,20), (gamestate.player.position.x*50 + 25, gamestate.player.position.y*50 + 25), 20)

    pygame.draw.rect(surface, (0,0,0), (gamestate.player.position.x*50, gamestate.player.position.y*50 - 50, 50,50), 1)
    pygame.draw.rect(surface, (0,0,0), (gamestate.player.position.x*50, gamestate.player.position.y*50 + 50, 50,50), 1)
    pygame.draw.rect(surface, (0,0,0), (gamestate.player.position.x*50 - 50, gamestate.player.position.y*50, 50,50), 1)
    pygame.draw.rect(surface, (0,0,0), (gamestate.player.position.x*50 + 50, gamestate.player.position.y*50, 50,50), 1)

def draw_walls(gamestate, surface):
    for y in range(0, gamestate.level.height):
        for x in range(0, gamestate.level.width):
            if gamestate.level.walls[y][x] != 0:
                pygame.draw.rect(surface, (20,20,200), (x*50, y*50, 50,50))

def draw_molecules(gamestate, surface):
    for y in range(0, gamestate.level.height):
        for x in range(0, gamestate.level.width):
            if gamestate.level.molecules[y][x] != None:
                pygame.draw.circle(surface, (200,20,20), (x*50 + 25, y*50 + 25), 20)

def draw_screen(gamestate, surface):
    draw_walls(gamestate, surface)
    draw_molecules(gamestate, surface)
    draw_player(gamestate, surface)