# generate warehouse graph to txt file

import networkx as nx
import argparse

def main(rows, cols, skip_cols):
    
    G = nx.Graph()
    
    for i in range(rows*cols):
        G.add_node(i)


    for row in range(rows):
        for col in range(cols-1):
            G.add_edge(row * cols + col, row * cols + col + 1)

    for col in range(cols):
        if not col % skip_cols:
            continue
        for row in range(rows-1):
            G.add_edge(row*cols + col, (row+1)*cols + col)
            

    nx.write_adjlist(G, f"generated_graphs/graph_{rows}_{cols}.adjlist")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser dla funkcji main")
    parser.add_argument("--rows", type=int, default=4, help="Liczba wierszy, domyślnie 10")
    parser.add_argument("--cols", type=int, default=4, help="Liczba kolumn, domyślnie 10")
    parser.add_argument("--skip_cols", type=int, default=2, help="Pomijane kolumny, domyślnie 1")

    args = parser.parse_args()
    main(args.rows, args.cols, args.skip_cols)
