import pygame
import sys
import time
import argparse

from draw import *
from game import *
from algorithms import *


direction_strings = {
    UP: "UP",
    DOWN: "DOWN",
    LEFT: "LEFT",
    RIGHT: "RIGHT"
}

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
        elif event.key == pygame.K_h:
            get_hint(gamestate)
        elif event.key == pygame.K_ESCAPE :
            pygame.quit()
            sys.exit()
            
def game_loop(gamestate):
    print("At any point click H to get a Hint!")
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((650, 650))

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    while (True):
        surface.fill((250,250,250))
        draw_screen(gamestate, surface)
        screen.blit(surface, (0,0))
        pygame.display.update()

        handle_input(gamestate)

def get_hint(gamestate):
    _,moves = get_algorithms_results(gamestate)
    print(f"According to the chosen algorithm you should play the move {direction_strings[moves[0]]}")

def get_algorithms_results(initial_gamestate):

    print("Available algorithms:")
    print("1. DFS")
    print("2. BFS")
    print("3. IDS")
    print("4. Greedy Search")
    print("5. A* Search")
    
    choice = input("Enter the number of the algorithm you want to run: ")
    gamestate_result = []
    moves = []
    if choice.isdigit():
        choice = int(choice)
        if choice == 1:
            result = dfs(initial_gamestate)
            for move,state in result:
                moves.append(move)
                gamestate_result.append(state)
        elif choice == 2:
            result = bfs(initial_gamestate)
            for move, state in result:
                moves.append(move)
                gamestate_result.append(state)
        elif choice == 3:
            max_depth = None
            while max_depth is None:
                max_depth_input = input("Enter the maximum depth for IDS: ")
                if max_depth_input.isdigit():
                    max_depth = int(max_depth_input)
                else:
                    print("Invalid input. Please enter a valid integer.")
            result = ids(initial_gamestate, max_depth)
            if result == None:
                print(f"Couldn't find a solution with {max_depth} maximum depth")
            else:
                for move, state in result:
                    moves.append(move)
                    gamestate_result.append(state)
        elif choice == 4:
            result = greedy_search(initial_gamestate)
            for move, state in result:
                moves.append(move)
                gamestate_result.append(state)
        elif choice == 5:
            result = a_star_search(initial_gamestate)
            for move, state in result:
                moves.append(move)
                gamestate_result.append(state)
        else:
            print("Invalid input. Please enter a valid number. ")
    else:
        print("Invalid input. Please enter a number.")

    return gamestate_result,moves

def handle_algorithms(initial_gamestate):
    while True:

        gamestate_result, moves = get_algorithms_results(initial_gamestate)

        interval = None
        while interval is None:
            interval_input = input("Enter the interval in seconds between moves: ")
            try:
                interval = float(interval_input)
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((650, 650))

        surface = pygame.Surface(screen.get_size())
        surface = surface.convert()
        for i in range(len(gamestate_result) - 1): 
            surface.fill((250, 250, 250))
            draw_screen(gamestate_result[i], surface)
            screen.blit(surface, (0, 0))
            print(f"Direction chosen for move number {i + 1}: {direction_strings[moves[i]]}")
            pygame.display.update()
            time.sleep(interval)
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
        pygame.quit()

        




def main(args):

    gamestate = GameState()
    gamestate.load_level_from_string(13, 13,  "XXXXXXXXXXXXX"
                                        "XXXXXX XXXXXX"
                                        "XXXXX C XXXXX"
                                        "XXXX     XXXX"
                                        "XXX       XXX"
                                        "XX  h      XX"
                                        "X           X"
                                        "XX   X     XX"
                                        "XXX       XXX"
                                        "XXXX     XXXX"
                                        "XXXXX   XXXXX"
                                        "XXXXXX XXXXXX"
                                        "XXXXXXXXXXXXX")



    if args.algorithms:
        handle_algorithms(gamestate)
    else:
        game_loop(gamestate)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description of your program")
    parser.add_argument("--algorithms", help="Runs a version of the game where you can watch the game evolve", action='store_true')
    
    args = parser.parse_args()
    main(args)