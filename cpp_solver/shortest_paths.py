# cpp_solver/shortest_paths.py

"""
Contains Dijkstra's algorithm for finding all-pairs
shortest paths.
"""

import heapq

def dijkstra(graph, start_node: str) -> tuple[dict, dict]:
    """
    Finds the shortest paths from a single source node.
    
    Args:
        graph: The Graph object.
        start_node: The starting vertex.

    Returns:
        A tuple (distances, predecessors):
        - distances: {'v': cost, ...}
        - predecessors: {'v': 'u', ...} (u comes before v on path)
    """
    distances = {v: float('inf') for v in graph.vertices}
    predecessors = {v: None for v in graph.vertices}
    distances[start_node] = 0
    
    # Priority queue stores (cost, vertex)
    pq = [(0, start_node)]
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        if current_dist > distances[u]:
            continue
            
        # self.graph.edges[u] is a Counter {neighbor: count}
        # We only care about *if* a neighbor exists, not how many
        for v in graph.edges[u]:
            weight = graph.weights[(u, v)]
            distance = current_dist + weight
            
            if distance < distances[v]:
                distances[v] = distance
                predecessors[v] = u
                heapq.heappush(pq, (distance, v))
                
    return distances, predecessors

def find_all_pairs_shortest_paths(graph, nodes: list[str]) -> tuple[dict, dict]:
    """
    Runs Dijkstra from each node in the 'nodes' list.
    
    Args:
        graph: The Graph object.
        nodes: The list of nodes to find paths between (e.g., odd vertices).

    Returns:
        A tuple (costs, paths):
        - costs: {'u': {'v': cost, ...}, ...}
        - paths: {'u': {'v': 'pred_of_v', ...}, ...}
    """
    all_costs = {}
    all_paths = {}
    
    for node in nodes:
        costs, preds = dijkstra(graph, node)
        all_costs[node] = costs
        all_paths[node] = preds
        
    return all_costs, all_paths

def reconstruct_path(predecessors: dict, u: str, v: str) -> list[str]:
    """Reconstructs a path list from a predecessor dict."""
    path = [v]
    curr = v
    while curr != u:
        curr = predecessors[curr]
        if curr is None:
            return None # No path
        path.append(curr)
    path.reverse()
    return path
