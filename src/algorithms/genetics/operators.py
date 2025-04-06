import random
import copy
from typing import Dict
from algorithms.interface import RobotRoute, AlgorithmOutput, Order
from objects.robot import Robot
from algorithms.genetics.other import fill_routes, cut_zeros, add_zeros


def crossover(parent1: AlgorithmOutput, parent2: AlgorithmOutput, order_items: Order, weights: Dict[int, int], warehouse)\
        -> AlgorithmOutput:
    """
    Function that takes half of solutions' routes from parent1 and half from parent2

    :param order_items:
    :param parent1:
    :param parent2:
    :return: new solutions based on two other
    """
    cut_zeros(parent2)
    cut_zeros(parent1)

    robots_indices = list(range(len(parent1.result)))
    first_parent_robots_indices = random.sample(robots_indices, len(robots_indices) // 2)

    robots = list(parent1.result.keys())
    second_parent_robots = []
    for k in parent2.result.keys():
        if robots.index(k) not in first_parent_robots_indices:
            second_parent_robots.append(k)

    new_solution = AlgorithmOutput({})
    items_left = copy.deepcopy(order_items.items)
    for i in first_parent_robots_indices:
        new_solution.result[robots[i]] = copy.deepcopy(parent1.result[robots[i]])
        for node, quantity in parent1.result[robots[i]].items.items():
            if items_left[node] == quantity:
                items_left.pop(node)
            else:
                items_left[node] = items_left[node] - quantity

    for robot in second_parent_robots:
        temp_robot_route = RobotRoute([], {})
        for node, quantity in parent2.result[robot].items.items():
            if node in items_left.keys():
                if items_left[node] > 0:  # could be skipped
                    temp_robot_route.route.append(node)
                    if items_left[node] <= quantity:
                        temp_robot_route.items[node] = items_left[node]
                        items_left.pop(node)
                    elif items_left[node] > quantity:
                        temp_robot_route.items[node] = quantity
                        items_left[node] = items_left[node] - quantity
        new_solution.result[robot] = temp_robot_route
    fill_routes(new_solution, Order(items_left), weights, warehouse)
    add_zeros(new_solution)
    add_zeros(parent1)
    add_zeros(parent2)
    return new_solution


def mutate(solution: AlgorithmOutput, robots_count: int):
    """
    Shuffle node order in robots_count randomly chosen robots

    :param solution:
    :param robots_count:
    """
    cut_zeros(solution)
    robots_indices = list(range(len(solution.result)))
    chosen_robot_indices = random.sample(robots_indices, robots_count)
    robots = list(solution.result.keys())
    for robot_i in chosen_robot_indices:
        random.shuffle(solution.result[robots[robot_i]].route)
    add_zeros(solution)


# teściki - do wywalenia ostatecznie, nie chce mi się pisać unit testów
# trzea poprawić
# r1 = Robot('1')
# t1 = [1, 3, 5]
# i1 = {1: 1, 3: 3, 5: 4}
# rr1 = RobotRoute(t1, i1)
# r2 = Robot('2')
# t2 = [1, 2, 4]
# i2 = {1: 1, 2: 3, 4: 3}
# rr2 = RobotRoute(t2, i2)
# r3 = Robot('3')
# t3 = [2, 3, 4, 5]
# i3 = {2: 3, 3: 3, 4: 4, 5: 4}
# rr3 = RobotRoute(t3, i3)
#
# orderr = Order({1: 2, 2: 6, 3: 6, 4: 7, 5: 8})
#
# parent1 = AlgorithmOutput({r1: rr3, r2: rr1, r3: rr2})
# parent2 = AlgorithmOutput({r1: rr1, r2: rr2, r3: rr3})
# weights = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
# nowe = crossover(parent1, parent2, orderr, weights)
# mutate(parent2, 1)
# print(nowe)
