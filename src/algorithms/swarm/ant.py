import math

import numpy as np

START_NODE = '0'


class Ant:
    def __init__(self, graph, max_capacity: int, velocity_factor: float):
        self.graph = graph
        self.max_capacity = max_capacity
        self.velocity_factor = velocity_factor

        self.reset()

    def reset(self):
        self.path = [START_NODE]
        self.capacity = self.max_capacity

        self.pause_ctr = 0

        self.runtime_data = {
            "total_distance": 0,
            "load_history": []
        }

    def tick(self):
        if self.pause_ctr == 0:
            self.act()

        self.pause_ctr -= 1

    def act(self):
        self.move()
        self.take_item()
        self.set_pause_ctr()

    def move(self):
        current_node = self.path[-1]
        next_node = self.choose_next_node(current_node)
        if current_node == next_node == START_NODE:
            return

        self.add_to_path(next_node)

    def take_item(self):
        node = self.path[-1]

        if node == START_NODE:
            return

        load = min(self.capacity, self.graph.nodes[node]['weight_left'])

        self.capacity -= load
        self.graph.nodes[node]['weight_left'] -= load

    def set_pause_ctr(self):
        current_node, next_node = self.path[-2], self.path[-1]
        if current_node == next_node == START_NODE:
            self.pause_ctr = np.inf
            return

        distance = self.graph[current_node][next_node]['distance']

        self.pause_ctr = max(math.ceil(distance / self.velocity_factor), 1)

        self.runtime_data['total_distance'] += distance

    def add_to_path(self, node):
        self.path.append(node)
        if node == START_NODE:
            self.on_visit_start_node()

    def choose_next_node(self, current_node):
        if self.capacity <= 0:
            return START_NODE

        available_nodes = [
            node for node in self.graph.neighbors(current_node)
            if self.graph.nodes[node]['weight_left'] > 0
        ]
        if not available_nodes:
            return START_NODE

        return self.sample_node(current_node, available_nodes)

    def sample_node(self, current_node, available_nodes):
        probs = np.array([
            self.graph[current_node][neighbor]['p']
            for neighbor in available_nodes
        ])

        if not probs.any():
            print(current_node, available_nodes)
            probs = np.array([1] * len(available_nodes))

        probs = probs / probs.sum()

        return np.random.choice(available_nodes, p=probs)

    def on_visit_start_node(self):
        total_load = self.max_capacity - self.capacity
        self.runtime_data['load_history'].append(total_load)

        self.capacity = self.max_capacity
