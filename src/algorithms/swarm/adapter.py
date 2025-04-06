import networkx as nx
import numpy as np

from .ant import START_NODE


def transform_graph(graph, orders):
    shortest_paths = nx.shortest_path(graph)

    nodes = list(orders.keys())
    nodes = [START_NODE] + [str(node) for node in nodes]
    graph = nx.Graph()

    for src in nodes:
        for dst in nodes:
            if src == dst:
                continue
            path = shortest_paths[src][dst]

            edge_data = dict(
                path=path,
                distance=len(path)-1,

                edge_load=1,

                pheromone=1,
                heuristic=1,
                p=1,
            )

            graph.add_edge(src, dst, **edge_data)

    nx.set_node_attributes(graph, {
        node: {
            "weight": orders.get(int(node), np.inf),
            "weight_left": orders.get(int(node), np.inf),
        }
        for node in nodes
    })

    max_distance = max(
        graph[u][v]['distance']
        for u, v in graph.edges
    )

    nx.set_edge_attributes(graph, {
        (u, v): {
            "distance_norm": graph[u][v]['distance'] / max_distance
        }
        for u, v in graph.edges
    })

    return graph
