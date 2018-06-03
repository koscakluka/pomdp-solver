from problems.tiger_problem import *
import sys


def main(problem_choice="tiger", gui="-nogui"):
    if problem_choice == "tiger":
        problem = TigerProblem()
    else:
        raise Exception("Unknown problem " + problem_choice)

    if gui == "-gui":
        pass
    else:
        interactive_shell(problem)


def interactive_shell(problem):
    print("Available actions:")
    print(problem.mdp.actions)
    while True:
        action = input("Choose action: ")
        if action == "_Quit":
            break
        elif action not in problem.mdp.actions:
            print("Unknown action!")
            continue
        action = problem.mdp.get_action(action)

        problem.do_action(action)
        print("Beliefs about states: " + str(problem.belief_mdp.get_belief_probabilities()))
        print("Current score: " + str(problem.get_score()))


def argument_parser(argv):
    pass


if __name__ == "__main__":
    print(sys.argv)
    problem, gui = sys.argv[1:]
    main(problem, gui)
