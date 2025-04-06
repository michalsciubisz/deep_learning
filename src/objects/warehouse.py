import networkx as nx
from typing import List
from .robot import Robot


class Warehouse:
    def __init__(self, graph: nx.Graph, robots: List[Robot]) -> None:
        self.graph = graph
        self.robots = robots