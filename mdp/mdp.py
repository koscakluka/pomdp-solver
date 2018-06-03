import random


class State:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "State: " + self.name


class Action:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Action: " + self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other


class MDP:

    def __init__(self, states, actions, transitions, rewards, start_state=None):
        """
            states - list of State objects
            actions - list of Action objects
            transitions - dictionary of lists with syntax {(State, Action, State): double in interval [0,1]}
            rewards - dictionary with syntax {(State, Action): double}
            start_state - state from which the MDP starts
        """
        # Definition variables
        self.states = states
        self.actions = actions
        self.transitions = transitions
        self.rewards = rewards

        # Game variables
        self.current_state = start_state
        if start_state is None or start_state not in states:
            self.current_state = random.choice(self.states)
        self.score = 0

    def validate_transitions(self):
        # TODO: Validate that all transition probabilities add up to 1
        pass

    def do_action(self, action):
        """
            Applies action to the MDP and returns the new state
        """
        rand_num = random.uniform(0, 1)
        candidate_states = self.get_candidate_end_states(self.current_state, action)

        roulette_wheel_value = 0
        for state in candidate_states:
            roulette_wheel_value += self.transitions[(self.current_state, action, state)]
            if roulette_wheel_value > rand_num:

                # Apply reward
                if (self.current_state, action) in self.rewards:
                    self.score += self.rewards[(self.current_state, action)]

                # Change state
                self.current_state = state
                return self.current_state

    def get_candidate_end_states(self, state, action):
        candidate_states = []
        for end_state in self.states:
            if (state, action, end_state) in self.transitions:
                candidate_states.append(end_state)
        return candidate_states

    def get_transitional_probability(self, start_state, action, end_state):
        if (start_state, action, end_state) in self.transitions:
            return self.transitions[(start_state, action, end_state)]
        else:
            return 0.0

    def get_action(self, action_name):
        for action in self.actions:
            if action == action_name:
                return action

    def get_score(self):
        return self.score

    def get_current_state(self):
        return self.current_state
