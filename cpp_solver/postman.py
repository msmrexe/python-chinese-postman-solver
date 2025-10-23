# cpp_solver/postman.py

"""
The main orchestrator that solves the
Chinese Postman Problem (CPP).
"""

from .graph import Graph
from .shortest_paths import find_all_pairs_shortest_paths, reconstruct_path
from .matching import find_min_weight_matching
from .eulerian import find_eulerian_circuit

def solve_chinese_postman(graph: Graph) -> tuple[list, int]:
    """
    Solves the undirected, weighted Chinese Postman Problem.

    Args:
        graph: The input Graph object.

    Returns:
        A tuple (circuit, total_cost):
        - circuit: The list of vertices in the optimal tour.
        - total_cost: The total weight of the optimal tour.
    """
    
    # 1. Check connectivity
    if not graph._is_connected():
        return None, "Graph is not connected. No solution."
        
    # 2. Identify all odd-degree vertices
    odd_vertices = graph.get_odd_degree_vertices()
    
    # If no odd-degree vertices, graph is already Eulerian
    if not odd_vertices:
        print("Graph is already Eulerian.")
        start_node = next(iter(graph.vertices))
        circuit = find_eulerian_circuit(graph.edges, start_node)
        return circuit, graph.total_weight

    print(f"Found {len(odd_vertices)} odd-degree vertices: {odd_vertices}")
    
    # 3. Find all-pairs shortest paths between odd vertices
    print("Finding all-pairs shortest paths...")
    costs, paths = find_all_pairs_shortest_paths(graph, odd_vertices)
    
    # 4. Find the minimum weight perfect matching
    print("Finding minimum weight perfect matching...")
    matching_pairs, matching_cost = find_min_weight_matching(odd_vertices, costs)
    print(f"Minimum matching cost: {matching_cost}")

    # 5. Create the augmented graph
    print("Augmenting graph with new edges...")
    augmented_graph = Graph()
    
    # 5a. Add all original edges
    for u in graph.edges:
        for v, count in graph.edges[u].items():
            if u <= v: # To avoid adding edges twice
                weight = graph.weights[(u, v)]
                for _ in range(count):
                    augmented_graph.add_edge(u, v, weight)

    # 5b. Add all new edges from the matching
    for u, v in matching_pairs:
        path = reconstruct_path(paths[u], u, v)
        for i in range(len(path) - 1):
            n1 = path[i]
            n2 = path[i+1]
            weight = graph.weights[(n1, n2)]
            augmented_graph.add_edge(n1, n2, weight)
            
    # 6. Find the Eulerian circuit in the augmented graph
    print("Finding Eulerian circuit in augmented graph...")
    start_node = odd_vertices[0]
    circuit = find_eulerian_circuit(augmented_graph.edges, start_node)
    
    total_cost = graph.total_weight + matching_cost
    
    return circuit, total_cost
