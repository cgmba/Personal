"""
Define problem and start execution of search problems


"""
from missionaries_and_cannibals_complete import MissionariesAndCannibals
from node_and_search_complete import SearchAlgorithm
from utils import save_content_to_file as WriteToFile

filename = "Assignment1-Report+Longho_Bernard_Che_and_Mba_Godwin.md"
init_state = [[0, 0], 'r', [3, 3]]
goal_state = [[3, 3], 'l', [0, 0]]


def run_mm_cc(algorithm, print_stats=True, verbose_print=True, check_visited_nodes=False, save_to_file=True):
    """Run the Missionaries and Cannibals solver

    Args:
        algorithm (str): the algorithm used for solving the problem.
        print_stats (bool, optional): whether or not the running statistics will be printed. Defaults to True.
        verbose_print (bool, optional): whether the action and path shall be printed. Defaults to True.
        check_visited_nodes (bool, optional): whether or not already visited nodes is checked before adding a node to the frontier. Defaults to False.
        save_to_file (bool, optional): whether the results shall be saved to file. Defaults to True.
    """
    message = f"\nRunning {algorithm.upper()} with the following configuration:" \
              f" {' check for explored nodes.' if check_visited_nodes else ' not checking explored nodes.'}  "
    print(message)

    mc = MissionariesAndCannibals(init_state, goal_state)

    sa = SearchAlgorithm(mc, check_visited_nodes=check_visited_nodes)
    # ============= BFS ==================
    # if algorithm.lower() == "bfs":
    print("BFS")
    print('Start state: ')
    mc.pretty_print()
    goal_node = sa.bfs(statistics=print_stats)
    goal_node.pretty_print_solution(verbose=verbose_print)

    print('goal state: ')

    goal_node.state.pretty_print()

    if print_stats:
        sa.statistics()
    # elif algorithm.lower() == "dfs":
    print("DFS")
    print('Start state: ')
    mc.pretty_print()
    goal_node = sa.dfs(statistics=print_stats)
    goal_node.pretty_print_solution(verbose=verbose_print)

    print('goal state: ')

    goal_node.state.pretty_print()

    if print_stats:
        sa.statistics()
    # elif algorithm.lower() == "ids":  # ids
    print("IDS")
    print('Start state: ')
    mc.pretty_print()
    goal_node = sa.ids(statistics=print_stats)
    # goal_node.pretty_print_solution(verbose=verbose_print)

    print('goal state: ')

    # goal_node.state.pretty_print()

    if print_stats:
        sa.statistics()

    # elif algorithm.lower() == "a_star":  # ids
    print("A_STAR")
    print('Start state: ')
    mc.pretty_print()
    # goalNode = sa.a_star(statistics=print_stats)
    goal_node = sa.a_star(statistics=print_stats)
    goal_node.pretty_print_solution(verbose=verbose_print)
    # goalNode.pretty_print_solution(verbose=verbose_print)
    print('goal state: ')

    goal_node.state.pretty_print()
    if print_stats:
        sa.statistics()

    print("GFS")
    print('Start state: ')
    mc.pretty_print()
    # goal_node = sa.gfs(statistics=print_stats)

    # goalNode = sa.gfs(statistics=print_stats)
    goal_node.pretty_print_solution(verbose=verbose_print)
    # goalNode.pretty_print_solution(verbose=verbose_print)
    print('goal state: ', goal_node.solution())
    #print("Path Cost: ", goal_node.path_cost)
    # goal_node.state.pretty_print()

    if print_stats:
        sa.statistics()

    if save_to_file:
        WriteToFile(filename=filename, msg=message)
        WriteToFile(filename=filename, msg=str(sa.get_running_stats()))


# -------------------------------------------------------------------
def main():
    """
    Entry point of the program
    Returns None
    -------

    """
    run_mm_cc(algorithm="bfs", print_stats=True, verbose_print=True, check_visited_nodes=True)
    run_mm_cc(algorithm="dfs", print_stats=True, verbose_print=True, check_visited_nodes=True)
    run_mm_cc(algorithm="ids", print_stats=True, verbose_print=True, check_visited_nodes=True)
    run_mm_cc(algorithm="gfs", print_stats=True, verbose_print=True, check_visited_nodes=True)
    run_mm_cc(algorithm="a_star", print_stats=True, verbose_print=True, check_visited_nodes=True)

    # Not checking for explored nodes
    run_mm_cc(algorithm="bfs", print_stats=True, verbose_print=True, check_visited_nodes=False)
    run_mm_cc(algorithm="dfs", print_stats=True, verbose_print=True, check_visited_nodes=False)
    run_mm_cc(algorithm="ids", print_stats=True, verbose_print=True, check_visited_nodes=False)
    run_mm_cc(algorithm="gfs", print_stats=True, verbose_print=True, check_visited_nodes=False)
    run_mm_cc(algorithm="a_star", print_stats=True, verbose_print=True, check_visited_nodes=False)
    # ids

    # a_star
    # run_mm_cc(algorithm="a_star", print_stats=True, verbose_print=True, check_visited_nodes=True)
    # run_mm_cc(algorithm="a_star", print_stats=True, verbose_print=True, check_visited_nodes=False)

    # gfs


if __name__ == "__main__":
    main()
