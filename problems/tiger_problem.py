from mdp.belief_mpd import *


class TigerProblem():
    # TODO define Problem class
    def __init__(self):

        self.states = [State("Tiger left"), State("Tiger right")]
        self.actions = [Action("Left"), Action("Right"), Action("Listen")]
        self.rewards = {
            (self.states[0], self.actions[0]): -100,
            (self.states[0], self.actions[1]): 10,
            (self.states[0], self.actions[2]): -1,
            (self.states[1], self.actions[0]): 10,
            (self.states[1], self.actions[1]): -100,
            (self.states[1], self.actions[2]): -1
        }

        self.transitions = {
            (self.states[0], self.actions[0], self.states[0]): 0.5,
            (self.states[0], self.actions[0], self.states[1]): 0.5,
            (self.states[0], self.actions[1], self.states[0]): 0.5,
            (self.states[0], self.actions[1], self.states[1]): 0.5,
            (self.states[1], self.actions[0], self.states[0]): 0.5,
            (self.states[1], self.actions[0], self.states[1]): 0.5,
            (self.states[1], self.actions[1], self.states[0]): 0.5,
            (self.states[1], self.actions[1], self.states[1]): 0.5,
            (self.states[0], self.actions[2], self.states[0]): 1,
            (self.states[1], self.actions[2], self.states[1]): 1
        }

        self.observations = [Observation("Tiger left"), Observation("Tiger right")]

        self.observations_probability = {
            (self.states[0], self.actions[0], self.observations[0]): 0.5,
            (self.states[0], self.actions[0], self.observations[1]): 0.5,
            (self.states[0], self.actions[1], self.observations[0]): 0.5,
            (self.states[0], self.actions[1], self.observations[1]): 0.5,
            (self.states[1], self.actions[0], self.observations[0]): 0.5,
            (self.states[1], self.actions[0], self.observations[1]): 0.5,
            (self.states[1], self.actions[1], self.observations[0]): 0.5,
            (self.states[1], self.actions[1], self.observations[1]): 0.5,
            (self.states[0], self.actions[2], self.observations[0]): 0.85,
            (self.states[0], self.actions[2], self.observations[1]): 0.15,
            (self.states[1], self.actions[2], self.observations[0]): 0.15,
            (self.states[1], self.actions[2], self.observations[1]): 0.85
        }

        self.beliefs = ["Tiger left", "Tiger right"]

        self.mdp = MDP(self.states, self.actions, self.transitions, self.rewards)
        self.pomdp = POMDP(self.mdp, self.observations, self.observations_probability)
        self.belief_mdp = BeliefMDP(self.pomdp)

    def do_action(self, action):
        return self.belief_mdp.do_action(action)

    def get_score(self):
        return self.pomdp.mdp.get_score()
