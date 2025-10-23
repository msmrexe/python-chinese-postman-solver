# cpp_solver/graph.py

"""
Contains the weighted Graph class.
"""

import json
from collections import defaultdict, Counter

class Graph:
    """
    Represents a weighted, undirected graph that supports
    parallel edges (multi-graph).
    """
    
    def __init__(self):
        # self.edges[u][v] = count of edges
        self.edges = defaultdict(Counter)
        # self.weights[(u, v)] = weight
        self.weights = {}
        self.vertices = set()
        self.total_weight = 0

    def add_edge(self, u: str, v: str, weight: int):
        """Adds a weighted, undirected edge between u and v."""
        u, v = str(u), str(v)
        self.edges[u][v] += 1
        self.edges[v][u] += 1
        
        # Store weight for both directions for easy lookup
        # This assumes weight is the same in both directions
        self.weights[(u, v)] = weight
        self.weights[(v, u)] = weight
        
        self.vertices.add(u)
        self.vertices.add(v)
        self.total_weight += weight

    def get_degree(self, vertex: str) -> int:
        """Returns the total degree of a vertex (sum of all edges)."""
        return sum(self.edges[vertex].values())

    def get_odd_degree_vertices(self) -> list[str]:
        """Returns a list of all vertices with an odd degree."""
        return [v for v in self.vertices if self.get_degree(v) % 2 != 0]

    def _is_connected(self) -> bool:
        """
        Checks if all vertices with a non-zero degree are
        part of a single connected component.
        """
        start_node = None
        for v in self.vertices:
            if self.get_degree(v) > 0:
                start_node = v
                break
        if start_node is None:
            return True # Trivial
            
        visited = {v for v in self.vertices if self.get_degree(v) == 0}
        stack = [start_node]
        visited.add(start_node)
        
        while stack:
            u = stack.pop()
            for v in self.edges[u]:
                if v not in visited:
                    visited.add(v)
                    stack.append(v)
        
        return len(visited) == len(self.vertices)

    @classmethod
    def from_json(cls, file_path: str):
        """Creates a Graph instance from a JSON file."""
        g = cls()
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            if "edges" not in data:
                raise ValueError("JSON file must have an 'edges' key.")

            for u, v, weight in data["edges"]:
                g.add_edge(u, v, int(weight))
                
        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'")
            return None
        except Exception as e:
            print(f"Error loading graph: {e}. Ensure edges are [u, v, weight].")
            return None
            
        return g
