from game import *
from collections import deque
from draw import *
import pygame
import time

def get_child_states(parent_state):
    child_states = []

    for direction in [DOWN, LEFT, RIGHT, UP]:
        child_state = copy.deepcopy(parent_state)
        if child_state.try_to_move_atom(child_state.get_player(), direction):
            child_state.player_try_to_move(direction)
            child_states.append((child_state,direction))

    return child_states

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
        print(path)
        return path
    


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
