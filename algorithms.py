from game import *
from collections import deque
import copy

moves = { UP, DOWN, LEFT, RIGHT}

def get_all_states(original_gamestate):
    gamestates = []
    for move in moves:
        copy_gamestate = copy.deepcopy(original_gamestate)
        copy_gamestate.player_try_to_move(move)
        gamestates.append(copy_gamestate)
    return gamestates
            
        

def breadth_first_search(initial_state):

    q = deque([initial_state])
    visited = {initial_state: None}

    while len(q) != 0:
        current_state = q.popleft()
        
        if current_state.is_goal_achieved():
            path = []
            while current_state:
                path.append(current_state)
                current_state = visited[current_state]  
            path.reverse()
            return path
        for state in get_all_states(current_state):
            if state not in visited:
                visited[state] = current_state
                q.append(state)
    
    return []




