from copy import deepcopy
import numpy as np


class Grid:
    """
    Class to simulate grid movements and obtain information about grid
    Legend:
    i: row index
    j: column index
    matrix: representation of grid in list of list

    """
    def __init__(self, mat):
        # Work with numpy array instead of list of list
        self.matrix = np.array(deepcopy(mat))  # Using deepcopy to make sure not altering the original matrix

    def __eq__(self, other):
        """ Built in function to compare, if state matrices of Grid are equal or not elementwise"""
        return (self.matrix == other.matrix).all()

    def get_matrix(self):
        return deepcopy(self.matrix)

    def place_new_tile(self, i, j, number):
        # Number for new tile can only be 2 or 4
        self.matrix[i][j] = number

    def eval(self):
        """
        Function for evaluating state
        Using: sum of scores* number of zeros
        """
        #return np.sum(self.matrix)/np.count_nonzero(self.matrix)
        #return np.max(self.matrix) - np.count_nonzero(self.matrix)
        # weight light matrix
        # c = 3
        # weight = np.array([
        #     [c**15, c**14, c**13, c**12],
        #     [c**8, c**9, c**10, c**11],
        #     [c**7, c**6, c**5, c**4],
        #     [c**0, c**1, c**2, c**3],
        # ])
        # return np.sum(weight*self.matrix)/np.count_nonzero(self.matrix)

        # weight_pwr = np.array([
        #         [2.5, 2.3, 2.1, 1.9],
        #         [2.3, 2.1, 1.9, 1.8],
        #         [2.1, 1.9, 1.8, 1.7],
        #         [1.9, 1.8, 1.7, 1.6]
        #     ])

        utility = 0
        smooth = 0
        no_empty = np.count_nonzero(self.matrix == 0)

        score_p = np.sum(np.power(self.matrix, 2))
        grid_s = np.sqrt(self.matrix)
        smooth -= np.sum(np.abs(grid_s[::, 0] - grid_s[::, 1]))
        smooth -= np.sum(np.abs(grid_s[::, 1] - grid_s[::, 2]))
        smooth -= np.sum(np.abs(grid_s[::, 2] - grid_s[::, 3]))
        smooth -= np.sum(np.abs(grid_s[0, ::] - grid_s[1, ::]))
        smooth -= np.sum(np.abs(grid_s[1, ::] - grid_s[2, ::]))
        smooth -= np.sum(np.abs(grid_s[2, ::] - grid_s[3, ::]))

        empty_fac = 100000
        smooth_exp = 3.0

        empty_u = no_empty * empty_fac
        smooth_u = smooth ** smooth_exp

        utility += score_p
        utility += empty_u
        utility += smooth_u

        return utility


    def get_zero_non_zero_indices(self):
        """
        :return: indices for zero and non zero rows and columns
        """
        # Indices of zero and non zero values
        non_zero_idx = np.where(self.matrix != 0)
        zero_idx = np.where(self.matrix == 0)
        non_zero_row_idx = non_zero_idx[0]
        non_zero_col_idx = non_zero_idx[1]
        zero_row_idx = zero_idx[0]
        zero_col_idx = zero_idx[1]
        return non_zero_row_idx, non_zero_col_idx, zero_row_idx, zero_col_idx

    def can_move_up(self):
        # Get indices first
        non_zero_row_idx, non_zero_col_idx, zero_row_idx, zero_col_idx = self.get_zero_non_zero_indices()
        # Checking, if there is a zero UPWARDS or if there are two numbers with zeros inbetween adjacent to merge (
        # columnwise)
        for j in range(4):
            tmp_non_zero_row_idx = non_zero_row_idx[non_zero_col_idx == j]
            tmp_zero_row_idx = zero_row_idx[zero_col_idx == j]
            # Zero check, if above non zero value
            if len(tmp_non_zero_row_idx) > 0 and len(tmp_zero_row_idx) > 0:
                if np.max(tmp_non_zero_row_idx) > np.max(tmp_zero_row_idx):
                    return True
            # Merge check
            values = self.matrix[tmp_non_zero_row_idx, j]
            if (values[1:] == values[:-1]).any():
                return True
        return False

    def can_move_down(self):
        # Get indices first
        non_zero_row_idx, non_zero_col_idx, zero_row_idx, zero_col_idx = self.get_zero_non_zero_indices()

        # Checking, if there is a zero BELOW or if there are two numbers with zeros inbetween adjacent to merge (
        # columnwise)
        for j in range(4):
            tmp_non_zero_row_idx = non_zero_row_idx[non_zero_col_idx == j]
            tmp_zero_row_idx = zero_row_idx[zero_col_idx == j]
            # Zero check, if below non zero value
            if len(tmp_non_zero_row_idx) > 0 and len(tmp_zero_row_idx) > 0:
                if np.max(tmp_non_zero_row_idx) < np.max(tmp_zero_row_idx):
                    return True
            # Merge check
            values = self.matrix[tmp_non_zero_row_idx, j]
            if (values[1:] == values[:-1]).any():
                return True
        return False

    def can_move_right(self):
        # Get indices first
        non_zero_row_idx, non_zero_col_idx, zero_row_idx, zero_col_idx = self.get_zero_non_zero_indices()

        # Checking, if there is a zero RIGHT or if there are two numbers with zeros inbetween adjacent to merge (
        # rowwise)
        for i in range(4):
            tmp_non_zero_col_idx = non_zero_col_idx[non_zero_row_idx == i]
            tmp_zero_col_idx = zero_col_idx[zero_row_idx == i]
            # Zero check, if (column index) above non zero value
            if len(tmp_non_zero_col_idx) > 0 and len(tmp_zero_col_idx) > 0:
                if np.max(tmp_non_zero_col_idx) < np.max(tmp_zero_col_idx):
                    return True
            # Merge check
            values = self.matrix[i, tmp_non_zero_col_idx]
            if (values[1:] == values[:-1]).any():
                return True
        return False

    def can_move_left(self):
        # Get indices first
        non_zero_row_idx, non_zero_col_idx, zero_row_idx, zero_col_idx = self.get_zero_non_zero_indices()

        # Checking, if there is a zero RIGHT or if there are two numbers with zeros inbetween adjacent to merge (
        # rowwise)
        for i in range(4):
            tmp_non_zero_col_idx = non_zero_col_idx[non_zero_row_idx == i]
            tmp_zero_col_idx = zero_col_idx[zero_row_idx == i]
            # Zero check, if (column index) above non zero value
            if len(tmp_non_zero_col_idx) > 0 and len(tmp_zero_col_idx) > 0:
                if np.max(tmp_non_zero_col_idx) > np.max(tmp_zero_col_idx):
                    return True
            # Merge check
            values = self.matrix[i, tmp_non_zero_col_idx]
            if (values[1:] == values[:-1]).any():
                return True
        return False

    def get_available_moves_max(self):
        """ Returns possible moves for the max player"""
        moves = []
        if self.can_move_up():
            moves.append(0)
        if self.can_move_down():
            moves.append(1)
        if self.can_move_left():
            moves.append(2)
        if self.can_move_right():
            moves.append(3)
        return moves

    def get_available_moves_min(self):
        """ Get coordinates of available tiles and make tuple (i, j, value)"""
        _, _, zero_row_idx, zero_col_idx = self.get_zero_non_zero_indices()
        places = []
        for ii in range(len(zero_row_idx)):
            places.append((zero_row_idx[ii], zero_col_idx[ii], 2))
            places.append((zero_row_idx[ii], zero_col_idx[ii], 4))
        return places

    def get_children(self, who):
        """

        :param who: either max or min
        :return: returns depending on current level of search tree next child actions
        """
        if who == "max":
            return self.get_available_moves_max()
        elif who == "min":
            return self.get_available_moves_min()

    def is_terminal(self, who):
        """
        Function to check whether we reached a terminal state of the game state
        """
        if who == "max":
            return len(self.get_available_moves_max()) == 0
        elif who == "min":
            _, _, zero_row_idx, zero_col_idx = self.get_zero_non_zero_indices()
            return len(zero_row_idx) == 0

    def is_game_over(self):
        return self.is_terminal(who="max")

    def merge_left(self, arr1d):
        """ Function to merge ONE 1d array according to 2048 rules to the left"""
        new_col = np.zeros(4, dtype=arr1d.dtype)
        jj = 0
        previous = None
        # Loop until finding first non zero
        for ii in range(arr1d.size):
            if arr1d[ii] != 0:
                if previous is None:
                    previous = arr1d[ii]
                else:
                    # Merge two values together
                    if previous == arr1d[ii]:
                        new_col[jj] = 2 * arr1d[ii]
                        jj += 1
                        previous = None
                    # Otherwise move towards end
                    else:
                        new_col[jj] = previous
                        jj += 1
                        previous = arr1d[ii]
        # For last value
        if previous is not None:
            new_col[jj] = previous
        return new_col

    def move_calculation(self, direction):
        """
        Direction must be mapped accordingly to # 0: left, 1: up, 2: right, 3: down for numpy function rotation we need
        --> In our game: 0 means UP, 1 means DOWN, 2 means LEFT, 3 means RIGHT
        """
        rotation_list = [1, 3, 0, 2]
        rotation = rotation_list[direction]
        rotated_board = np.rot90(self.matrix, rotation)
        cols = [rotated_board[i, :] for i in range(4)]
        new_board = np.array([self.merge_left(col) for col in cols])
        return np.rot90(new_board, -rotation)

    def up(self):
        self.matrix = self.move_calculation(0)

    def down(self):
        self.matrix = self.move_calculation(1)

    def left(self):
        self.matrix = self.move_calculation(2)

    def right(self):
        self.matrix = self.move_calculation(3)

    def move(self, direction):
        if direction == 0:
            self.up()
        elif direction == 1:
            self.down()
        elif direction == 2:
            self.left()
        else:
            self.right()

    def get_move_to_child(self, child):
        """

        :param child: child of the Grid class
        :return: integer for which move direction is needed to perform to get to th next grid state
        """
        if self.can_move_up():
            g = Grid(mat=self.get_matrix())
            g.up()
            if g == child:
                return 0
        if self.can_move_down():
            g = Grid(mat=self.get_matrix())
            g.down()
            if g == child:
                return 1
        if self.can_move_left():
            g = Grid(mat=self.get_matrix())
            g.left()
            if g == child:
                return 2
        return 3


if "__main__" == __name__:

    # Test
    a = np.array([
        [4, 2, 8, 16],
        [2, 4, 2, 4],
        [2, 0, 0, 0],
        [2, 4, 2, 2]
    ])

    grid = Grid(a)

    print(grid.get_available_moves_max())
    print(grid.get_available_moves_min())

    grid.down()
    print(grid.matrix)
    print(grid.is_game_over())

