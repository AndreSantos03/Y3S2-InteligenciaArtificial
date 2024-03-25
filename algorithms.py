from game import *
from draw import *

from collections import deque
import heapq


class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost


    def is_goal_state(self):

        return self.state.is_goal_achieved()

    

    def get_path(self):
        path = []
        current_node = self
        while current_node.parent is not None:
            path.append((current_node.action, current_node.state)) 
            current_node = current_node.parent
        path.reverse()
        return path
    
    def __lt__(self, other):
        # Compare nodes based on their costs
        return self.cost < other.cost
    

    
def get_child_states(parent_state):
    child_states = []

    for direction in [DOWN, LEFT, RIGHT, UP]:
        child_state = copy.deepcopy(parent_state)
        if child_state.try_to_move_atom(child_state.get_player(), direction):
            child_state.player_try_to_move(direction)
            child_states.append((child_state,direction))

    return child_states

def search_heuristic(state):
    player_position = state.get_player().position
    min_distance = sys.maxsize 

    for atom_row in state.atoms:
        for atom in atom_row:
            if atom is not None:
                distance = player_position.distance(atom.position)
                min_distance = min(min_distance, distance)

    return min_distance



def dfs(initial_state):
    stack = [Node(initial_state)]
    visited = set()  # Initialize an empty set for visited states
    visited.add(initial_state)  # Add the initial state to the set
    while stack:
        current_node = stack.pop()
        current_state = current_node.state
        if current_state.is_goal_achieved():
            return current_node.get_path()
        for child_state, direction in get_child_states(current_node.state):
            if child_state in visited:
                continue
            else:
                visited.add(child_state)  # Add the child state to the visited set
            child_node = Node(child_state, parent=current_node, action=direction)
            stack.append(child_node)
    return None, None


def bfs(initial_state):
    queue = deque([Node(initial_state)])
    visited = set()

    while queue:
        current_node = queue.popleft()
        current_state = current_node.state
        if current_state.is_goal_achieved():
            return current_node.get_path()
        for child_state, direction in get_child_states(current_node.state):
            if child_state not in visited:
                visited.add(child_state)
                child_node = Node(child_state,parent=current_node,action=direction)
                queue.append(child_node)
    return None


def ids(initial_state, max_depth):
    for depth in range(max_depth):
        result = recursive_dls(Node(initial_state),depth)
        if result is not None:
            return result
    return None


def recursive_dls(node, depth_limit):
    state = node.state
    if state.is_goal_achieved():
        return node.get_path()
    elif depth_limit == 0:
        return None
    else:
        cutoff_occurred = False
        for child_state, direction in get_child_states(state):
            child_node = Node(child_state, parent=node, action=direction)
            result = recursive_dls(child_node, depth_limit - 1)
            if result == 'cutoff':
                cutoff_occurred = True
            elif result is not None:
                return result
        if cutoff_occurred:
            return 'cutoff'
        else:
            return None
        
def greedy_search(initial_state):
    visited = set() 
    frontier = [(Node(initial_state), search_heuristic(initial_state))]

    while frontier:
        current_node, _ = frontier.pop(0)
        current_state = current_node.state
        if current_state.is_goal_achieved():
            return current_node.get_path()
        
        visited.add(current_state)

        for child_state, direction in get_child_states(current_state):
            if child_state not in visited:
                child_node = Node(child_state, parent=current_node, action=direction)
                frontier.append((child_node, search_heuristic(child_state)))
            
        frontier.sort(key=lambda x: x[1]) 
    
    return None


def a_star_search(initial_state):
    visited = set()
    frontier = [(search_heuristic(initial_state), 0, Node(initial_state))]  # Priority queue: (heuristic, actual_cost, node)
    heapq.heapify(frontier)  # Convert frontier list into a heap

    while frontier:
        _, actual_cost, current_node = heapq.heappop(frontier)  # Pop the node with the lowest total cost
        current_state = current_node.state
        if current_state.is_goal_achieved():
            return current_node.get_path()

        visited.add(current_state)

        for child_state, direction in get_child_states(current_state):
            if child_state not in visited:
                child_node = Node(child_state, parent=current_node, action=direction)
                child_actual_cost = actual_cost + 1  
                child_heuristic = search_heuristic(child_state)
                total_cost = child_actual_cost + child_heuristic
                heapq.heappush(frontier, (total_cost, child_actual_cost, child_node))


    
    return None

    
    
        