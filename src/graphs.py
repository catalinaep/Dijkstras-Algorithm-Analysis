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


GRAPHS = {
        'SG1': {
            'vertices': 'ABCDEF',
            'weights': [(0,1,4), (0,2,2), (1,3,5), (2,3,1), (3,4,3), (4,5,2)]
        },
        'SG2': {
            'vertices': '1234567',
            'weights': [(0,1,3), (0,2,6), (1,3,2), (2,4,4), (3,5,6), (4,6,1), (1,4,5)]
        },
        'DG1': {
            'vertices': 'ABCDE',
            'weights': [
                (0,1,2), (0,2,5), (0,3,1), (0,4,4), (1,2,3), (1,3,2), (1,4,6), 
                (2,3,3), (2,4,1), (3,4,2)
            ]
        },
        'DG2': {
            'vertices': '123456',
            'weights': [
                (0,1,3), (0,4,5), (1,2,1), (2,3,3), (3,4,2), (4,5,1), (0,2,2), (1,3,2), 
                (1,4,4), (2,4,6), (0,3,6), (0,5,4), (1,5,7), (2,5,5), (3,5,4)
            ]
        }
    }

class AdjMatrix:
    def __init__(self, size):
        self.size = size # number of vertices
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.vertex_data = [''] * size
        
    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            #graph is expected to be undirected
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data
    

    def dijkstra_linear(self, source, target):
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
                        
        return self.print_path(source, target_index, dist, parent_nodes) 

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


        print("Shortest path:", " -> ".join(path))
        print("Total cost:", dist[target_index])

        for i, d in enumerate(dist):
            print(f"Distance from {source} to {self.vertex_data[i]}: {d}")    
         

################################################################################


class AdjList:
    def __init__(self, size):
        self.adj_list = {}
        #names of vertices
        self.vertex_data = [''] * size
        self.size = size
    
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
        return self.print_path(source, target_index, dist, parent_nodes)

        
    
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


        print("Shortest path:", " -> ".join(path))
        print("Total cost:", dist[target_index])

        for i, d in enumerate(dist):
            print(f"Distance from {source} to {self.vertex_data[i]}: {d}")
    
    def dijkstra_priority(self, source):
        source_vertex = self.vertex_data.index(source)
        dist = [float('inf')] * self.size
        dist[source_vertex] = 0

        prev = [None] * self.size

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
                        prev[v] = u
                        heapq.heappush(pq, (relax, v))
        return dist


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


if __name__ == "__main__":
    #SPARSE GRAPH 1 ADJ MATRIX TESTING====================================
    sparse_graph1= AdjList(6)
    print("ADJ LIST TEST SPARSE GRAPH 1========================")

    load_vertex_weights('SG1', sparse_graph1)
    #linear testing
    sparse1_linear_time = measure_time(sparse_graph1.dijkstra_linear, 'A', 'F')
    sparse1_linear_mem = measure_memory(sparse_graph1.dijkstra_linear, 'A', 'F')
    print("\n===================================================")
    print(f"Graph 1 Linear Time Results (Adj List): {sparse1_linear_time:.6f}ms")
    print(f"Graph 1 Linear Memory Results (Adj List): {sparse1_linear_mem:.6f}")

    #heap testing
    sparse1_heap_time = measure_time(sparse_graph1.dijkstra_priority, 'A')
    sparse1_heap_mem = measure_memory(sparse_graph1.dijkstra_priority, 'A')
    print("\n===================================================")
    print(f"Graph 1 Heap Time Results (Adj List): {sparse1_heap_time:.6f}ms")
    print(f"Graph 1 Heap Memory Results (Adj List): {sparse1_heap_mem:.6f}")
    
    
    #SPARSE GRAPH 2 ADJ LIST TESTING======================================
    sparse_graph2= AdjList(6)
    print("ADJ LIST TEST SPARSE GRAPH 2========================")

    load_vertex_weights('SG2', sparse_graph2)
    #linear testing
    sparse2_linear_time = measure_time(sparse_graph2.dijkstra_linear, '1', '6')
    sparse2_linear_mem = measure_memory(sparse_graph2.dijkstra_linear, '1', '6')
    print("\n===================================================")
    print(f"Graph 2 Linear Time Results (Adj List): {sparse2_linear_time:.6f}ms")
    print(f"Graph 2 Linear Memory Results (Adj List): {sparse2_linear_mem:.6f}")

    #heap testing
    sparse2_heap_time = measure_time(sparse_graph2.dijkstra_priority, '1')
    sparse2_heap_mem = measure_memory(sparse_graph2.dijkstra_priority, '1')
    print("\n===================================================")
    print(f"Graph 2 Heap Time Results (Adj List): {sparse2_heap_time:.6f}ms")
    print(f"Graph 2 Heap Memory Results (Adj List): {sparse2_heap_mem:.6f}")