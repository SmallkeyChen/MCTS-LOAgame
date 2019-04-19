import random
import time
from Efunction import Efunction
import numpy as np
from GlobalVar import *


# when using evaluation functions in every step
# depth: ~40
# get_legal_play time: ~0.003s
# evaluation time: ~0.0003s(?), legal plays: ~40, total: ~0.01s
# roll out time: 40 * (0.003 + 0.01) = ~0.5s

# TODO 优化get_legal_plays

depths = []
time_get_legal_plays = []
time_evaluation = []
count_legal_plays = []


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
            e_fun = Efunction()

            # when too deep, return evaluation value directly
            if depth > depth_threshold:
                # evaluate current value
                e_value = e_fun.evaluate_state(tmp_state)
                return e_value

            # choose an action to take
            time1 = time.time()
            actions = tmp_state.get_legal_plays()
            # print("actions: ", actions)
            time2 = time.time()
            time_get_legal_plays.append(time2 - time1)
            # print("actions count: ", actions.__len__())
            count_legal_plays.append(actions.__len__())
            # print("get legal play time: ", time2 - time1)

            if roll_out_mode == RollOutMode.Evaluation:
                action_scores = []
                time1 = time.time()

                if depth % depth_step == 0:
                    # action_scores = e_fun.quick_val(tmp_state, actions)
                    action_scores = e_fun.evaluate_action(tmp_state, actions)
                    action = actions[np.argmax(action_scores)]
                else:
                    random.shuffle(actions)
                    # TODO if actions is empty?
                    # action_scores = e_fun.quick_val(tmp_state, actions[0:int(actions.__len__() / chosen)])
                    action_scores = e_fun.evaluate_action(tmp_state, actions[0:max(int(actions.__len__() / chosen), 1)])
                    action = actions[np.argmax(action_scores)]

                time2 = time.time()
                time_evaluation.append(time2 - time1)

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
        time_get_legal_plays.clear()
        count_legal_plays.clear()
        time_evaluation.clear()

        for _ in range(times):
            node = MCTS.tree_policy(root)

            time_1 = time.time()
            reward = MCTS.roll_out(node)
            time_2 = time.time()

            print("--- roll-out time: ", time_2 - time_1, " ---")

            node.backup(reward)

        time_end = time.time()

        print("\ntotal time: {0:.3f}".format(time_end - time_start))
        print("average roll-out time: {0:.3f}".format((time_end - time_start) / total_counts))
        print("average depth: {0:.3f}".format(np.mean(depths)))
        print("average number of legal plays: {0:.1f}".format(np.mean(count_legal_plays)))
        print("average get_legal_play time: {0:.5f} --- {1:.2f}%".format(np.mean(time_get_legal_plays), np.mean(time_get_legal_plays) / (time_end - time_start) * np.mean(depths) * total_counts * 100))
        print("average evaluation time: {0:.5f} --- {1:.2f}%".format(np.mean(time_evaluation), np.mean(time_evaluation) / (time_end - time_start) * np.mean(depths) * total_counts * 100))
        print("----- children scores -----")
        for child in root.children:
            print(child.value, "/", child.visits)
        print("---------------------------\n")

        return root.best_child(0)
