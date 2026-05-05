# Dijkstra's Algorithm Analysis

Performance comparison of Dijkstra's algorithm using different data structures.

## What It Does

- Implements Dijkstra's algorithm with:
  - Array-based linear search: O(V²)
  - Priority queue (binary heap): O((V + E) log V)
- Measures execution time and memory usage
- Compares performance across sparse and dense graphs

## Authors

Catalina Padilla & Robert Vanderburg  
CS361-001, Spring 2026

Full analysis available at: [https://github.com/catalinaep/Dijkstras-Algorithm-Analysis](https://github.com/catalinaep/Dijkstras-Algorithm-Analysis)

## Quick Start

```bash
# Install dependencies
pip install pandas matplotlib

# Run hand-crafted graph tests (prints to terminal)
python graphs.py

# Run random graph analysis (generates plots)
# Edit graphs.py: set RUN_GRAPH_ANALYSIS = True
python graphs.py
```

## Running the Code

### Option 1: Hand-Crafted Graph Analysis (Default)

Runs analysis on 5 pre-defined test graphs (2 sparse, 3 dense) and prints results to terminal:

```bash
python graphs.py
```

**Output includes:**
- Execution time (milliseconds)
- Memory usage (bytes)
- Shortest path and cost
- Distance from source to all vertices

### Option 2: Random Graph Analysis

Generates 50 random graphs and produces performance comparison plots:

1. Open `graphs.py`
2. Set `RUN_GRAPH_ANALYSIS = True` (line ~480)
3. Run:
```bash
   python graphs.py
```

## Customization

### Modify Test Parameters

In `random_graph_analysis()` (line ~370):
```python
num_vertices = random.randint(100, 1000)  # Change vertex range
edge_density = random.random()            # Change density distribution
weight_range = (15, 30)                   # Change edge weight range
```

### Add Custom Graphs

Add to the `GRAPHS` dictionary:
```python
GRAPHS['MY_GRAPH'] = {
    'vertices': ['A', 'B', 'C'],
    'weights': [(0, 1, 5), (1, 2, 3), (0, 2, 7)]
}
```