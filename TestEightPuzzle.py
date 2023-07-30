import unittest

from eight_puzzle import EightPuzzle


init_state = [[7, 2, 4], [5, 'e', 6], [8, 3, 1]]
goal_state = [['e', 1, 2], [3, 4, 5], [6, 7, 8]]


class EightPuzzleTestClass(EightPuzzle):
    """
    This class is a wrapper for the EightPuzzle Class
    It avoids specifying the goal state in every test.
    """

    def __init__(self, initial_state, goal=None):
        if goal is None:
            goal = goal_state
        super().__init__(initial_state, goal)


class TestEightPuzzle(unittest.TestCase):

    def test_h1(self):
        ep = EightPuzzleTestClass(initial_state=init_state)
        self.assertEqual(ep.h_1(), 8, "The number of tiles out of place should be 8")

    def test_h2(self):
        ep = EightPuzzleTestClass(initial_state=init_state)
        self.assertEqual(ep.h_2(), 18, "The manhattan distance should be 18")

    def test_goal_state(self):
        ep = EightPuzzleTestClass(initial_state=init_state)
        self.assertEqual(ep.check_goal(), False, "The goal state should return false")

        ep_goal = EightPuzzleTestClass(initial_state=goal_state)

        self.assertEqual(ep_goal.check_goal(), True, "The goal state should be true")

    # =========== start test of up move ======================
    def test_up_from_goal_state(self):
        # 1. No move in goal state
        ep = EightPuzzleTestClass(initial_state=goal_state)
        ep.up()
        self.assertEqual(ep.state, goal_state, "Up should not work when it has reached the goal state")

    def test_legal_up_move(self):
        # 2. Legal move
        ep_legal = EightPuzzleTestClass(initial_state=[[7, 2, 4], [5, 'e', 6], [8, 3, 1]])
        ep_legal.up()
        expected = [[7, 2, 4], [5, 3, 6], [8, 'e', 1]]
        self.assertEqual(ep_legal.state, expected,
                         f"An up move [legal] from {init_state} should give {expected}")

    def test_illegal_up_move(self):
        # 3. Illegal move
        illegal_state = [[7, 2, 4], [5, 3, 6], [8, 'e', 1]]
        ep_illegal = EightPuzzleTestClass(initial_state=illegal_state)
        ep_illegal.up()
        self.assertEqual(ep_illegal.state, illegal_state,
                         f"A down move from this state[illegal] {ep_illegal} should give {illegal_state}")

    # ******** end of up move ******
    # ==================== Down move tests ==================
    def test_down_from_legal_state(self):
        # 1. Goal state should not move
        ep = EightPuzzleTestClass(initial_state=goal_state)
        result = ep.down()
        print(f"Result of up from goal state is {result}")
        self.assertEqual(ep.state, goal_state,
                         f"A goal down move from {init_state} should give {ep.state}")

    def test_legal_down_move(self):
        # 2. Legal move
        ep_legal = EightPuzzleTestClass(initial_state=init_state)
        ep_legal.down()
        expected_state = [[7, 'e', 4], [5, 2, 6], [8, 3, 1]]
        self.assertEqual(ep_legal.state, expected_state,
                         f"A correct down move from {init_state} should give {expected_state}")

    def test_illegal_down_move(self):
        # 3. Illegal move, state remains the same
        state_with_illegal_down = [[7, 'e', 4], [5, 2, 6], [8, 3, 1]]
        ep_illegal = EightPuzzleTestClass(initial_state=state_with_illegal_down)
        bad_result = ep_illegal.down()
        self.assertEqual(ep_illegal.state, state_with_illegal_down,
                         f"A wrong down move from {state_with_illegal_down} should give {state_with_illegal_down} with "
                         f"result {bad_result}")

    # ***************************** End test of down move*******************************

    # ====================== Test left move =====================
    def test_left_from_goal_state(self):
        # 1. Goal state should not move
        ep = EightPuzzleTestClass(initial_state=goal_state)
        ep.left()
        self.assertEqual(ep.state, goal_state)

    # 2. Legal move
    def test_legal_left_move(self):
        ep_legal = EightPuzzleTestClass(initial_state=[[7, 2, 4], [5, 'e', 6], [8, 3, 1]])
        ep_legal.left()
        expected_state = [[7, 2, 4], [5, 6, 'e'], [8, 3, 1]]
        self.assertEqual(ep_legal.state, expected_state,
                         f"A  left move [legal] from {ep_legal.state} should give {expected_state}")

    # 3. Illegal move
    def test_illegal_left_move(self):
        state_with_illegal_left = [['e', 2, 4], [5, 6, 7], [8, 3, 1]]
        ep_illegal = EightPuzzleTestClass(initial_state=state_with_illegal_left)
        ep_illegal.left()
        self.assertEqual(ep_illegal.state, state_with_illegal_left,
                         f"A  left [illegal] move from {state_with_illegal_left} should give {state_with_illegal_left}")

    # ******************** END OF LEFT MOVE TESTS*************************************

    # =========== RIGHT MOVE TESTS ==========================
    def test_right_from_goal_state(self):
        # 1. No move in goal state
        ep = EightPuzzleTestClass(initial_state=goal_state)
        ep.right()
        self.assertEqual(ep.state, goal_state)

    def test_legal_right_move(self):
        # 2. Legal move
        ep_legal = EightPuzzleTestClass(initial_state=[[7, 2, 4], [5, 'e', 6], [8, 3, 1]])
        ep_legal.right()
        expected_state = [[7, 2, 4], ['e', 5, 6], [8, 3, 1]]
        self.assertEqual(ep_legal.state, expected_state,
                         f"A right move from {[[7, 2, 4], [5, 'e', 6], [8, 3, 1]]} should give {expected_state}")

    def test_illegal_right_ove(self):
        # 3. Illegal move
        state_with_illegal_right = [[7, 2, 4], [5, 6, 'e'], [8, 3, 1]]
        ep_illegal = EightPuzzleTestClass(initial_state=state_with_illegal_right)
        ep_illegal.right()
        self.assertEqual(ep_illegal.state, state_with_illegal_right,
                         f"A right move from {state_with_illegal_right} should give {state_with_illegal_right}")


# *************** End test of right move *************************

if __name__ == '__main__':
    unittest.main()