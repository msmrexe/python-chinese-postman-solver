# cpp_solver/eulerian.py

"""
Implements Hierholzer's algorithm for finding an
Eulerian path or circuit in a graph (or multi-graph).
"""

import copy

def find_eulerian_circuit(graph_edges, start_node: str) -> list[str]:
    """
    Finds an Eulerian circuit using Hierholzer's algorithm.
    
    Assumes the graph is Eulerian.
    
    Args:
        graph_edges: The adjacency list (Counter) to "burn".
        start_node: The node to start from.

    Returns:
        The circuit path (list of vertex names).
    """
    
    # We use a copy of the edge Counters to "burn" edges
    graph_copy = copy.deepcopy(graph_edges)
    
    stack = [start_node]
    path = []
    
    while stack:
        u = stack[-1]
        
        # If the vertex has neighbors
        if graph_copy[u]:
            # Get an arbitrary neighbor
            v = next(iter(graph_copy[u]))
            
            # Push neighbor to stack and "burn" the edge
            stack.append(v)
            
            # Remove edge (u, v) from the copied graph
            graph_copy[u][v] -= 1
            graph_copy[v][u] -= 1
            if graph_copy[u][v] == 0:
                del graph_copy[u][v]
            if graph_copy[v][u] == 0:
                del graph_copy[v][u]
        else:
            # If no neighbors, add to final path
            path.append(stack.pop())
            
    path.reverse()
    return path
