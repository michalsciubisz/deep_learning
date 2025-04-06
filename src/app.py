from pathlib import Path
from typing import List
import numpy as np
import networkx as nx
import json
import matplotlib.pyplot as plt
from algorithms.interface import Order
from objects.robot import Robot, RobotSize
from objects.warehouse import Warehouse
from algorithms.genetics.other import generate_random_solution
from algorithms.genetics.genetic import GeneticAlgorithm
from algorithms.swarm import AntAlgorithm

INPUT_DATA_DIR = Path('D:\\semestr_8\\GUiIO\\projekt\\deep_learning\\input_data')

def test_genetic():
    with open(INPUT_DATA_DIR / 'robots/robotsg1.json', 'r') as f:
        sizes = json.load(f)

    with open(INPUT_DATA_DIR / 'orders/order2v2.json', 'r') as f:
        order = json.load(f)

    graph = nx.read_adjlist(INPUT_DATA_DIR / 'graphs/10_10.adjlist')

    robots = [
        Robot(f'{i+1}', size)
        for i, size in enumerate(sizes)
    ]
    warehouse = Warehouse(graph, robots)
    order = {int(k): v for k, v in order.items()}

    warehouse.graph = nx.relabel_nodes(warehouse.graph, {n: int(n) for n in warehouse.graph})

    GeneticAlg = GeneticAlgorithm(Order(order), warehouse)
    GeneticAlg.run(100, 30)


    # longest = calculate_one(solution, warehouse)
    # print(GeneticAlg.best_solution)    
    x_vec = np.linspace(1, len(GeneticAlg.best_list), len(GeneticAlg.best_list))

    plt.step(x_vec, GeneticAlg.best_list, color='b', linestyle='-')
    plt.title('Step plot of change of cost function', fontsize=14)
    plt.xlabel('Iteration', fontsize=12)
    plt.ylabel('Value of cost function', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(['Cost function'], loc='best', fontsize=10)
    plt.tight_layout() 
    plt.show()

    # return list_best

def test_case_1():
    with open(INPUT_DATA_DIR / 'robots\\robots1.json', 'r') as f:
        sizes = json.load(f)

    with open(INPUT_DATA_DIR / 'orders\\order1.json', 'r') as f:
        order = json.load(f)

    graph = nx.read_adjlist(INPUT_DATA_DIR / 'graphs\\10_10.adjlist')

    robots = [
        Robot(f'{i+1}', size)
        for i, size in enumerate(sizes)
    ]
    warehouse = Warehouse(graph, robots)
    order = {int(k): v for k, v in order.items()}

    alg = AntAlgorithm.from_input_data(order, warehouse)
    alg.solve(
        iter=1000,
        alpha=0.1,
        beta=0.1,
        decay_rate=0.01
    )

    # here will be generating plots script etc.

    return alg


if __name__ == '__main__':
    test_genetic()
    # test_case_1()
