from LOAState import LOAState
import numpy as np


class Efunction:
    def __init__(self):
        self.function = {
                          'concentration': self.concentration,
                          'centralisation': self.centralisation,
                          # 'mobility': self.mobility,
                          'connectedness': self.connectedness,
                          # 'quads': self.quads,
                       }

    def evaluate(self, state):
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

    def concentration(self, board, color):
        num = 0
        countx = 0; county = 0
        nlist = []
        for i in range(8):
            for j in range(8):
                if board[i][j] == color:
                    nlist.append([i, j])
                    num = num+1
                    countx = countx+i
                    county = county+j
        cx = countx/num;cy = county/num
        dx2 = 0; dy2 = 0
        for n in nlist:
            dx2 = dx2+pow(n[0]-cx, 2)
            dy2 = dy2+pow(n[1]-cy, 2)
        lmin = num*0.5 if num <= 4 else 4*0.5+(num-4)*2.5
        score = lmin / (dx2+dy2) if dx2+dy2 != 0 else 1
        return score

    def centralisation(self, board, color):
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
        return score

    def mobility(self, board, color):
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

    def connectedness(self, board, color):
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
    value = Efun.evaluate(state)
    print(value)

