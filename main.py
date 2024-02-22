import pygame
import sys

import draw

UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GameState:
    def __init__(self):
        self.player_pos = Position(6,6)

    def reset(self):
        self.__init__()
    
    def try_to_move(self, direction):
        self.player_pos.x += direction[0]
        self.player_pos.y += direction[1]


def handle_input(gamestate):
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            gamestate.try_to_move(UP)
        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
            gamestate.try_to_move(DOWN)
        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
            gamestate.try_to_move(LEFT)
        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            gamestate.try_to_move(RIGHT)
        elif event.key == pygame.K_r:
            gamestate.reset()
            return
        elif event.key == pygame.K_ESCAPE :
            pygame.quit()
            sys.exit()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((650, 650))

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    gamestate = GameState()

    while (True):
        surface.fill((250,250,250))
        draw.draw_screen(gamestate, surface)
        screen.blit(surface, (0,0))
        pygame.display.update()

        handle_input(gamestate)

main()