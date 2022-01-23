import numpy as np
from Grid import Grid

def maximize(grid_state: Grid, a, b, d):
    (max_child, max_utility) = (None, -np.inf)

    if d == 0 or grid_state.is_terminal(who="max"):
        return None, grid_state.eval()

    d -= 1

    for child in grid_state.get_children(who="max"):
        grid = Grid(mat=grid_state.get_matrix())
        grid.move(child)
        (_, utility) = minimize(grid, a, b, d)
        if utility > max_utility:
            (max_child, max_utility) = (grid, utility)
        if max_utility >= b:
            break
        if max_utility > a:
            a = max_utility

    return max_child, max_utility


def minimize(grid_state: Grid, a, b, d):
    """

    :param grid_state: current grid node state
    :param a: alpha
    :param b: beta
    :param d: depth of search (is assed along)
    :return: Choice of min player
    """
    (min_child, min_utility) = (None, np.inf)

    if d == 0 or grid_state.is_terminal(who="min"):
        return None, grid_state.eval()
    d -= 1

    for child in grid_state.get_children(who="min"):
        grid = Grid(mat=grid_state.get_matrix())
        grid.place_new_tile(child[0], child[1], child[2])
        (_, utility) = maximize(grid, a, b, d)
        if utility < min_utility:
            (min_child, min_utility) = (grid, utility)
        if min_utility <= a:
            break
        if min_utility < b:
            b = min_utility

    return min_child, min_utility


def get_best_move(grid, depth=5):
    """
    Function to recursively get best move for given state
    :param grid: state of grid
    :param depth: depth of max-min iteration
    :return: integer of action
    """
    (child, _) = maximize(Grid(mat=grid.get_matrix()), -np.inf, np.inf, depth)
    return grid.get_move_to_child(child)

def NextMove(grid: list, step: int) -> int:
    gridc = Grid(grid)
    if gridc.is_game_over():
        print("Unfortunately, I lost the game.")
        return 4
    #elif np.max(gridc.get_matrix()) > 2000:
     #   print("Stop here, more than 2000 achieved, that's enough :D")
      #  return 4

    depth = 3

    move_code = get_best_move(gridc, depth)
    #moves_str = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    #print(f'Move #{step}: {moves_str[move_code]}')
    return move_code
