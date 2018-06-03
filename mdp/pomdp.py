from mdp.mdp import *


class Observation:

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Observation: " + self.name


class POMDP:

    def __init__(self, mdp: MDP, observations, observation_probability):
        """
            mdp - underlying MDP object
            observations_set - list of
        """
        # Definition variables
        self.mdp = mdp
        # self.beliefs = [] # TODO: Set of beliefs (same as state set?)
        self.observations = observations
        self.observation_probability = observation_probability

        # Game variables
        pass

    def do_action(self, action):
        self.mdp.do_action(action)
        return self.__get_observation(self.mdp.get_current_state(), action)

    def get_observation_probability(self, state, action, observation):
        if (state, action, observation) in self.observation_probability:
            return self.observation_probability[(state, action, observation)]
        else:
            return 0.0

    def __get_observation(self, state, action):
        rand_num = random.uniform(0, 1)

        roulette_wheel_value = 0
        for observation in self.observations:
            if (state, action, observation) in self.observation_probability:
                roulette_wheel_value += self.observation_probability[(state, action, observation)]
                if roulette_wheel_value >= rand_num:
                    return observation
