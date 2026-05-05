"""
 * Dijkstra Implementation Analysis (Project 2)
 * 
 *   Course: CS361
 *  Section: 001
 *  Authors:
 *     Catalina Padilla
 *     Robert Vanderburg
 *  Project: Dijkstra Implementation Analysis
 * Filename: graphs.py
 * 
 * Description:
 * Implements Dijkstra's algorithm using 3 different data structures: an array, a matrix, and a min-
 * heap priority queue. Provides an analysis on timing and memory usage across the different
 * implementations.
"""

import heapq
import time
import sys
import tracemalloc
import random

import pandas as pd
import matplotlib.pyplot as plt

# Dictionary representation of the graphs.
GRAPHS = {
        'SG1': {
            'vertices': ['A','B','C','D','E','F'],
            'weights': [(0,1,4), (0,2,2), (1,3,5), (2,3,1), (3,4,3), (4,5,2)]
        },
        'SG2': {
            'vertices': ['1','2','3','4','5','6','7'],
            'weights': [(0,1,3), (0,2,6), (1,3,2), (2,4,4), (3,5,7), (4,6,1), (1,4,5)]
        },
        'DG1': {
            'vertices': ['A','B','C','D','E'],
            'weights': [
                (0,1,2), (0,2,5), (0,3,1), (0,4,4), (1,2,3), (1,3,2), (1,4,6), 
                (2,3,3), (2,4,1), (3,4,2)
            ]
        },
        'DG2': {
            'vertices': ['1','2','3','4','5','6'],
            'weights': [
                (0,1,3), (0,4,5), (1,2,1), (2,3,3), (3,4,2), (4,5,1), (0,2,2), (1,3,2), 
                (1,4,4), (2,4,6), (0,3,6), (0,5,4), (1,5,7), (2,5,5), (3,5,4)
            ]
        }
    }

class AdjMatrix:
    """
    Class used to represent Dijkstra using an adjacency matrix.

    :param size: The size of the matrix to be generated.
    """
    def __init__(self, size):
        self.size = size # number of vertices
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.vertex_data = [''] * size
        self.run = []
    
    
    def add_edge(self, u, v, weight):
        """
        Add the edge weight to the matrix. Assumes graphs are undirected.

        :param u: integer representing edges
        :param v: integer representing vertices
        :param weight: integer representing the edge weight.
        """
        if 0 <= u < self.size and 0 <= v < self.size:
            #graph is expected to be undirected
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight


    def add_vertex_data(self, vertex, vertex_tuple):
        """
        Add vertex tuple data including connected vertices and weight (u1, u2, w).

        :param vertex: integer representing a vertex index.
        :param vertex_tuple: tuple representing two connected nodes, including edge weight.
        """
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = vertex_tuple

    def dijkstra_Matrix(self, source, target):
        """
        Matrix searching Dijkstra implementation using a source and target to calculate route. Appends
        path data to the run class attribute.

        :param source: string representation of the source node to start search.
        :param target: string representation of the target node to optimize for.
        """
        source_index = self.vertex_data.index(source)
        target_index = self.vertex_data.index(target)
        dist = [float("inf")] * self.size
        dist[source_index] = 0

        #keeps track of path
        parent_nodes = [None] * self.size

        visited = set()
        
        #find the vertex with the smallest weight
        for _ in range(self.size):
            min_dist = float('inf')
            u = None
            for i in range(self.size):
                if i not in visited and dist[i] < min_dist:
                    min_dist = dist[i]
                    u = i
            
            # All reachable vertices have been visited
            if u is None:
                break

            visited.add(u)

            #for each of u's neighbors, relax the distance and replace if smaller
            for v in range(self.size):
                #check if a neighbor and that it hasn't been visited
                if self.adj_matrix[u][v] != 0 and v not in visited:
                    relaxation = dist[u] + self.adj_matrix[u][v]
                    if relaxation < dist[v]:
                        #replace distance
                        dist[v] = relaxation
                        parent_nodes[v] = u
                        
        self.run = []
        self.run.append((source_index, target_index, dist, parent_nodes))
    
    def print_path(self, source, target_index, dist, parent_nodes):
        """
        Print the path, weights, and individual decisions from source node to target node.

        :param source: String representation of the source node.
        :param target_index: Integer index of the target node.
        :param dist: List of integers representing chosen edge weights for shortes path.
        :param parent_nodes: List of integers representing parent nodes.
        """
        path = []
        curr = target_index

        while curr is not None:
            path.append(self.vertex_data[curr])
            curr = parent_nodes[curr]

        path.reverse()

        if dist[target_index] == float('inf'):
            print("No path to given target")
            return


        print(f"Shortest path @ {dist[target_index]} cost:", " -> ".join(path))

        for i, d in enumerate(dist):
            print(f"Distance from {source} to {self.vertex_data[i]}: {d}")    


