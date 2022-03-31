"""
Eight puzzle solver
@author Bernard Longho, Mba Godwin
"""
from copy import deepcopy

import utils


class EightPuzzle:
    """
    An 8-puzzle solver 
    """
    _empty_symbol = 'e'

    def __init__(self, initial_state, goal):
        self.state = initial_state
        self.goal = goal
        # The different possible directions to move
        self.action = ["up", "down", "left", "right"]

    def check_goal(self):
        return self.state == self.goal

    def move(self, move):
        if move == "up":
            dc = deepcopy(self)
            if dc.up():
                return dc
        elif move == "down":
            dc = deepcopy(self)
            if dc.down():
                return dc
        elif move == "left":
            dc = deepcopy(self)
            if dc.left():
                return dc
        elif move == "right":
            dc = deepcopy(self)
            if dc.right():
                return dc

    def up(self):
        """
        Move one place up
        - There should be no move when it has reached the goal state
        - The puzzle moves one place up if the empty spot is not in the last row
        Returns: True if there is a legal move. Otherwise false
        """
        if self.check_goal():  # Do not move up if this is goal state
            return False
        row, col = self._get_empty_position()
        if row == 2:  # Cannot move up if the empty cell is at the bottom
            return False

        self.state[row][col] = self.state[row + 1][col]
        self.state[row + 1][col] = self._empty_symbol
        return True

    def down(self):
        """
        Move a number down
        - Will not move if it is the goal state
        - Cannot move down if the empty spot is at the top
        Returns: True if move is legal, otherwise false
        """
        if self.check_goal():
            return False

        row, col = self._get_empty_position()

        if row == 0:
            return False

        self.state[row][col] = self.state[row - 1][col]
        self.state[row - 1][col] = self._empty_symbol
        return True

    def left(self):
        """
        Moves a value to the left
        - No move if it is goal state
        - No move if empty cell is in col=0
        Returns: True if legal move. Otherwise false
        """
        if self.check_goal():
            return False

        row, col = self._get_empty_position()

        if col == 0:
            return False

        self.state[row][col] = self.state[row][col + 1]
        self.state[row][col + 1] = self._empty_symbol
        return True

    def right(self):
        """
        Move one place to the right
        - Should not move if goal state
        - Should not move if empty cell is at col=2
        Returns: True if legal move. Otherwise False
        """
        if self.check_goal():
            return False

        row, col = self._get_empty_position()

        if col == 2:
            return False

        self.state[row][col] = self.state[row][col - 1]
        self.state[row][col - 1] = self._empty_symbol
        return True

    def h_1(self):
        """Heuristics that calculates the number of tiles out of place
        Returns(int): the number of tiles out of place
        """
        # Go through current state and check for and count the number of tiles out of place

        num_tiles_out_of_place = 0
        for row in range(3):
            for col in range(3):
                if self.state[row][col] != 'e' and self.state[row][col] != self.goal[row][col]:
                    num_tiles_out_of_place += 1

        return num_tiles_out_of_place

    def h_2(self):
        """Calculate the Manhattan distance
        Returns: The manhattan distance
        -------
        """
        m_distance = 0
        for row in range(3):
            for col in range(3):
                entry = self.state[row][col]
                if str(entry) != 'e':
                    goal_row, goal_col = self._calculated_expected_goal_position(entry)
                    m_distance += abs(goal_row - row) + abs(goal_col - col)

        return m_distance

    def _is_solvable(self):
        inversion = 0
        flattened_state = utils.flatten(self.state)
        for i in range(len(flattened_state)):
            for j in range(i + 1, len(flattened_state)):
                if flattened_state[i] != 'e' and flattened_state[j] != 'e' and flattened_state[i] > flattened_state[j]:
                    inversion += 1

        return inversion % 2 == 0

    def _get_empty_position(self):
        for idx, row in enumerate(self.state):
            for jdx, col in enumerate(row):
                if col == 'e':
                    return idx, jdx
        return None

    def _calculated_expected_goal_position(self, entry):
        for row in range(3):
            for col in range(3):
                if self.goal[row][col] == entry:
                    return row, col
        return None

    def pretty_print(self) -> None:
        """
        Prints the current game state
        Returns: None
        """
        delim = "|"
        for idx, row in enumerate(self.state):
            if self.state[idx][0] == 'e':
                self.state[idx][0] = ' '
            print("-" * 13)
            print(delim, self.state[idx][0], delim, self.state[idx][1], delim,
                  self.state[idx][2], delim)
        print("-" * 13)

    def display(self):
        print(self.state)