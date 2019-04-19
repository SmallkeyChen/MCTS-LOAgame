import random
import numpy as np
from Efunction import Efunction


class MCTSNode:
    def __init__(self, state, parent=None):
        self.value = 0.0
        self.visits = 0.0
        self.state = state
        self.parent = parent
        self.children = []
        self.e_value = 0
        actions = self.state.get_legal_plays()
        random.shuffle(actions)
        self.untried_actions = actions
        self.pruning()

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
        self.value += result
        if self.parent:
            self.parent.backup(result)

    def best_child(self, c=1.414):
        weights = []
        for i in self.children:
            if self.state.now_move == -1:
                i.value = -i.value
            w = (i.value / i.visits + c * np.sqrt((2 * np.log(self.visits)) / i.visits))
            weights.append(w)

        return self.children[np.argmax(weights)]

    def pruning(self):
        e_fun = Efunction()
        e_values = []

        for action in self.untried_actions:
            tmp_state = self.state
            tmp_state = tmp_state.state_move(action)
            e_value = e_fun.evaluate_state(tmp_state)
            e_value = -e_value
            e_values.append(e_value)
        untried = self.untried_actions
        actions = []
        while untried:
            action = untried.pop()
            actions.append(action)
            e_values.pop()
            if untried:
                remove = np.argmin(e_values)
                del untried[remove]
                del e_values[remove]
        self.untried_actions = actions
