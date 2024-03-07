import pygame
import sys
import time

from draw import *
from game import *
from algorithms import *


def handle_input(gamestate):
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            gamestate.player_try_to_move(UP)
        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
            gamestate.player_try_to_move(DOWN)
        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
            gamestate.player_try_to_move(LEFT)
        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            gamestate.player_try_to_move(RIGHT)
        elif event.key == pygame.K_r:
            gamestate.reset()
            return
        elif event.key == pygame.K_ESCAPE :
            pygame.quit()
            sys.exit()
            
def show_algorithms(game_states):
    print(len(game_states))
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((650, 650))

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    for state in game_states:
        surface.fill((250,250,250))
        draw_screen(state, surface)
        screen.blit(surface, (0,0))
        pygame.display.update()
        time.sleep(0.5)  # 2-second delay between moves


def main():

    gamestate = GameState()
    gamestate.load_level_from_string(13, 13,  "XXXXXXXXXXXXX"
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


    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((650, 650))

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()


    
    result = breadth_first_search(gamestate, surface, screen)
    print(len(result))
    show_algorithms(result)

    


    # while (True):
    #     surface.fill((250,250,250))
    #     draw_screen(gamestate, surface)
    #     screen.blit(surface, (0,0))
    #     pygame.display.update()

    #     handle_input(gamestate)
    #     print(gamestate.is_goal_achieved())


main()
