from typing import List

import networkx as nx
import numpy as np

from objects.warehouse import Warehouse

from .adapter import transform_graph
from .ant import START_NODE, Ant


class AntAlgorithm:
    MAX_ITER = 10_000

    def __init__(self, graph: nx.Graph, ants: List[Ant]) -> None:
        self.graph = graph
        self.ants = ants

        self.runtime_data = {
            'best_solutions': [],
            'best_scores': [],
        }

        self.reset_iter_state()

    def solve(self, iter: int, alpha: float, beta: float, decay_rate: float):
        self.runtime_data['params'] = {
            "iter": iter,
            "alpha": alpha,
            "beta": beta,
            "decay_rate": decay_rate,
        }
        
        best_score = np.inf
        best_solution = None

        for it in range(iter):
            result = self.simulate()

            if result['score'] < best_score:
                best_score = result['score']
                best_solution = [
                    {
                        'id': i + 1,
                        'total_distance': ant.runtime_data['total_distance'],
                        'capacity': ant.max_capacity,
                        'velocity': ant.velocity_factor,
                        'total_load': sum(ant.runtime_data['load_history']),
                        'path': ant.path,
                    }
                    for i, ant in enumerate(self.ants)
                ]
                self.runtime_data['best_solutions'].append(best_solution)
                self.runtime_data['best_scores'].append((it, best_score))

                print(f'Found better score {best_score} in iteration {it}')

            self.update_pheromone(decay_rate)
            self.update_probs(alpha, beta)

            self.reset_iter_state()

        return best_solution

    def reset_iter_state(self):
        for ant in self.ants:
            ant.reset()

        nx.set_node_attributes(self.graph, {
            node: {
                "weight_left": self.graph.nodes[node]['weight']
            }
            for node in self.graph.nodes()
        })

    def set_max_pheromone(self):
        nx.set_edge_attributes(self.graph, {
            (u, v): {
                'pheromone': 1,
            }
            for u, v in self.graph.edges()
        })

    def update_pheromone(self, decay_rate: float) -> None:
        self.update_edge_load()

        for u, v in self.graph.edges():
            updated_pheromone = (1 - decay_rate) * self.graph[u][v]['pheromone'] + self.graph[u][v]['load_fraction']  # noqa

            self.graph[u][v]['pheromone'] = updated_pheromone

    def update_probs(self, alpha: float, beta: float) -> None:
        for u, v in self.graph.edges():
            pheromone = self.graph[u][v]['pheromone'] ** alpha
            heuristic = self.graph[u][v]['distance_norm'] ** beta

            p = pheromone * heuristic

            nx.set_edge_attributes(self.graph, {
                (u, v): {
                    'p': p
                }
            })

    def update_edge_load(self):
        for u, v in self.graph.edges():
            self.graph[u][v]['edge_load'] = 10e-5
        for ant in self.ants:
            it = 0
            loads = ant.runtime_data['load_history']
            for src, dst in zip(ant.path[:-1], ant.path[1:]):
                self.graph[src][dst]['edge_load'] += loads[it]
                if dst == START_NODE:
                    it += 1

        max_load = max(
            self.graph[u][v]['edge_load']
            for u, v in self.graph.edges()
        )
        total_load = sum(
            self.graph[u][v]['edge_load']
            for u, v in self.graph.edges()
        )

        load_even = 1.0 / self.graph.number_of_edges() if max_load == 0 else None

        for u, v in self.graph.edges():
            self.graph[u][v]['load_norm'] = load_even or self.graph[u][v]['edge_load'] / max_load
            self.graph[u][v]['load_fraction'] = load_even or self.graph[u][v]['edge_load'] / total_load

    def simulate(self):
        i = 0
        while not self.stop_simulation():
            for ant in self.ants:
                ant.tick()
            i += 1

            if i > self.MAX_ITER:
                raise StopIteration("Maximum iteration count exceeded.")

        score = max(
            ant.runtime_data['total_distance'] / ant.velocity_factor
            for ant in self.ants
        )

        return {
            "iter": i,
            "score": score
        }

    def stop_simulation(self):
        weights_left = sum(
            self.graph.nodes[node]['weight_left']
            for node in self.graph.neighbors(START_NODE)
        )
        ants_returned = (
            ant.path[-1] == START_NODE
            for ant in self.ants
        )
        return weights_left <= 0 and all(ants_returned)

    @classmethod
    def from_input_data(cls, orders, warehouse: Warehouse):
        graph = transform_graph(warehouse.graph, orders)
        ants = [
            Ant(
                graph,
                robot.load_capacity,
                robot.velocity,
            )
            for robot in warehouse.robots
        ]

        return cls(graph, ants)
