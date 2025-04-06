import networkx as nx
import numpy as np

START_NODE = 0

def change_graph(graph, orders):

    shortest_paths = nx.shortest_path(graph)

    nodes = list(orders.items.keys())
    nodes = [START_NODE] + [node for node in nodes]
    graph = nx.Graph()

    for src in nodes:
        for dst in nodes:
            if src == dst:
                continue

            path = shortest_paths[src][dst]

            edge_data = dict(
                path=path,
                distance = len(path) - 1,
            )

            graph.add_edge(src, dst, **edge_data)

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

# graph = nx.read_adjlist('../../../generated_graphs/graph_4_4.adjlist')
# x = change_graph(graph)
# print(x)