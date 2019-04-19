from LOAState import LOAState
import numpy as np
from GlobalVar import *
import unittest


# TODO 把三个估值计算合起来，不用循环三次

def move_is_capture(board, move):
    return board[move[0][0]][move[0][1]] == -board[move[1][0]][move[1][1]]

class Efunction:
    def __init__(self):
        self.function = {
                          'concentration': self.concentration,
                          'centralisation': self.centralisation,
                          # 'mobility': self.mobility,
                          'connectedness': self.connectedness,
                          # 'quads': self.quads,
                       }

    def evaluate_state(self, state):
        # features = ['concentration','centralisation','mobility','connectedness','quads']
        features = ['concentration', 'centralisation', 'connectedness']
        count = 0
        evalue = 0
        adverse = -1 if state.now_move == 1 else 1
        for feature in features:
            evalue = evalue+self.function[feature](state.board, state.now_move) \
                     - self.function[feature](state.board, adverse)
            # print(evalue)
            count = count+1
        evalue = evalue/count
        evalue = evalue * 4
        if evalue > 1:
                evalue = 1
        if evalue < -1:
                evalue = -1
        return evalue

    @staticmethod
    def quick_val(state, actions):
        action_scores = []
        xlist, ylist = np.where(state.board == state.now_move)
        num = np.sum(state.board == state.now_move)
        cx = np.sum(xlist) / num
        cy = np.sum(ylist) / num
        for action in actions:
            val1 = abs(action[0][0]-cx) + abs(action[0][1]-cy)
            val2 = abs(action[1][0]-cx) + abs(action[1][1]-cy)
            action_scores.append(val1-val2)
        return action_scores

    @staticmethod
    def evaluate_action_0(state, actions):
        """
        评估每一步的分数，分为CONCENTRATION，CENTRALIZATION，CONNECTEDNESS，每项的分数区间[-1/3，1/3]，总分区间[-1，1]
        :param state: the current state
        :param actions: the list of actions to evaluate
        :return: the list of scores corresponding to the actions
        """
        actions_scores = []

        num, sum_x, sum_y, total_dist_before = 0, 0, 0, 0
        n_list = []

        # region get status of current player: pieces-number, center-coord: before & after, distance
        # ------------------------------------------------------------------------------------------

        # 1. find center coord before move
        for i in range(8):
            for j in range(8):
                if state.board[i][j] == state.now_move:
                    n_list.append([i, j])
                    num = num + 1
                    sum_x = sum_x + i
                    sum_y = sum_y + j
        cx_before, cy_before = sum_x / num, sum_y / num

        # 2. calculate average distance before move
        for n in n_list:
            total_dist_before = total_dist_before + max(abs(n[0] - cx_before), abs(n[1] - cy_before))
        average_dist_before = total_dist_before / num

        # endregion

        # region evaluate each move in actions
        # -----------------------------
        for i in range(actions.__len__()):     # [(row, col), (e_row, e_col)]
            move = actions[i]
            start_coord, end_coord, total_dist_after = move[0], move[1], 0
            connect_before, connect_after = 0, 0
            actions_scores.append(0)

            # 1. find center coord after each move
            cx_after = cx_before + (end_coord[0] - start_coord[0]) / num
            cy_after = cy_before + (end_coord[1] - start_coord[1]) / num

            # 2. calculate average distance after move
            for n in n_list:
                total_dist_after = total_dist_after + max(abs(n[0] - cx_after), abs(n[1] - cy_after))
            # average_dist_after = total_dist_after / num

            # 3. record score for **CONCENTRATION**: -delta(total_distance) * 1/6 * 1/3 (cause max delta = 6?)
            actions_scores[i] = actions_scores[i] + (total_dist_before - total_dist_after) * 1/6 * 1/3
            # print("------\n concentration: %.2f" % actions_scores[i])

            # 4. record score for **CENTRALIZATION**: -delta(distance_to_board_center) * 1/6 * 1/3 (cause max delta = 6)
            dist_before = abs(start_coord[0] - 3.5) + abs(start_coord[1] - 3.5)
            dist_after = abs(end_coord[0] - 3.5) + abs(end_coord[1] - 3.5)
            actions_scores[i] = actions_scores[i] + (dist_before - dist_after) * 1/6 * 1/3
            # print(" centralization: %.2f" % ((dist_before - dist_after) * 1/6 * 1/3))

            # 5. record score for **CONNECTEDNESS**: delta(connected_pieces) * 1/8 * 1/3 (cause max delta = 8)
            one_step_moves = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
            for m in one_step_moves:
                start_neigh = (start_coord[0] + m[0], start_coord[1] + m[1])
                end_neigh = (end_coord[0] + m[0], end_coord[1] + m[1])
                if 0 <= start_neigh[0] <= 7 and 0 <= start_neigh[1] <= 7:
                    connect_before = connect_before + (state.board[start_neigh[0]][start_neigh[1]] == state.now_move)
                if 0 <= end_neigh[0] <= 7 and 0 <= end_neigh[1] <= 7:
                    connect_after = connect_after + (state.board[end_neigh[0]][end_neigh[1]] == state.now_move)
            actions_scores[i] = actions_scores[i] + (connect_after - connect_before) * 1/8 * 1/3
            # print(" connectedness: %.2f" % ((connect_after - connect_before) * 1/8 * 1/3))

            # 6. if move is capturing: calculate bonus score based on opponent's pieces
            if state.board[end_coord] == -state.now_move:

                # 6.1. **CENTRALIZATION**: (area: [-1/6, 1/6])
                actions_scores[i] = actions_scores[i] - (abs(end_coord[0] - 3.5) + abs(end_coord[1] - 3.5) - 4) * 1/3 * 1/6
                # print(" oppo central: %.2f" % -((abs(end_coord[0] - 3.5) + abs(end_coord[1] - 3.5) - 4) * 1/3 * 1/6))

                # 6.2. **CONNECTEDNESS**: delta(opponent_connectedness) * 1/7 * 1/3 (area: [0, 1/3])
                opponent_connect = 0
                for m in one_step_moves:
                    opponent_end_neigh = (end_coord[0] + m[0], end_coord[1] + m[1])
                    if 0 <= opponent_end_neigh[0] <= 7 and 0 <= opponent_end_neigh[1] <= 7:
                        opponent_connect = opponent_connect + (state.board[opponent_end_neigh[0]][opponent_end_neigh[1]] == -state.now_move)
                actions_scores[i] = actions_scores[i] + opponent_connect * 1/7 * 1/3
                # print(" oppo connect: %.2f" % (opponent_connect * 1/7 * 1/3))

            actions_scores[i] = clamp(actions_scores[i], -1, 1)
            # print("action score: %.3f" % actions_scores[i])

        # endregion

        return actions_scores

    @staticmethod
    def evaluate_action(state, actions):
        """
        评估每一步的分数，分为CONCENTRATION，CENTRALIZATION，CONNECTEDNESS
        :param state: the current state
        :param actions: the list of actions to evaluate
        :return: the list of scores corresponding to the actions
        """
        actions_scores = []

        num, sum_x, sum_y, total_dist_before = 0, 0, 0, 0
        n_list = []

        # region get status of current player: pieces-number, center-coord: before & after, distance
        # ------------------------------------------------------------------------------------------

        # 1. find center coord before move
        for i in range(8):
            for j in range(8):
                if state.board[i][j] == state.now_move:
                    n_list.append([i, j])
                    num = num + 1
                    sum_x = sum_x + i
                    sum_y = sum_y + j
        cx_before, cy_before = sum_x / num, sum_y / num

        # 2. calculate average distance before move
        for n in n_list:
            total_dist_before = total_dist_before + n[0] - cx_before + n[1] - cy_before
            # total_dist_before = total_dist_before + pow(n[0] - cx_before, 2) + pow(n[1] - cy_before, 2)
        average_dist_before = total_dist_before / num

        # endregion

        # region evaluate each move in actions
        # -----------------------------
        for i in range(actions.__len__()):     # [(row, col), (e_row, e_col)]
            move = actions[i]
            start_coord, end_coord, total_dist_after = move[0], move[1], 0
            connect_before, connect_after = 0, 0
            actions_scores.append(0)

            # 1. find center coord after each move
            cx_after = cx_before + (end_coord[0] - start_coord[0]) / num
            cy_after = cy_before + (end_coord[1] - start_coord[1]) / num

            # 2. calculate average distance after move
            for n in n_list:
                total_dist_after = total_dist_after + n[0] - cx_after + n[1] - cy_after
                # total_dist_after = total_dist_after + pow(n[0] - cx_after, 2) + pow(n[1] - cy_after, 2)
            # average_dist_after = total_dist_after / num

            # 3. **CONCENTRATION**: -delta(total_distance) * 1/6 * 1/6 (cause max delta = 6?)
            actions_scores[i] = actions_scores[i] + (total_dist_before - total_dist_after) * 1/6 * 1/3
            # print("------\n concentration: %.2f" % actions_scores[i])

            # 4. **CENTRALIZATION**: delta(distance_to_board_center) * 1/6 * 1/2 (cause max delta = 6)
            dist_before = abs(start_coord[0] - 3.5) + abs(start_coord[1] - 3.5)
            dist_after = abs(end_coord[0] - 3.5) + abs(end_coord[1] - 3.5)
            actions_scores[i] = actions_scores[i] + (dist_before - dist_after) * 1/6 * 1/3
            # print(" centralization: %.2f" % ((dist_before - dist_after) * 1/6 * 1/3))

            # 5. **CONNECTEDNESS**: delta(connected_pieces) * 1/8 * 1/3 (cause max delta = 8)
            one_step_moves = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
            for m in one_step_moves:
                start_neigh = (start_coord[0] + m[0], start_coord[1] + m[1])
                end_neigh = (end_coord[0] + m[0], end_coord[1] + m[1])
                if 0 <= start_neigh[0] <= 7 and 0 <= start_neigh[1] <= 7:
                    connect_before = connect_before + (state.board[start_neigh[0]][start_neigh[1]] == state.now_move)
                if 0 <= end_neigh[0] <= 7 and 0 <= end_neigh[1] <= 7:
                    connect_after = connect_after + (state.board[end_neigh[0]][end_neigh[1]] == state.now_move)
            actions_scores[i] = actions_scores[i] + (connect_after - connect_before) * 1/8 * 1/3
            # print(" connectedness: %.2f" % ((connect_after - connect_before) * 1/8 * 1/3))

            # 6. if move is capturing: calculate bonus score based on opponent's pieces
            if state.board[end_coord] == -state.now_move:

                # 6.1. **CENTRALIZATION**: (area: [-1/6, 1/6])
                actions_scores[i] = actions_scores[i] - (abs(end_coord[0] - 3.5) + abs(end_coord[1] - 3.5) - 4) * 1/3 * 1/6
                # print(" oppo central: %.2f" % -((abs(end_coord[0] - 3.5) + abs(end_coord[1] - 3.5) - 4) * 1/3 * 1/6))

                # 6.2. **CONNECTEDNESS**: delta(opponent_connectedness) * 1/7 * 1/3 (area: [0, 1/3])
                opponent_connect = 0
                for m in one_step_moves:
                    opponent_end_neigh = (end_coord[0] + m[0], end_coord[1] + m[1])
                    if 0 <= opponent_end_neigh[0] <= 7 and 0 <= opponent_end_neigh[1] <= 7:
                        opponent_connect = opponent_connect + (state.board[opponent_end_neigh[0]][opponent_end_neigh[1]] == -state.now_move)
                actions_scores[i] = actions_scores[i] + opponent_connect * 1/7 * 1/3
                # print(" oppo connect: %.2f" % (opponent_connect * 1/7 * 1/3))

            actions_scores[i] = clamp(actions_scores[i], -1, 1)
            # print("action score: %.3f" % actions_scores[i])

        # endregion

        return actions_scores

    @staticmethod
    def concentration(board, color):
        num, count_x, count_y = 0, 0, 0
        nlist = []
        for i in range(8):
            for j in range(8):
                if board[i][j] == color:
                    nlist.append([i, j])
                    num = num+1
                    count_x = count_x+i
                    count_y = count_y+j
        cx = count_x/num;cy = count_y/num
        dx2 = 0; dy2 = 0
        for n in nlist:
            dx2 = dx2+pow(n[0]-cx, 2)
            dy2 = dy2+pow(n[1]-cy, 2)
        lmin = num*0.5 if num <= 4 else 4*0.5+(num-4)*2.5

        # score = 1 / (dis_total - dis_min)
        score = lmin / (dx2+dy2) if dx2+dy2 != 0 else 1
        # print("concen:", score)

        return score

    # TODO improve this
    @staticmethod
    def centralisation(board, color):
        """
        计算棋子中心化程度。只要有棋子在边缘上，分数都是一样的诶……
        :param board:
        :param color:
        :return:
        """
        num = 0
        score = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == color:
                    num = num+1
                    tmp = 1
                    a = 2; b = 5
                    while not(a < i < b and a < j < b):
                        a = a - 1; b = b + 1
                        tmp = tmp / 2
                    score = score + tmp
        score = score / num
        # print("central:", score)
        return score

    @staticmethod
    def mobility(board, color):
        state = LOAState(board, color)
        score = 0
        num = (np.sum(board == color)).astype(int)
        plays = state.get_legal_plays()
        for play in plays:
            tmp = 0.125
            a = 2 ; b = 5
            while not(a < play[0][0] < b and a < play[0][1] < b):
                tmp = tmp * 2
                a = a - 1 ; b = b + 1
            a = 2 ; b = 5
            while not(a < play[1][0] < b and a < play[1][1] < b):
                tmp = tmp / 2
                a = a - 1 ; b = b + 1
            score = score + tmp
        score = score / num
        score = score / 4
        return score

    @staticmethod
    def connectedness(board, color):
        num = 0
        score = 0
        moves = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for i in range(8):
            for j in range(8):
                if board[i][j] == color:
                    num = num+1
                    for move in moves:
                        x = i + move[0]
                        y = j + move[1]
                        if -1 < x < 8 and -1 < y < 8 and board[x][y] == color:
                            score += 1
        score = score / (num * 4)
        # print("connect:", score)
        return score
        # def quads(self,board,color):



if __name__ == "__main__":
    initial_board = np.zeros((8, 8))
    # initial_board[[0, 7], 1:7] = 1
    initial_board[[3, 4], 3:5] = 1
    initial_board[1:7, [0, 7]] = -1
    print(initial_board)
    state = LOAState(initial_board, 1)
    Efun = Efunction()
    value = Efun.evaluate_state(state)
    print(value)

