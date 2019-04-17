import random
import time
from Efunction import Efunction
from enum import Enum
import numpy as np
from GlobalVar import *


# TODO use evaluation functions in every step
#  depth: ~40
#  get_legal_play time: ~0.003s
#  evaluation time: ~0.0003s(?), legal plays: ~40, total: ~0.01s
#  roll out time: 40 * (0.003 + 0.01) = ~0.5s

# TODO 优化get_legal_plays

# TODO 优化evaluate，如果没吃棋，对方的棋子的分数（应该）不会变。
#  另外，不用每次重新计算（质心位置、……），因为不同子节点之间，只有一个棋子有不同

RollOutMode = Enum('RollOutMode', 'Random Evaluation')
roll_out_mode = RollOutMode.Evaluation
depths = []


class MCTS:
    @staticmethod
    def tree_policy(node):
        tmp = node
        while not tmp.is_terminal():
            if tmp.is_all_expanded():
                tmp = tmp.best_child()
            else:
                return tmp.expand()
        return tmp

    @staticmethod
    def roll_out(node):

        tmp_state = node.state
        depth = 0

        while not tmp_state.is_over():
            depth = depth + 1

            # evaluate current value
            e_fun = Efunction()
            e_value = e_fun.evaluate(tmp_state)

            # when too deep, return evaluation value directly
            if depth > depth_threshold:
                return e_value


            # choose an action to take
            time1 = time.time()
            actions = tmp_state.get_legal_plays()
            time2 = time.time()
            # print("get legal play time: ", time2 - time1)

            if roll_out_mode == RollOutMode.Evaluation:
                action_scores = []
                time1 = time.time()

                if depth % depth_step == 0:
                    # evaluate each next-state: the more negative, the better
                    for act in actions:
                        next_state = tmp_state.state_move(act)
                        action_scores.append(e_fun.evaluate(next_state))
                    action = actions[np.argmin(action_scores)]
                    time2 = time.time()
                    # print("[7] legal plays: ", actions.__len__(), "selection time: ", time2 - time1)
                else:
                    random.shuffle(actions)
                    for i in range(max(int(actions.__len__() / chosen), 1)):
                        act = actions[i]
                        next_state = tmp_state.state_move(act)
                        action_scores.append(e_fun.evaluate(next_state))
                    action = actions[np.argmin(action_scores)]
                    time2 = time.time()
                    # print("legal plays: ", actions.__len__(), "selection time: ", time2 - time1)

            elif roll_out_mode == RollOutMode.Random:
                action = random.choice(actions)

            else:
                action = random.choice(actions)

            tmp_state = tmp_state.state_move(action)

        result = tmp_state.get_result()
        print("depth :", depth, " | result: ", result)
        depths.append(depth)
        return result

    @staticmethod
    def best_action(times, root):

        time_start = time.time()

        depths.clear()
        # for i in range(depths.__len__()):
        #     depths[i] = 0

        for _ in range(times):
            node = MCTS.tree_policy(root)

            time_1 = time.time()
            reward = MCTS.roll_out(node)
            time_2 = time.time()

            print("--- roll-out time: ", time_2 - time_1, " ---\n")

            node.backup(reward)

        time_end = time.time()

        print("\ntotal time: ", time_end - time_start)
        print("\naverage time: ", (time_end - time_start) / total_counts)
        print("\naverage depth: ", np.mean(depths))
        print("--- children scores ---\n")
        for child in root.children:
            print(child.value, "/", child.visits)
        print("-----------------------\n")

        return root.best_child()
