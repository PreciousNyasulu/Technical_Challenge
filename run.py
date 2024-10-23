import networkx as nx 

class Graph:
    def __init__(self, airports, routes):
        self.graph = nx.DiGraph() 
        self.graph.add_nodes_from(airports)
        self.graph.add_edges_from(routes)

    def calculate_min_additional_routes(self, starting_airport):
        # get all strongly connected components from graph, Directed graph BTW
        components = list(nx.strongly_connected_components(self.graph))
        compressed_graph, mapping = self._compress_graph(components)

        # get the in-degrees for nodes 
        in_degrees = dict(compressed_graph.in_degree())
        count = 0
        
        # Count strongly connected comps with zero in-degree 
        for node in compressed_graph.nodes():
            if in_degrees[node] == 0 and node != mapping[starting_airport]: # skip the starting_aitpot
                count += 1

        return count

    def _compress_graph(self, components):
        compressed_graph = nx.DiGraph()  
        mapping = {}
        
        # Map a node to respective Strongly connected comp
        for i, component in enumerate(components):
            for node in component:
                mapping[node] = i
            compressed_graph.add_node(i) 
        
   
        for u, v in self.graph.edges():
            if mapping[u] != mapping[v]:  # make sure its only strongly connected comps
                compressed_graph.add_edge(mapping[u], mapping[v])

        return compressed_graph, mapping


airports = ["DSM", "ORD", "BGI", "LGA", "JFK", "TLV", "DEL", "CDG", "SIN", "DOH", "HND", "ICN", "SFO", "SAN", "BUD", "EWR", "LHR", "EYW"]
routes = [("DSM", "ORD"), ("ORD", "BGI"), ("BGI", "LGA"), ("LGA", "JFK"), ("TLV", "DEL"), ("DEL", "DOH"), ("CDG", "SIN"), ("HND", "ICN"), 
          ("SFO", "SAN"), ("SAN", "BUD"), ("EWR", "HND"), ("LHR", "EYW")]

starting_airport = "JFK"

graph = Graph(airports, routes)
min_routes = graph.calculate_min_additional_routes(starting_airport)
print(f"Min. number of additional_routes for {starting_airport}: ", min_routes)
