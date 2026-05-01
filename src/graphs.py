"""
 * Dijkstra Implementation Analysis (Project 2)
 * 
 *   Course: CS361
 *  Section: 001
 *  Authors:
 *     Catalina Padilla
 *     Robert Vanderburg
 *  Project: Dijkstra Impelemntation Analysis
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
        #TODO add print of shortest distance and reconstruct path
        #Set source dist to 0 and all others to infinity
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


if __name__ == "__main__":
    
    #sparse graph 1 from instructions
    graph = AdjList(6)

    load_vertex_weights('SG1', graph)

    print("\nDijkstra's Algorithm starting from vertex D:")
    distances = graph.dijkstra_linear('D')
    priority_dist = graph.dijkstra_priority('D')
    for i , d in enumerate(distances):
        print(f"Distance from D to {graph.vertex_data[i]}: {d}")

    print("\nDijkstra's Priority starting from vertex D:")
    for i , d in enumerate(priority_dist):
        print(f"Distance from D to {graph.vertex_data[i]}: {d}")
