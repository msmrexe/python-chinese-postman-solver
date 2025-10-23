# Chinese Postman Problem Solver

This project is a Python solution for the undirected, weighted **Chinese Postman Problem (CPP)**, also known as the **Route Inspection Problem**. It was developed for an Algorithms & Data Structures course to find the *cheapest possible tour* that visits every single edge of a graph at least once and returns to the starting point.

This is the classic "National Park Tour" or "snowplow" problem: how do you drive down every street in a neighborhood (visiting all *edges*) in the shortest/cheapest possible distance, given that some streets are dead ends?

---

## The Problem: Chinese Postman Requirements

The key to this problem is understanding **Eulerian paths**, which are paths that visit every *edge* exactly once.

### Scenario 1: The "Perfect" Neighborhood (Eulerian Circuit)

If every single intersection (vertex) in the neighborhood has an **even** number of streets (edges) connected to it, the problem is simple. You can start at any intersection, walk down every street exactly once, and end up right back where you started. This is called an **Eulerian Circuit**.

* **Solution:** The shortest tour is just the circuit itself.
* **Total Cost:** The sum of all edge weights in the graph.

### Scenario 2: The "Real-World" Neighborhood (The Real Problem)

In any real map, you have dead ends and intersections with 3, 5, or 7 streets. These are **odd-degree vertices**.

* **The Problem:** If a graph has *any* odd-degree vertices, an Eulerian Circuit is **impossible**. Every time you enter an intersection, you must also leave it. An odd-degree vertex guarantees that you will eventually enter one and have no unvisited edge to leave on, getting "stuck."
* **The Goal:** To solve the problem, we must "fix" the graph by re-traveling (duplicating) some streets until all vertices are even-degree.
* **The Challenge:** We can't just re-travel *any* streets. We must re-travel the **cheapest possible paths** to keep the total tour distance/cost minimal.

This is why the graph **must be weighted**. The weights represent the **cost** (distance/time) of each street. We need to find the cheapest path between odd vertices, not just *any* path.

---

## The 5-Step Solution (How It Works)

This project solves the Chinese Postman Problem by implementing the standard 5-step algorithm:

### 1. Identify Odd-Degree Vertices
First, the program checks the degree of every vertex in the graph. It creates a list of all vertices that have an odd number of edges (e.g., `['A', 'C', 'E', 'F']`). If this list is empty, the graph is already Eulerian, and we skip to Step 5.

### 2. Find All-Pairs Cheapest Paths
We can't just connect odd vertices `A` and `C` with the direct edge `(A, C)` if a shorter path like `A-B-C` exists. We must find the *absolute cheapest path* between all pairs of odd-degree vertices. This is done by running **Dijkstra's algorithm** starting from each odd vertex.

### 3. Find Minimum Weight Perfect Matching
This is the heart of the solution. We now have a list of odd vertices and the least cost to get from any of them to any other. We must find the "cheapest" way to pair them all up.

For example, with 4 nodes `(A, B, C, D)`, we compare:
* Cost of `(A,B) + (C,D)`
* Cost of `(A,C) + (B,D)`
* Cost of `(A,D) + (B,C)`

The algorithm finds the pairing with the **minimum total cost**. This project uses a recursive, brute-force matching algorithm, which is effective for the small number of odd vertices in typical problems.

### 4. Augment the Graph
With the best pairings found, the algorithm "fixes" the graph. It creates a new *multi-graph* (a graph that can have multiple edges between two nodes). It adds:
1.  All the edges from the *original* graph.
2.  *New* edges corresponding to the *cheapest paths* found in the matching (Step 3).

This new "augmented" graph is now **guaranteed to be Eulerian**. All its vertices will have an even degree.

### 5. Find the Eulerian Circuit
The problem is now simple again. The algorithm runs **Hierholzer's Algorithm** (an efficient $O(V+E)$ method) on the new, augmented graph to find the final circuit. This circuit is the cheapest possible tour that visits every original edge at least once.

The **Total Tour Cost** is: `(Sum of all original edge weights) + (Cost of the min-weight matching)`.

---

## Features

* Solves the full, weighted, undirected Chinese Postman Problem.
* **Weighted Graph** implementation that supports multi-graphs.
* **Dijkstra's Algorithm** for finding all-pairs cheapest paths.
* **Minimum Weight Perfect Matching** to find the optimal paths to duplicate.
* **Hierholzer's Algorithm** ($O(V+E)$) to find the final Eulerian circuit.
* Loads graphs from a flexible, weighted `JSON` file.
* Structured as a clean, modular Python package (`cpp_solver`).

## Project Structure

```
python-chinese-postman-solver/
├── .gitignore
├── LICENSE
├── README.md                # This documentation
├── main.py                  # Main runnable script (CLI)
├── sample_graph.json        # An example weighted graph input
└── cpp_solver/
    ├── __init__.py          # Makes 'cpp_solver' a package
    ├── graph.py             # Weighted Graph class
    ├── shortest_paths.py    # Dijkstra's algorithm
    ├── matching.py          # Min-Weight Perfect Matching logic
    ├── eulerian.py          # Hierholzer's algorithm
    └── postman.py           # The main CPP orchestrator
```

## How to Run

1.  **Create a graph file.**
    Create a file like `my_graph.json` with a list of weighted edges `[node1, node2, weight]`, with `weight` being the cost of that edge/road:
    ```json
    {
        "edges": [
            ["A", "B", 4],
            ["A", "C", 8],
            ["B", "C", 3],
            ["C", "D", 2],
            ["C", "E", 4],
            ["D", "E", 1],
            ["D", "F", 6],
            ["E", "F", 2]
        ]
    }
    ```

3.  **Run the program:**
    ```bash
    # Run on the sample graph
    python main.py sample_graph.json
    
    # Run on your new graph
    python main.py my_graph.json
    ```

### Example Output (for `sample_graph.json`)

```
$ python main.py sample_graph.json
Loading graph from 'sample_graph.json'...
Solving Chinese Postman Problem...
Found 4 odd-degree vertices: ['C', 'A', 'F', 'E']
Finding all-pairs shortest paths...
Finding minimum weight perfect matching...
Minimum matching cost: 7
Augmenting graph with new edges...
Finding Eulerian circuit in augmented graph...

--- Optimal Tour Found ---
Total Tour Cost (Weight): 37

Tour Path (visiting all edges):
C -> A -> B -> C -> E -> D -> F -> E -> D -> C -> ...
```
*(The path will be long, and the starting point may vary, but it will trace the optimal tour)*

---

## Author

Feel free to connect or reach out if you have any questions!

* **Maryam Rezaee**
* **GitHub:** [@msmrexe](https://github.com/msmrexe)
* **Email:** [ms.maryamrezaee@gmail.com](mailto:ms.maryamrezaee@gmail.com)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.
