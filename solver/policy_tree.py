from mdp.pomdp import POMDP
import numpy as np

DISCOUNT_RATE = 0.9


class PolicyTree:

    def __init__(self, pomdp: POMDP, action, subtrees=None):
        self.pomdp = pomdp
        self.action = action
        if subtrees is not None:
            self.subtrees = dict(subtrees)
        else:
            self.subtrees = None

    def get_stval(self, start_state, observation):
        if self.subtrees is None or observation not in self.subtrees:
            return 0
        stval = 0
        for end_state in self.pomdp.mdp.get_candidate_end_states(start_state, self.action):
            stval += self.pomdp.mdp.get_transitional_probability(start_state, self.action, end_state) * \
                     self.pomdp.get_observation_probability(end_state, self.action, observation) * \
                     self.subtrees[observation].get_value(end_state)

        return stval

    def get_value(self, start_state):
        value = self.pomdp.mdp.rewards[(start_state, self.action)]
        for observation in self.pomdp.observations:
            value += DISCOUNT_RATE*self.get_stval(start_state, observation)

        return value

    def get_values(self):
        values = []
        for state in self.pomdp.mdp.states:
            values.append(self.get_value(state))
        return np.array(values)

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.subtrees is None:
            return str(self.action)
        rep = str(self.action) + " ->  ["
        for subtree in self.subtrees:
            rep += str(subtree) + ":" + str(self.subtrees[subtree])+ ", "
        rep += "]"
        return rep
