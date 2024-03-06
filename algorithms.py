from game import GameState

moves = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

def bfs(unvisited,visited): 

    current_state = unvisited[0]
    unvisited = unvisited[1:]
    visited.append(current_state)

    if current_state.goal_achieved():
        return visited
    
    else:
        next_states = []
        for move in moves:
            next_states.append(GameState.try_to_move)

