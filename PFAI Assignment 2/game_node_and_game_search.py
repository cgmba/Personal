'''
Definitions for GameNode, GameSearch and MCTS

Author: Tony Lindgren
Student: Godwin Mba
'''
from time import process_time
import random
#from random import *
#from random import choice
import math


class GameNode:
    '''
    This class defines game nodes in game search trees. It keep track of: 
    state
    '''
    def __init__(self, state, node=None, parent = None, parent_action = None):
        self.state = state 
        
     
        self.parent = parent
        self.parent_action = parent_action
        self.no_of_visits = 0    
        self.node_wins = 0
        self.untried_moves = self.state.actions()  
        self.children= []

    # def children(self):
    #     children = []
    #     for action in self.state.actions():
    #         child = self.state.result(action)
    #         if child is not None:
    #             childNode = GameNode(child, self, action)
    #             children.append(childNode)
    #     return children

    def node_children(self, children):
        
        children_ubc1 = {}  
        for child in children:
            children_ubc1[child] = child.ucb1_calculator()            
        return max(children_ubc1, key=children_ubc1.get)

    def most_visited(self, children):
        
        children_visit = {}
        for child in children:
            children_visit[child] = child.no_of_visits 
            return max(children_visit, key=children_visit.get)

    def ucb1_calculator(self):
        ucb1 = self.node_wins / self.no_of_visits  + math.sqrt(2) * math.sqrt(math.log(self.parent.no_of_visits) / self.no_of_visits)
        return ucb1  
    

    def is_terminal_node(self):
        stop, value = self.state.is_terminal()
        return stop, value


class GameSearch:
    '''
    Class containing different game search algorithms, call it with a defined game/node
    '''                 
    def __init__(self, game, depth=3, time=0):
        self.state = game       
        self.depth = depth
        self.time = time

    def mcts(self):                     
        start_time = process_time() 
        tree = GameNode(self.state)
        tree.actions_left = tree.state.actions()   
        elapsed_time = 0
        while elapsed_time < self.time:   
            leaf = self.select(tree)
            child = self.expand(leaf)               
            result = self.simulate(child) 
            self.back_propagate(result, child)         
            stop_time = process_time()
            elapsed_time = stop_time - start_time
        move = self.actions(tree)
        return move

    def select(self, node):
        
        # if node.untried_moves == []:
        #     node = node.node_children(node.children())
        #     return self.select(node)
        while node.untried_moves == []:
            node = node.node_children(node.children)
        return node

    def expand(self, node):
        
        # terminal, value = node.state.is_terminal()
        # if not terminal:
        #     action = random.choice(node.untried_moves)
        #     node.untried_moves.remove(action)
        #     next_move = node.state.result(action)
        #     child_move = GameNode(state=next_move, parent=node, action=action)
        #     node.children.append(child_move)
        #     return child_move
        # return node

        stop, _ = node.state.is_terminal()
        if stop != True:
            action = random.choice(node.untried_moves)
            node.untried_moves.remove(action)
            next_state = node.state.result(action)
            child = GameNode(state=next_state, parent=node, parent_action=action)
            node.children.append(child)
            return child
        return node 

    def simulate(self, node):
        
        present_state = node.state
        stop, value = present_state.is_terminal()
        while not stop:
            action = random.choice(present_state.actions()) 
            present_state = present_state.result(action)
            stop, value = present_state.is_terminal()

        if value == 0:
            return None
        if present_state.to_move() == 'r':
            winning_chip = 'w'
        else:
            winning_chip = 'r'
        return winning_chip

    def back_propagate(self, result, node):
        

        while node != None:
            if result == node.state.to_move():
                node.no_of_visits += 1
                node.node_wins += 1
            else:
                node.no_of_visits += 1
            node = node.parent
    
    
    
    def actions(self, node):
        children = node.children        
        most_visited_node = node.most_visited(children)
        
        
        return most_visited_node.parent_action 
        


    
    # def minimax_search(self): 
    #     start_time = process_time()   
    #     _, move = self.max_value(self.state, self.depth)  
    #     return move
    
    # def max_value(self, state, depth):
    #     move = None
    #     terminal, value = state.is_terminal()
    #     if terminal or depth == 0:
    #         return value, None
    #     v = -100000
    #     actions = state.actions()
    #     for action in actions: 
    #         new_state = state.result(action)
    #         v2, _ = self.min_value(new_state, depth - 1)
    #     if v2 > v:
    #         v = v2
    #         move = action
    #     return v, move
    
    # def min_value(self, state, depth):
    #     move = None
    #     terminal, value = state.is_terminal()
    #     if terminal or depth == 0:
    #         return value, None  
    #     v = 100000
    #     actions = state.actions()
    #     for action in actions: 
    #         new_state = state.result(action)
    #         v2, _ = self.max_value(new_state, depth - 1)
    #         if v2 < v:
    #             v = v2
    #             move = action
    #     return v, move


    def minimax_search(self): 
        start_time = process_time()   
        _, move = self.max_value(self.state, self.depth, start_time, alpha = -math.inf, beta = +math.inf)  
        return move
    
    def max_value(self, state, depth, start_time, alpha, beta):
        end_time = process_time()
        move = None
        terminal, value = state.is_terminal()
        if self.time < (end_time - start_time):
            return value, None
        if terminal or depth == 0:
            if terminal:
                return value, None
            else:
                heuristic = state.eval(state, state.curr_move)
            return heuristic, None
        v = -100000
        actions = state.actions()
        for action in actions: 
            new_state = state.result(action)
            v2, _ = self.min_value(new_state, depth - 1, start_time, alpha, beta)
        if v2 > v:
            v = v2
            move = action
            alpha = max(alpha, v)
        if v > beta:
               return v, move
        return v, move
    
    def min_value(self, state, depth, start_time, alpha, beta):
        end_time = process_time()
        move = None
        terminal, value = state.is_terminal()
        if self.time < (end_time - start_time):
            return value, None
        if terminal or depth == 0:
            if terminal:
                return value, None
            else:
                heuristic = state.eval(state, state.curr_move)
                return heuristic, None  
        v = 100000
        actions = state.actions()
        for action in actions: 
            new_state = state.result(action)
            v2, _ = self.max_value(new_state, depth - 1, start_time, alpha, beta)
            if v2 < v:
                v = v2
                move = action
                beta = min(beta, v)
            if v < alpha:
                return v, move
        return v, move