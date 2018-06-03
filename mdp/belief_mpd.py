from mdp.pomdp import *


class BeliefMDP:

    def __init__(self, pomdp: POMDP, belief_probabilities = None):
        self.pomdp = pomdp

        self.belief_probabilities = {}
        if belief_probabilities is not None:
            self.belief_probabilities = belief_probabilities
        else:
            for state in self.pomdp.mdp.states:
                self.belief_probabilities[state] = 1/len(self.pomdp.mdp.states)

    def do_action(self, action):
        observation = self.pomdp.do_action(action)
        self.apply_observation(observation, action)
        return observation

    def apply_observation(self, observation, action):
        self.belief_probabilities = self.apply_observation_to_beliefs(observation, action, self.belief_probabilities)

    def apply_observation_to_beliefs(self, observation, action, beliefs):
        new_beliefs = {}
        for end_state in self.pomdp.mdp.states:
            observation_prob = self.pomdp.get_observation_probability(end_state, action, observation)
            joint_end_start_prob = 0.0
            for state in self.pomdp.mdp.states:
                transitional_prob = self.pomdp.mdp.get_transitional_probability(state, action, end_state)
                joint_end_start_prob += transitional_prob * beliefs[state]

            new_beliefs[end_state] = observation_prob * joint_end_start_prob

        normalization_factor = sum(new_beliefs.values())
        for key, item in new_beliefs.items():
            new_beliefs[key] = item / normalization_factor

        return new_beliefs

    def get_belief_probabilities(self):
        return self.belief_probabilities
