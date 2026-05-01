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
        #TODO implement the priority version
        pass

#==========tests==================


graph1= AdjMatrix(6)
print("ADJ MATRIX TEST========================")
graph1.add_vertex_data(0, 'A')
graph1.add_vertex_data(1, 'B')
graph1.add_vertex_data(2, 'C')
graph1.add_vertex_data(3, 'D')
graph1.add_vertex_data(4, 'E')
graph1.add_vertex_data(5, 'F')

graph1.add_edge(0,1,4)
graph1.add_edge(0,2,2)
graph1.add_edge(1,3,5)
graph1.add_edge(2,3,1)
graph1.add_edge(3,4,3)
graph1.add_edge(4,5,2)

graph1.dijkstra_linear('A', 'F')

#list
print("ADJ LIST TEST ======================")
graph2 = AdjList(6)
graph2.add_vertex_data(0, 'A')
graph2.add_vertex_data(1, 'B')
graph2.add_vertex_data(2, 'C')
graph2.add_vertex_data(3, 'D')
graph2.add_vertex_data(4, 'E')
graph2.add_vertex_data(5, 'F')
graph2
graph2.add_edge(0,1,4)
graph2.add_edge(0,2,2)
graph2.add_edge(1,3,5)
graph2.add_edge(2,3,1)
graph2.add_edge(3,4,3)
graph2.add_edge(4,5,2)
graph2
graph2.dijkstra_linear('A', 'D')