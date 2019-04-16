import numpy as np


class LOAState:
    """ The state of the LOA game.
        Initial state:
        -XXXXXX-
        O------O
        O------O
        O------O
        O------O
        O------O
        O------O
        -XXXXXX-
        X is 1, O is -1, nothing is 0
    """

    def __init__(self, board, now_move):
        self.board = board
        self.board_size = 8
        self.now_move = now_move

    def is_move_legal(self, move):
        """
        judge human move is legal. now move is -1 (for human)
        :param move: [(row1,col1), (row2,col2)], UI should promise we have a move, not at same place.
        :return: True or False
        """
        start_row = move[0][0]
        start_col = move[0][1]
        end_row = move[1][0]
        end_col = move[1][1]
        delta_col = end_col - start_col
        delta_row = end_row - start_row
        adverse = -1 if self.now_move == 1 else 1

        if delta_col == 0:
            step = abs(delta_row)
            min_row, max_row = (start_row, end_row) if start_row < end_row else (end_row, start_row)
            between = self.board[min_row + 1: max_row, start_col]
            if np.any(between == adverse):
                return False
            nums = np.sum((self.board[:, start_col] != 0).astype(int))

        elif delta_row == 0:
            step = abs(delta_col)
            min_col, max_col = (start_col, end_col) if start_col < end_col else (end_col, start_col)
            between = self.board[start_row, min_col + 1: max_col]
            if np.any(between == adverse):
                return False
            nums = np.sum((self.board[start_row] != 0).astype(int))

        elif delta_col * delta_row < 0:
            if abs(delta_col) != abs(delta_row):
                return False

            step = abs(delta_col)
            tmp_row, tmp_col = (start_row - 1, start_col + 1) if start_row > end_row else (end_row - 1, end_col + 1)
            for i in range(step - 1):
                if self.board[tmp_row, tmp_col] == adverse:
                    return False
                tmp_row, tmp_col = tmp_row - 1, tmp_col + 1

            nums = 0
            if start_row + start_col >= 7:
                head = (7, start_row + start_col - 7)
                n_ = 14 - start_row - start_col + 1
            else:
                head = (start_row + start_col, 0)
                n_ = start_row + start_col + 1

            for i in range(n_):
                if self.board[head[0], head[1]]:
                    nums = nums + 1
                head = (head[0] - 1, head[1] + 1)

        else:
            if abs(delta_col) != abs(delta_row):
                return False

            step = abs(delta_col)
            tmp_row, tmp_col = (start_row + 1, start_col + 1) if start_row < end_row else (end_row + 1, end_col + 1)
            for i in range(step - 1):
                if self.board[tmp_row, tmp_col] == adverse:
                    return False
                tmp_row, tmp_col = tmp_row + 1, tmp_col + 1

            nums = 0
            if start_row >= start_col:
                head = (start_row - start_col, 0)
                n_ = 7 - start_row + start_col + 1
            else:
                head = (0, start_col - start_row)
                n_ = 7 - start_col + start_row + 1

            for i in range(n_):
                if self.board[head[0], head[1]]:
                    nums = nums + 1
                head = (head[0] + 1, head[1] + 1)

        return step == nums

    def get_legal_plays(self):
        """
        :return: get a list of all legal moves for the MTCSNode to expand
        """
        row_list, col_list = np.where(self.board == self.now_move)
        space_row_list, space_col_list = np.where(self.board != self.now_move)
        legal_plays = []
        for row, col in zip(row_list, col_list):
            for e_row, e_col in zip(space_row_list, space_col_list):
                move = [(row, col), (e_row, e_col)]
                if self.is_move_legal(move):
                    legal_plays.append(move)

        return legal_plays

    def get_result(self):
        """
        if now_move is 1, that is X is ready to move, wo should judge O is win or not.
        :return: is X can win, return 1, O can win, return -1, if tie, return 0
        """
        if self.now_move == 1:
            win = self.is_win(self.board, -1)
            # white location
            if np.sum((self.board == 1).astype(int)) == 1 or win:
                # nums of black = 1, white also win
                return -1
            else:
                return None
        else:
            win = self.is_win(self.board, 1)
            if np.sum((self.board == -1).astype(int)) == 1 or win:
                return 1
            else:
                return None

    def is_over(self):
        """
        :return: is game already terminal
        """
        return self.get_result() is not None

    def state_move(self, move):
        """
        :param move: [(row1,col1), (row2,col2)]
        :return: a new LOAState
        """
        new_board = self.board.copy()
        new_board[move[0][0], move[0][1]] = 0
        new_board[move[1][0], move[1][1]] = self.now_move
        now_move = -1 if self.now_move == 1 else 1
        return LOAState(new_board, now_move)

    @staticmethod
    def get_start(board, color):
        """
        :return: find the broad search start point
        """
        for i in range(8):
            for j in range(8):
                if board[i][j] == color:
                    return i, j

    @staticmethod
    def is_win(board, color):
        """
        :param board: the board need to judge
        :param color: judge the color chess is massed
        :return: color win or not
        """
        tmp = LOAState.get_start(board, color)
        board = (board == color).astype(int)
        np.sum(board == color).astype(int)
        color_nums = np.sum(board)
        moves = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        openlist = [tmp]
        visited = [tmp]

        while openlist:
            tmp = openlist.pop(0)
            for move in moves:
                x = tmp[0] + move[0]
                y = tmp[1] + move[1]
                if -1 < x < 8 and -1 < y < 8 and board[x][y] and board[x][y]:
                    if (x, y) not in visited:
                        openlist.append((x, y))
                        visited.append((x, y))
        return len(visited) == color_nums
