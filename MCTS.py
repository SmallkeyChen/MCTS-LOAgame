import random


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
        while not tmp_state.is_over():
            actions = tmp_state.get_legal_plays()
            action = random.choice(actions)
            tmp_state = tmp_state.state_move(action)
        return tmp_state.get_result()

    @staticmethod
    def best_action(times, root):
        for _ in range(times):
            node = MCTS.tree_policy(root)
            reward = MCTS.rollout(node)
            node.backup(reward)
        return root.best_child()








