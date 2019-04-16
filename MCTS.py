import random
import time
import concurrent.futures


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
        with concurrent.futures.ProcessPoolExecutor() as executor:
            depth = 0
            tmp_state = node.state
            while not tmp_state.is_over():
                actions = tmp_state.get_legal_plays()
                action = random.choice(actions)
                tmp_state = tmp_state.state_move(action)
                depth += 1
                if depth > 400:
                    print(">400: return 0")
                    return 0
            result = tmp_state.get_result()
            print("depth :", depth, " | result: ", result)
            return result

    @staticmethod
    def best_action(times, root):

        time_start = time_3 = time.time()

        for _ in range(times):
            node = MCTS.tree_policy(root)
            time_1 = time.time()
            # print("tree_policy time: ", time_1 - time_3)

            reward = MCTS.rollout(node)
            time_2 = time.time()
            print("roll-out time: ", time_2 - time_1)

            node.backup(reward)
            # time_3 = time.time()
            # print("backup time: ", time_3 - time_2)

        time_end = time.time()

        print("--- time spent: ", time_end - time_start, " ---")
        for child in root.children:
            print(child.value, "/", child.visits)
        print("---\n")

        return root.best_child()








