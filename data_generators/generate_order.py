import random

def generate_orders(num_orders, num_nodes, weight_range):
    """
    Generate a dictionary of orders where the keys are node IDs and the values are product weights.
    
    :param num_orders: Number of orders to generate
    :param num_nodes: Number of nodes in the graph (assumes node IDs start from 1 to num_nodes)
    :param weight_range: Tuple indicating the range of weights (inclusive)
    :return: Dictionary of orders with node ID as key and product weight as value
    """
    if num_orders > num_nodes:
        raise ValueError("Number of orders cannot exceed the number of available nodes")

    # Randomly select unique node IDs
    selected_node_ids = random.sample(range(1, num_nodes + 1), num_orders)

    # Assign a random weight to each selected node ID
    orders = {node_id: random.randint(*weight_range) for node_id in selected_node_ids}

    return orders

# Example usage:
orders = generate_orders(30, 100, (1, 20))
print(orders)

orders = {10: 3, 44: 18, 39: 18, 76: 7, 6: 4, 56: 10, 53: 8, 13: 12, 31: 6, 14: 19, 49: 9, 92: 9, 32: 19, 16: 16, 98: 5, 63: 15, 89: 5, 51: 14, 85: 9, 45: 13, 80: 16, 21: 11, 68: 10, 67: 9, 37: 20, 4: 16, 93: 2, 33: 6, 5: 4, 26: 4}
