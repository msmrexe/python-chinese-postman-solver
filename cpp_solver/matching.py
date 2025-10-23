# cpp_solver/matching.py

"""
Finds the Minimum Weight Perfect Matching for the
odd-degree vertices.

Uses a brute-force recursive approach that is
sufficient for the small number of odd vertices
(guaranteed to be even) typical in these problems.
"""

def get_all_pairings(nodes: list) -> list[list[tuple]]:
    """
    Recursively generates all possible perfect pairings
    for a list of nodes.
    
    e.g., [1, 2, 3, 4] ->
      [[(1,2), (3,4)], [(1,3), (2,4)], [(1,4), (2,3)]]
    """
    if not nodes:
        yield []
        return
    
    first = nodes[0]
    rest = nodes[1:]
    
    for i in range(len(rest)):
        second = rest[i]
        remaining = rest[:i] + rest[i+1:]
        
        for sub_pairing in get_all_pairings(remaining):
            yield [(first, second)] + sub_pairing

def find_min_weight_matching(odd_vertices: list[str], costs: dict) -> tuple[list, int]:
    """
    Finds the pairing of odd-degree vertices with the
    minimum total weight.
    
    Args:
        odd_vertices: List of odd-degree node names.
        costs: The all-pairs shortest path cost matrix
               (e.g., costs['u']['v'] = cost).

    Returns:
        A tuple (best_pairing, min_cost):
        - best_pairing: A list of (u, v) tuples.
        - min_cost: The total cost of this pairing.
    """
    min_cost = float('inf')
    best_pairing = []
    
    for pairing in get_all_pairings(odd_vertices):
        current_cost = 0
        for u, v in pairing:
            current_cost += costs[u][v]
            
        if current_cost < min_cost:
            min_cost = current_cost
            best_pairing = pairing
            
    return best_pairing, min_cost
