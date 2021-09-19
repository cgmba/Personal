"""
Define nodes of search tree and vanilla bfs search algorithm
__author__: Tony Lindgren, Longho Bernard Che, Mba Godwin
"""
import queue
import time

#from utils import RunningStats

"""
Utility functions for lab1
__author__: "Bernard Longho <lobe2042@student.su.se>"
"""


class RunningStats:
    """
    A class to hold the running statistics
    """

    def __init__(self, algorithm: str, duration: float, depth: int, nodes: int, cost: int) -> None:
        """Initialized the running statistics
        Args:
            duration (float): the time taken for the algorithm to reach a solution
            depth (int): the depth reached before a solution could be found
            nodes (int): the number of nodes generated 
            cost (int): the number of nodes in path until a solution is reached 
        """
        self.algorithm = algorithm
        self.duration = duration
        self.depth = depth
        self.nodes = nodes
        self.cost = cost
        self.branching_factor = pow(self.nodes, 1 / depth)

    def __str__(self) -> str:
        """A string representation of the running stats. This allows the object to be printed like
        running_stats = RunningStats(value, value....)
        
        print(running_stats)
        Returns:
            str: string representation of this class
        """
        return "\n--------------------------------\n" \
               f"Statistics for {self.algorithm}\n" \
               f"Elapsed time (s): {self.duration}\n" \
               f"Solution found at depth: {self.depth}\n" \
               f"Number of nodes explored: {self.nodes}\n" \
               f"Cost of solution: {self.cost}\n" \
               f"Estimated effective branching factor: {self.branching_factor}\n" \
               "--------------------------------\n"

    def save_to_file(self, filename: str) -> None:
        """Save the statistics in a file 
        Args:
            filename (str): the file for saving the statistics into 
        """
        with open(file=filename, mode="wb", encoding="utf-8") as file:
            file.write(self.__str__())

class Node:
    """
    This class defines nodes in search trees. It keep track of:
    state, cost, parent, action, and depth
    """

    def __init__(self, state, cost=0, parent=None, action=None):
        self.parent = parent
        self.state = state
        self.action = action
        self.cost = cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def goal_state(self):
        return self.state.check_goal()

    def get_state(self):
        return self.state

    def successor(self):
        successors = queue.Queue()
        for action in self.state.action:
            child = self.state.move(action)
            if child is not None:
                childNode = Node(child, self.cost + 1, self, action)
                successors.put(childNode)
        return successors

    def get_solution_path(self):
        """
        Retrieve the solution path in a reversed fashion
        """
        node, path = self, []
        while node:
            path.append(node)
            node = node.parent
        return [[node.action, node.state.state] for node in path[::-1][1:]]

    def pretty_print_solution(self, verbose=False):
        """
        Prints out the actions needed to go from start to goal
        If verbose is set to true, both the actions and states will be printed.
        """
        path = self.get_solution_path()
        for action in path:
            print(f"action: {action[0]}")
            if verbose:
                print("----------------------------")
                print(" #miss on left bank: ", action[1][0][0])
                print(" #cann on left bank: ", action[1][0][1])
                print("            boat is: ", action[1][1])
                print("#miss on right bank: ", action[1][2][0])
                print("#cann on right bank: ", action[1][2][1])
                print("----------------------------")


class SearchAlgorithm:
    """
    Class for search algorithms, call it with a defined problem
    """

    def __init__(self, problem, check_visited=False):
        self.start = Node(problem)
        self.running_stats = None
        self.check_visited_nodes =check_visited

    def bfs(self, statistics=False):
        start_time = time.process_time()
        frontier = queue.Queue()
        frontier.put(self.start)
        explored = []
        stop = False
        while not stop:
            if frontier.empty():
                return None
            curr_node = frontier.get()
            if curr_node.goal_state():
                stop = True
                if statistics:
                    stop_time = time.process_time()
                    cpu_time = stop_time - start_time
                    nodes_explored = len(explored) if self.check_visited_nodes else frontier.qsize()
                    self.running_stats = RunningStats(algorithm="bfs", duration=cpu_time, depth=curr_node.depth,
                                                      nodes=nodes_explored, cost=curr_node.cost)
                return curr_node

            if self.check_visited_nodes:
                curr_state = curr_node.get_state()
                if curr_state not in explored:
                    explored.append(curr_state)
                    successor = curr_node.successor()
                    while not successor.empty():
                        frontier.put(successor.get())
            else:
                successor = curr_node.successor()
                while not successor.empty():
                    frontier.put(successor.get())


    def dfs(self, statistics=False):
        visited = {}
        visited[str(self.start.state.state)] = True
        start_time = time.process_time()
        frontier = queue.LifoQueue()
        frontier.put(self.start)
        explored = []
        stop = False
        while not stop:
            if frontier.empty():
                return None
            curr_node = frontier.get()
            if curr_node.goal_state():
                stop = True
                if statistics:
                    stop_time = time.process_time()
                    cpu_time = stop_time - start_time
                    nodes_explored = len(explored) if self.check_visited_nodes else frontier.qsize()
                    self.running_stats = RunningStats(algorithm="dfs", duration=cpu_time, depth=curr_node.depth,
                                                      nodes=nodes_explored, cost=curr_node.cost)
                return curr_node

            if self.check_visited_nodes:
                curr_state = curr_node.get_state()
                if curr_state not in explored:
                    explored.append(curr_state)
                    successor = curr_node.successor()
                    while not successor.empty():
                        frontier.put(successor.get())
            else:
                successor = curr_node.successor()
                while not successor.empty():
                    node = successor.get()
                    if str(node.state.state) not in visited.keys():
                        frontier.put(node)
                        visited[str(node.state.state)] = True


    def statistics(self):
        """
        Informs the user about
        - depth, d
        - search cost (number of nodes generated)
        - cost of solution (# of nodes from root to goal, N)
        - cpu time
        - effective branching factor (N^(1/d))
        """
        if self.running_stats is not None:
            print(self.running_stats)
            
            
    