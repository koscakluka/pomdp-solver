from matplotlib import pyplot as plot
from solver.policy_tree import *
from problems.tiger_problem import *
from scipy.optimize import linprog
import numpy as np
import itertools

EPSILON = 1e-4
ITERATIONS = 4


def unique(policy_trees):
    unique_policy_trees = []
    policy_trees = list(policy_trees)
    while len(policy_trees) > 0:
        policy_tree = policy_trees[0]
        unique_policy_trees.append(policy_tree)
        policy_trees.pop(0)
        for policy_tree_tilda in policy_trees:
            if all(policy_tree.get_values() == policy_tree_tilda.get_values()):
                policy_trees.remove(policy_tree_tilda)

    return unique_policy_trees


def dominate(problem, policy_tree, policy_trees):
    if len(policy_trees) == 0:
        return tuple(itertools.product([0.5], repeat=len(problem.states)))

    # minimization function coefficients
    c = [-int(i == len(problem.states)) for i in range(len(problem.states)+1)]

    A_ub = []
    b_ub = []
    for policy_tree_tilda in policy_trees:
        if policy_tree == policy_tree_tilda:
            continue

        A_ub.append(
            [(policy_tree_tilda.get_value(state) - policy_tree.get_value(state)) for state in problem.states]
        )
        A_ub[len(A_ub)-1].append(1)
        b_ub.append(0)

    A_eq = [[int(i != len(problem.states)) for i in range(len(problem.states) + 1)]]
    b_eq = 1

    bound = tuple([(0, 1) if i != problem.states else (None, None) for i in range(len(problem.states)+1)])

    res = linprog(c, A_ub, b_ub, A_eq, b_eq, bound)
    if res.success and res.x[len(problem.states)] > EPSILON: # (max(max(A_ub)) - min(min(A_ub)))*0.001:
        return [res.x[i] for i in range(len(problem.states))]

    return False


def policy_filter(problem, policy_trees):
    policy_trees = unique(policy_trees)
    dominant_trees = []
    for policy_tree in policy_trees:
        if dominate(problem, policy_tree, policy_trees):
            dominant_trees.append(policy_tree)
    return dominant_trees


def best_tree(x, policy_trees):
    x = np.array(x)
    maxtree = (None, -10**9)
    for policy_tree in policy_trees:
        val = np.dot(x, np.array(policy_tree.get_values()))
        if val > maxtree[1]:
            maxtree = (policy_tree, val)

    return maxtree[0]


def policy_filter_lark(problem, policy_trees):
    dominant_trees = []
    policy_trees = unique(policy_trees)
    while len(policy_trees) > 0:
        policy_tree = policy_trees[0]
        x = dominate(problem, policy_tree, dominant_trees)
        if not x:
            policy_trees.remove(policy_tree)
        else:
            policy_tree = best_tree(x, policy_trees)
            dominant_trees.append(policy_tree)
            policy_trees.remove(policy_tree)
    return dominant_trees


def plot_policy_trees(problem, policy_trees):
    x = np.array([0, 1])

    plot.figure()
    for policy_tree in policy_trees:
        y = x * policy_tree.get_value(problem.states[0]) + (1 - x) * policy_tree.get_value(problem.states[1])
        plot.plot(x, y, label=str(policy_tree))

    plot.legend()


def plot_value_function(problem, policy_trees):
    x_range = 0.001*np.array(list(range(0, 1001)))

    policy_tree = None

    plot.figure()
    for x in x_range:
        best_policy_tree = best_tree([x, 1-x], policy_trees)
        if policy_tree != best_policy_tree:
            if policy_tree is not None:
                plot.plot(
                    [x_start, x],
                    [np.dot([x_start, 1-x_start], policy_tree.get_values()),
                     np.dot([x, 1-x], policy_tree.get_values())],
                    label=str(policy_tree)
                )
            policy_tree = best_policy_tree
            x_start = x

    plot.plot(
        [x_start, x],
        [np.dot([x_start, 1 - x_start], policy_tree.get_values()),
         np.dot([x, 1 - x], policy_tree.get_values())],
        label=str(policy_tree)
    )
    plot.legend()


def main():
    problem = TigerProblem()

    policy_trees_optimal = {}

    policy_trees = []

    for action in problem.actions:
        policy_tree = PolicyTree(problem.pomdp, action)
        policy_trees.append(policy_tree)

    policy_trees_optimal[0] = list(policy_trees)

    for i in range(1, ITERATIONS):
        print("Iteration " + str(i+1) + " starting...")

        policy_trees = []

        for action in problem.actions:
            for subtrees_list in itertools.product(policy_trees_optimal[i-1], repeat=len(problem.observations)):
                subtrees = {}
                for j in range(0, len(problem.observations)):
                    subtrees[problem.observations[j]] = subtrees_list[j]
                policy_tree = PolicyTree(problem.pomdp, action, subtrees)
                policy_trees.append(policy_tree)

        policy_trees_optimal[i] = policy_filter_lark(problem, policy_trees)

    plot_policy_trees(problem, policy_trees_optimal[ITERATIONS-1])
    plot_value_function(problem, policy_trees_optimal[ITERATIONS - 1])
    plot.show()


if __name__ == "__main__":
    main()