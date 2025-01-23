"""Implementation of Ford-Fulkerson Algorithm with BFS for Max Flow"""
from collections import deque, defaultdict
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


class Graph:
    """Represents a directed graph with capacities and residuals."""

    def __init__(self, dataframe):
        self.graph = nx.MultiDiGraph()
        self._build_graph(dataframe)

    def _build_graph(self, dataframe):
        """Build the graph from a DataFrame."""
        for row in dataframe.itertuples():
            u = row.src_airport_code
            v = row.dstn_airport_code
            cap = row.capacity
            self.graph.add_edge(u, v, weight=cap, residual=cap, identifier=row.Index)
            self.graph.add_edge(v, u, weight=0, residual=0)

    def visualize_network(graph):
        """Visualizes the network using Matplotlib."""
        plt.figure(figsize=(10, 6))

        # Layout for better positioning of nodes
        pos = nx.spring_layout(graph, seed=42)

        # Draw nodes and edges
        nx.draw(graph, pos, with_labels=True, node_color="skyblue", edge_color="gray", node_size=2000, font_size=10)

        # Draw edge labels (capacities)
        edge_labels = {(u, v): f"{d['weight']}/{d['residual']}" for u, v, d in graph.edges(data=True)}
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)

        plt.title("Flow Network Visualization")
        plt.show()

    def get_networkx_graph(self):
        """Return the underlying NetworkX graph."""
        return self.graph


class FordFulkerson:
    """Implements the Ford-Fulkerson algorithm to find max flow."""

    def __init__(self, graph):
        self.graph = graph
        self.paths = defaultdict(list)

    def bfs(self, source, sink, parent):
        """Breadth-First Search to find an augmenting path."""
        queue = deque([source])
        visited = set([source])
        parent.clear()

        while queue:
            current = queue.popleft()

            for neighbour, edge_data in self.graph[current].items():
                residual = edge_data[0]['residual']

                if neighbour not in visited and residual > 0:
                    parent[neighbour] = current

                    if neighbour == sink:
                        path = []
                        node = sink
                        while node in parent:
                            path.append(node)
                            node = parent[node]
                        path.append(source)
                        path.reverse()

                        self.paths[sink].append((path, None))
                        return True

                    visited.add(neighbour)
                    queue.append(neighbour)

        return False

    def compute_max_flow(self, source, sink):
        """Calculate the maximum flow from source to sink."""
        max_flow = 0
        parent = {}

        while self.bfs(source, sink, parent):
            current = sink
            path_flow = float('Inf')

            while current != source:
                prev = parent[current]
                residual = self.graph[prev][current][0]['residual']
                path_flow = min(path_flow, residual)
                current = prev

            # Update the last path's flow
            self.paths[sink][-1] = (self.paths[sink][-1][0], path_flow)

            current = sink
            while current != source:
                prev = parent[current]
                self.graph[prev][current][0]['residual'] -= path_flow
                self.graph[current][prev][0]['residual'] += path_flow
                current = prev

            max_flow += path_flow

        return max_flow

class csv_handler:
    """this class handles all the interactions with csv files of this script"""
    
    def __init__(self):
        self.dataframe = pd.DataFrame()

    def read_data(self, path):
        self.dataframe = pd.read_csv(path)
        return self.dataframe
    
    def export_flows(self, graph):
        for u, v, data in graph.edges(data=True):
            
            

if __name__ == "__main__":
    # Load network data
    csv_object = csv_handler()
    network_df = csv_object.read_data("flight_network.csv")

    # Initialize graph and algorithm
    graph_obj = Graph(network_df)
    ntwrk = graph_obj.get_networkx_graph()
    ford_fulkerson = FordFulkerson(ntwrk)

    # Compute max flow
    src, snk = "BOM", "MAA"
    flow_max = ford_fulkerson.compute_max_flow(src, snk)

    # Output results
    print(f"Max Flow: {flow_max}\n")
    if snk in ford_fulkerson.paths:
        print(f"All augmenting paths to {snk} and their flows:")
        for _path, flow in ford_fulkerson.paths[snk]:
            print(f"Path: {_path}, Flow: {flow}")
    else:
        print(f"No paths to sink {snk}.")
