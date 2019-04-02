import random
import numpy as np


class MCTSNode:
    def __init__(self, state, parent=None):
        self.value = 0.0
        self.visits = 0.0
        self.state = state
        self.parent = parent
        self.children = []
        actions = self.state.get_legal_plays()
        random.shuffle(actions)
        self.untried_actions = actions

    def is_terminal(self):
        return self.state.is_over()

    def is_all_expanded(self):
        return len(self.untried_actions) == 0

    def expand(self):
        action = self.untried_actions.pop()
        # print(action)
        next_state = self.state.state_move(action)
        child = MCTSNode(next_state, self)
        self.children.append(child)
        return child

    def backup(self, result):
        self.visits += 1.0
        if result == 1:
            self.value += 1.0
        if self.parent:
            self.parent.backup(result)

    def best_child(self):
        weights = [(i.value / i.visits + 1.414 * np.sqrt((2*np.log(self.visits))/i.visits)) for i in self.children]
        return self.children[np.argmax(weights)]
