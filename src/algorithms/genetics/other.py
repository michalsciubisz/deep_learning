import networkx as nx
import random
from objects.robot import Robot
from algorithms.interface import AlgorithmOutput, Order, RobotRoute
from typing import Dict, List, Tuple
from objects.warehouse import Warehouse
from math import ceil

from algorithms.genetics.transform_graph import change_graph


def fill_routes(solution: AlgorithmOutput, items_left: Order, weights: Dict[int, int], warehouse):
    for i, quantity in items_left.items.items():
        times = calculate_times(solution, warehouse)
        subtracted = 0
        for k in range(len(times)):
            temp_robot = min(times, key=times.get)
            times.pop(temp_robot)
            temp_cap = capacity_left(temp_robot, solution.result[temp_robot], weights)
            if temp_cap > 0:
                if temp_cap < weights[i] * (quantity-subtracted):
                    for j in range(quantity-subtracted):
                        if capacity_left(temp_robot, solution.result[temp_robot], weights) > weights[i]:
                            if i in solution.result[temp_robot].route:
                                solution.result[temp_robot].items[i] += 1
                            else:
                                solution.result[temp_robot].route.append(i)
                                solution.result[temp_robot].items[i] = 1
                            subtracted += 1
                else:
                    if i in solution.result[temp_robot].route:
                        solution.result[temp_robot].items[i] += quantity - subtracted
                    else:
                        solution.result[temp_robot].route.append(i)
                        solution.result[temp_robot].items[i] = quantity - subtracted
                    subtracted += quantity - subtracted

            if items_left.items[i] == subtracted:
                break


def get_weights(orders: Dict) -> Dict:
    weight_dict = {}
    weight_range = [0.2, 0.2, 0.3, 0.4, 0.5] #adjust as needed
    # weight_range = [2, 1, 1.5, 3]
    index = 0

    for item_id in orders.keys():
        weight_dict[item_id] = weight_range[index % len(weight_range)] #repetitive result weight depend on index of edge
        index += 1

    return weight_dict


def capacity_left(robot: Robot, route: RobotRoute, weights: Dict[int, int]) -> int:
    s = 0
    for i, quantity in route.items.items():
        s += weights[i] * quantity  # I need this weights dict that says which item weighs how much
    return robot.load_capacity - s


def rank_selection(population: List[Tuple]) -> List[AlgorithmOutput]:
    solutions_to_take = int(ceil(len(population) * parents_to_population_rate))  # I want to take 2/3 of the solutions

    return [solution[0] for solution in population[:solutions_to_take]]


def calculate_times(robots: AlgorithmOutput, warehouse: Warehouse) -> Dict[Robot, float]: #must be float since distance is normalised
    distance_dict = {}

    graph_transformed = warehouse.graph
    distance_dict_norm = nx.get_edge_attributes(graph_transformed, 'distance')

    distance_dict_norm = {tuple(int(key) for key in keys): value for keys, value in distance_dict_norm.items()}

    for robot, (route, _) in robots.result.items():     

        total_distance = 0

        for i in range(len(route) - 1):

            if route == [0, 0]:
                break

            u = route[i]
            v = route[i+1]

            # total_distance += distance_dict_norm[(u, v)]

            try:
                total_distance += distance_dict_norm[(u, v)]
            except KeyError:
                total_distance += distance_dict_norm[(v, u)]

        distance_dict[robot] = float("{:.2f}".format(total_distance))
    
    times_dict = {robot: float("{:.2f}".format(distance_dict[robot] * robot.calculate_velocity())) for robot in distance_dict.keys()}

    return times_dict


def calculate_one(solution: AlgorithmOutput, warehouse: Warehouse) -> float: #assumed that it's robot id?
    return max(calculate_times(solution, warehouse).values()) 
        


def calculate_all(population: List[AlgorithmOutput], warehouse: Warehouse) -> List[float]:  # albo float
    return [calculate_one(sol, warehouse) for sol in population]


def generate_random_solution(orders: Order, warehouse: Warehouse) -> AlgorithmOutput:
    solution = {}

    graph = warehouse.graph
    robot_list = warehouse.robots

    weight_dict = get_weights(orders)

    picked_items = {item_id: 0 for item_id in orders}

    for robot in robot_list:
        route = [0]  #starting point for each robot
        items = {}  #tracking gathered items
        curr_capacity = robot.load_capacity

        for _ in range(len(orders)):
            if curr_capacity <= 0:
                break

            #filter out items that have already been picked
            available_items = [item_id for item_id in orders.keys() if picked_items[item_id] < orders[item_id]]


            if not available_items:
                break

            item_id = random.choice(available_items)  #random item to pick up

            max_items_to_pick = curr_capacity // weight_dict[item_id]
            amount_to_pick = min(orders[item_id] - picked_items[item_id], max_items_to_pick)

            if amount_to_pick == 0:
                continue

            # shortest_paths = nx.shortest_path(graph, route[-1], item_id)
            route.append(item_id)

            items[item_id] = int(amount_to_pick)
            curr_capacity -= amount_to_pick * weight_dict[item_id]
            picked_items[item_id] += amount_to_pick #tracking already picked items

        # shortest_paths = nx.shortest_path(graph, route[-1], 0) #return to starting point
        route.append(0)

        solution[robot] = RobotRoute(route=route, items=items)

    return AlgorithmOutput(solution)


def generate_population(count: int, orders, warehouse) -> List[AlgorithmOutput]:
    return [generate_random_solution(orders, warehouse) for _ in range(count)]


def cut_zeros(solution: AlgorithmOutput):
    for route in solution.result.values():
        if len(route.route) > 1:
            route.route.pop(0)
            route.route.pop()


def add_zeros(solution: AlgorithmOutput):
    for route in solution.result.values():
        # if len(route.route) > 1:
        route.route.insert(0, 0)
        route.route.append(0)


parents_to_population_rate = 2 / 3