class AdjList:
    def __init__(self, size):
        self.adj_list = {}
        #names of vertices
        self.vertex_data = [''] * size
        self.size = size
        self.run = []
    
    def add_vertex(self, v):
        if v not in self.adj_list:
            self.adj_list[v] =[]

    def add_edge(self, u, v, weight=1):
        self.add_vertex(u)
        self.add_vertex(v)

        # graph expected to be undirected
        self.adj_list[u].append((v, weight))
        self.adj_list[v].append((u, weight))
    
    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data
    
    def dijkstra_linear(self, source, target):
        #TODO add print of shortest distance and reconstruct path
        source_index = self.vertex_data.index(source)
        target_index = self.vertex_data.index(target)
        dist = [float('inf')] * self.size
        dist[source_index] = 0
        parent_nodes = [None] * self.size

        visited = set()
        for _ in range(self.size):
            min_dist = float('inf')
            u = None
            for i in range(self.size):
                if i not in visited and dist[i] < min_dist:
                    min_dist = dist[i]
                    u = i
        
        # All reachable vertices have been visited
            if u is None:
                break

            visited.add(u)

            #for each of u's neighbors, relax the distance and replace if smaller
            for v, weight in self.adj_list[u]:
                if v not in visited:
                    relaxation = dist[u] + weight
                    if relaxation < dist[v]:
                        dist[v] = relaxation
                        parent_nodes[v] = u
        self.run = []
        self.run.append((source_index, target_index, dist, parent_nodes))     
    
    def print_path(self, source, target_index, dist, parent_nodes):
        path = []
        curr = target_index

        while curr is not None:
            path.append(self.vertex_data[curr])
            curr = parent_nodes[curr]

        path.reverse()

        if dist[target_index] == float('inf'):
            print("No path to given target")
            return


        print(f"Shortest path @ {dist[target_index]} cost:", " -> ".join(path))

        for i, d in enumerate(dist):
            print(f"Distance from {source} to {self.vertex_data[i]}: {d}")
    
    def dijkstra_priority(self, source, target):
        source_vertex = self.vertex_data.index(source)
        target_index = self.vertex_data.index(target)
        dist = [float('inf')] * self.size
        dist[source_vertex] = 0

        parent = [None] * self.size

        pq = [(0, source_vertex)]

        visited = set()

        while pq:
            current_dist, u = heapq.heappop(pq)

            if u in visited:
                continue

            visited.add(u)

            if current_dist > dist[u]:
                continue

            for v, weight in self.adj_list[u]:
                if v not in visited:
                    relax = dist[u] + weight

                    if relax < dist[v]:
                        dist[v] = relax
                        parent[v] = u
                        heapq.heappush(pq, (relax, v))
        self.run = []
        self.run.append((source_vertex, target_index, dist, parent))


def load_vertex_weights(graph_key, dijkstra):
    """
    Load the given graph data using graph_key from GRAPH into the Dijkstra algorithm class.

    :param graph_key: String value key representing a graph in GRAPH.
    :param dijkstra: AdjMatrix or AdjList class representing algorithm implmentation.
    """
    for idx, n in enumerate(GRAPHS[graph_key]['vertices']):
        dijkstra.add_vertex_data(idx, n)

    for idx, n in enumerate(GRAPHS[graph_key]['weights']):
        dijkstra.add_edge(n[0], n[1], n[2])


