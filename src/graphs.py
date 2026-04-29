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
    

    def dijkstra_linear(self, source):
        #TODO add print of shortest distance and reconstruct path
        #Set source dist to 0 and all others to infinity
        source_vertex = self.vertex_data.index(source)
        dist = [float("inf")] * self.size
        dist[source_vertex] = 0

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
        
        return dist 

             






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
    
    def dijkstra_linear(self, source):
        #TODO add print of shortest distance and reconstruct path
        source_vertex = self.vertex_data.index(source)
        dist = [float('inf')] * self.size
        dist[source_vertex] = 0

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

        return dist
    
    def dijkstra_priority(self, source):
        #TODO implement the priority version
        pass

#sparse graph 1 from instructions
graph = AdjList(6)
graph.add_vertex_data(0, 'A')
graph.add_vertex_data(1, 'B')
graph.add_vertex_data(2, 'C')
graph.add_vertex_data(3, 'D')
graph.add_vertex_data(4, 'E')
graph.add_vertex_data(5, 'F')

graph.add_edge(0,1,4)
graph.add_edge(0,2,2)
graph.add_edge(1,3,5)
graph.add_edge(2,3,1)
graph.add_edge(3,4,3)
graph.add_edge(4,5,2)

print("\nDijkstra's Algorithm starting from vertex D:")
distances = graph.dijkstra_linear('D')
for i , d in enumerate(distances):
    print(f"Distance from D to {graph.vertex_data[i]}: {d}")
