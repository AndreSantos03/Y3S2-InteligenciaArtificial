import pygame

def draw_player(gamestate, surface):
    rect = pygame.Rect(gamestate.player_pos.x*50, gamestate.player_pos.y*50, 50,50)
    pygame.draw.rect(surface, (200,200,20), rect)

def draw_screen(gamestate, surface):
    #draw_board()
    draw_player(gamestate, surface)