def measure_time(func, *args):
    times = []
    for _ in range(5):
        start = time.time()
        func(*args)
        end = time.time()
        times.append(end - start)
    return (sum(times) / 5) * 1000  # ms


def measure_memory(func, *args):
    tracemalloc.start()
    func(*args)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def generate_graph(num_vertices, edge_density, weight_range):
    """
    Generate an udirected graph with the specified vertices, edge density, and weight range.
   
    :param num_vertices: Number of vertices in the graph.
    :param edge_probability: Probability of an edge existing between any two vertices.
    :param weight_range: Tuple (min_weight, max_weight) for edge weights.
    :return graph: Representation of an undirected graph for traversal by disjkra algorithsm.
    """

    # Create vertices string
    vertices = [str(i) for i in range(1,num_vertices+1)]
    
    # Generate edges
    weights = []
    
    # create undirected graph where i < j to avoid duplicate edges.
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if random.random() < edge_density:
                weight = random.randint(weight_range[0], weight_range[1])
                weights.append((i, j, weight))
    
    graph = {
        'vertices': vertices,
        'weights': weights
    }
   
    return graph


    def random_graph_analysis():
        """
        Generates 50 random graphs and measures execution time and memory usage for both priority 
        queue and linear search implementations. Results are displayed as scatter plots comparing performance
        across different graph sizes.
        
        :return: None. Displays matplotlib visualization of results.
        """
        for i in range(50):
            num_vertices = random.randint(100,1000)
            min_weight = random.randint(1,15)
            max_weight = random.randint(16,30)
            edge_density = random.random()
            graph_data = generate_graph(num_vertices, edge_density, (15,30))

            if (edge_density < 0.1):
                GRAPHS["S" + str(i)] = graph_data
            elif (0.1 <= edge_density < 0.3):
                GRAPHS["M" + str(i)] = graph_data
            else:
                GRAPHS["D" + str(i)] = graph_data

        analysis_array = []

        for key, value in GRAPHS.items():
            num_vertices = len(value['vertices'])

            graph = AdjList(num_vertices)
            load_vertex_weights(key, graph)

            source = value['vertices'][random.randint(0, num_vertices//2)]
            target = value['vertices'][random.randint(num_vertices//2, num_vertices-1)]

            priority_graph_time = measure_time(graph.dijkstra_priority, source, target)
            priority_graph_memory = measure_memory(graph.dijkstra_priority, source, target)

            linear_graph_time = measure_time(graph.dijkstra_linear, source, target)
            linear_graph_memory = measure_memory(graph.dijkstra_linear, source, target)

            # Store all metrics
            analysis_array.append({
                'num_vertices': num_vertices,
                'priority_time': priority_graph_time,
                'priority_memory': priority_graph_memory,
                'linear_time': linear_graph_time,
                'linear_memory': linear_graph_memory
            })


        df = pd.DataFrame(analysis_array)
        df = df.sort_values('num_vertices')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Graph 1: Time Comparison (Scatter)
        ax1.scatter(df['num_vertices'], df['priority_time'], 
                s=30, alpha=0.6, label='Priority Queue', color='blue')
        ax1.scatter(df['num_vertices'], df['linear_time'], 
                s=30, alpha=0.6, label='Linear Search', color='red')

        ax1.set_xlabel('Number of Vertices', fontsize=12)
        ax1.set_ylabel('Time (seconds)', fontsize=12)
        ax1.set_title('Dijkstra Algorithm: Time Complexity Comparison', fontsize=14, fontweight='bold')
        ax1.legend(loc='best', fontsize=10)
        ax1.grid(True, alpha=0.3)

        # Graph 2: Memory Comparison (Scatter)
        ax2.scatter(df['num_vertices'], df['priority_memory'], 
                s=30, alpha=0.6, label='Priority Queue', color='blue')
        ax2.scatter(df['num_vertices'], df['linear_memory'], 
                s=30, alpha=0.6, label='Linear Search', color='red')

        ax2.set_xlabel('Number of Vertices', fontsize=12)
        ax2.set_ylabel('Memory (MB)', fontsize=12)
        ax2.set_title('Dijkstra Algorithm: Memory Usage Comparison', fontsize=14, fontweight='bold')
        ax2.legend(loc='best', fontsize=10)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    """
    To run the graph analysis using random graph properties, set RUN_GRAPH_ANALYSIS below to True. 
    Otherwise the 5 handcrafted graphs analysis runs and prints to terminal.
    """
    RUN_GRAPH_ANALYSIS = False

    if (RUN_GRAPH_ANALYSIS):
        random_graph_analysis()
    else:
        #SPARSE GRAPH 1 ADJ MATRIX TESTING====================================
        sparse_graph1= AdjList(6)
        print("\n============| ADJ LIST TEST SPARSE GRAPH 1 |=============")

        load_vertex_weights('SG1', sparse_graph1)
        #linear testing
        sparse1_linear_time = measure_time(sparse_graph1.dijkstra_linear, 'A', 'F')
        sparse1_linear_mem = measure_memory(sparse_graph1.dijkstra_linear, 'A', 'F')
        print("\n===================================================\n")
        print(f"Graph 1 Linear Time Results (Adj List): {sparse1_linear_time:.6f}ms")
        print(f"Graph 1 Linear Memory Results (Adj List): {sparse1_linear_mem:.6f}")
        run = sparse_graph1.run
        sparse_graph1.print_path(run[0][0], run[0][1], run[0][2], run[0][3])


        #heap testing
        sparse1_heap_time = measure_time(sparse_graph1.dijkstra_priority, 'A', 'F')
        sparse1_heap_mem = measure_memory(sparse_graph1.dijkstra_priority, 'A', 'F')
        print("\n===================================================\n")
        print(f"Graph 1 Heap Time Results (Adj List): {sparse1_heap_time:.6f}ms")
        print(f"Graph 1 Heap Memory Results (Adj List): {sparse1_heap_mem:.6f}")
        run = sparse_graph1.run
        sparse_graph1.print_path(run[0][0], run[0][1], run[0][2], run[0][3])
        

        #SPARSE GRAPH 2 ADJ LIST TESTING======================================
        sparse_graph2= AdjList(7)
        print("\n============| ADJ LIST TEST SPARSE GRAPH 2 |============")

        load_vertex_weights('SG2', sparse_graph2)
        #linear testing
        sparse2_linear_time = measure_time(sparse_graph2.dijkstra_linear, '1', '6')
        sparse2_linear_mem = measure_memory(sparse_graph2.dijkstra_linear, '1', '6')
        print("\n===================================================\n")
        print(f"Graph 2 Linear Time Results (Adj List): {sparse2_linear_time:.6f}ms")
        print(f"Graph 2 Linear Memory Results (Adj List): {sparse2_linear_mem:.6f}")
        run = sparse_graph2.run
        sparse_graph2.print_path(run[0][0], run[0][1], run[0][2], run[0][3])

        #heap testing
        sparse2_heap_time = measure_time(sparse_graph2.dijkstra_priority, '1', '6')
        sparse2_heap_mem = measure_memory(sparse_graph2.dijkstra_priority, '1', '6')
        print("\n===================================================\n")
        print(f"Graph 2 Heap Time Results (Adj List): {sparse2_heap_time:.6f}ms")
        print(f"Graph 2 Heap Memory Results (Adj List): {sparse2_heap_mem:.6f}")
        run = sparse_graph2.run
        sparse_graph2.print_path(run[0][0], run[0][1], run[0][2], run[0][3])


        #DENSE GRAPH 1 MATRIX LIST TESTING======================================
        dense_graph1= AdjMatrix(5)
        print("\n============| ADJ MATRIX TEST DENSE GRAPH 1 |============")

        load_vertex_weights('DG1', dense_graph1)
        #matrix testing
        dense_matrix_time = measure_time(dense_graph1.dijkstra_Matrix, 'A', 'E')
        dense_matrix_mem = measure_memory(dense_graph1.dijkstra_Matrix, 'A', 'E')
        print("\n===================================================")
        print(f"Dense Graph 1 Matrix Time Results (Adj List): {dense_matrix_time:.6f}ms")
        print(f"Dense Graph 1 Matrix Memory Results (Adj List): {dense_matrix_mem:.6f}")
        run = dense_graph1.run
        dense_graph1.print_path(run[0][0], run[0][1], run[0][2], run[0][3])

        dense_graph1 = AdjList(5)
        load_vertex_weights('DG1', dense_graph1)
        #heap testing
        dense_heap_time = measure_time(dense_graph1.dijkstra_priority, 'A', 'E')
        dense_heap_mem = measure_memory(dense_graph1.dijkstra_priority, 'A', 'E')
        print("\n===================================================")
        print(f"Dense Graph 1 Heap Time Results (Adj List): {dense_heap_time:.6f}ms")
        print(f"Dense Graph 1 Heap Memory Results (Adj List): {dense_heap_mem:.6f}")
        run = dense_graph1.run
        dense_graph1.print_path(run[0][0], run[0][1], run[0][2], run[0][3])


        #DENSE GRAPH 2 ADJ MATRIX TESTING======================================
        dense_graph2= AdjMatrix(6)
        print("\n============| ADJ MATRIX TEST DENSE GRAPH 2 |============")

        load_vertex_weights('DG2', dense_graph2)
        #matrix testing
        dense_matrix_time = measure_time(dense_graph2.dijkstra_Matrix, '1', '5')
        dense_matrix_mem = measure_memory(dense_graph2.dijkstra_Matrix, '1', '5')
        print("\n===================================================")
        print(f"Dense Graph 2 Matrix Time Results (Adj Matrix): {dense_matrix_time:.6f}ms")
        print(f"Dense Graph 2 Matrix Memory Results (Adj Matrix): {dense_matrix_mem:.6f}")
        run = dense_graph2.run
        dense_graph2.print_path(run[0][0], run[0][1], run[0][2], run[0][3])

        dense_graph2 = AdjList(6)
        load_vertex_weights('DG2', dense_graph2)
        #heap testing
        dense_heap_time = measure_time(dense_graph2.dijkstra_priority, '1', '5')
        dense_heap_mem = measure_memory(dense_graph2.dijkstra_priority, '1', '5')
        print("\n===================================================")
        print(f"Dense Graph 2 Heap Time Results (Adj List): {dense_heap_time:.6f}ms")
        print(f"Dense Graph 2 Heap Memory Results (Adj List): {dense_heap_mem:.6f}")
        run = dense_graph2.run
        dense_graph2.print_path(run[0][0], run[0][1], run[0][2], run[0][3])


        #DENSE GRAPH 2 ADJ MATRIX TESTING======================================
        dense_graph3= AdjMatrix(250)
        print("\n============| ADJ MATRIX TEST DENSE GRAPH 3 |============")

        graph_data = generate_graph(250, 0.5, (5,25))
        GRAPHS['DG3'] = graph_data

        load_vertex_weights('DG3', dense_graph3)
        #matrix testing
        dense_matrix_time = measure_time(dense_graph3.dijkstra_Matrix, '1', '127')
        dense_matrix_mem = measure_memory(dense_graph3.dijkstra_Matrix, '1', '127')
        print("\n===================================================")
        print(f"Dense Graph 3 Matrix Time Results (Adj Matrix): {dense_matrix_time:.6f}ms")
        print(f"Dense Graph 3 Matrix Memory Results (Adj Matrix): {dense_matrix_mem:.6f}")
        run = dense_graph3.run
        dense_graph3.print_path(run[0][0], run[0][1], run[0][2], run[0][3])

        dense_graph3 = AdjList(250)
        load_vertex_weights('DG3', dense_graph3)
        #heap testing
        dense_heap_time = measure_time(dense_graph3.dijkstra_priority, '1', '127')
        dense_heap_mem = measure_memory(dense_graph3.dijkstra_priority, '1', '127')
        print("\n===================================================")
        print(f"Dense Graph 3 Heap Time Results (Adj List): {dense_heap_time:.6f}ms")
        print(f"Dense Graph 3 Heap Memory Results (Adj List): {dense_heap_mem:.6f}")
        run = dense_graph3.run
        dense_graph3.print_path(run[0][0], run[0][1], run[0][2], run[0][3])

    

    

