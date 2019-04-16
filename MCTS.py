import random
import time
from Efunction import Efunction

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
    def rollout(node):
        tmp_state = node.state
        depth = 0
        while not tmp_state.is_over():
            depth = depth + 1
            if depth > 30:
                efun = Efunction()
                time_1 = time.time()
                evalue=efun.evaluate(tmp_state)
                time_2 = time.time()
                print("evaluation time: ", time_2 - time_1, ", evalue: ", evalue)
                return evalue
            actions = tmp_state.get_legal_plays()
            action = random.choice(actions)
            tmp_state = tmp_state.state_move(action)
        result = tmp_state.get_result()
        print("depth :", depth, " | result: ", result)
        return result

    @staticmethod
    def best_action(times, root):

        time_start = time.time()

        for _ in range(times):
            node = MCTS.tree_policy(root)
            time_1 = time.time()

            reward = MCTS.rollout(node)

            time_2 = time.time()
            print("roll-out time: ", time_2 - time_1)

            node.backup(reward)

        time_end = time.time()

        print("--- time spent: ", time_end - time_start, " ---")
        for child in root.children:
            print(child.value, "/", child.visits)
        print("---\n")

        return root.best_child()








