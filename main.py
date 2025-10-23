# main.py

"""
Chinese Postman Problem (CPP) Solver - CLI

This script is the main entry point for finding the shortest
tour that covers all edges in a weighted, undirected graph.
"""

import argparse
from cpp_solver.graph import Graph
from cpp_solver.postman import solve_chinese_postman

def main():
    """Parses CLI arguments and runs the CPP solver."""
    
    parser = argparse.ArgumentParser(
        description="Find the optimal Chinese Postman (Route Inspection) tour."
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the .json file defining the graph's weighted edges."
    )
    args = parser.parse_args()

    # 1. Load the graph from the JSON file
    print(f"Loading graph from '{args.input_file}'...")
    graph = Graph.from_json(args.input_file)
    
    if graph is None:
        print("Failed to load graph. Exiting.")
        return

    # 2. Solve the Chinese Postman Problem
    print("Solving Chinese Postman Problem...")
    circuit, cost = solve_chinese_postman(graph)
    
    # 3. Print the results
    if circuit:
        print("\n--- Optimal Tour Found ---")
        print(f"Total Tour Cost (Weight): {cost}")
        print("\nTour Path (visiting all edges):")
        print(" -> ".join(circuit))
    else:
        print("\n--- No Solution ---")
        print(f"Error: {cost}")

if __name__ == "__main__":
    main()
