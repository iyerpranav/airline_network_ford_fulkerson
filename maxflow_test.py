import pandas as pd
import networkx as nx

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('data.csv')

# Create a MultiDiGraph
G = nx.MultiDiGraph()

# Add edges to the graph from the DataFrame
for row in df.itertuples():
    G.add_edge(row.source, row.destination, capacity=row.capacity, identifier=row.index)

# Now G is a MultiDiGraph containing all the edges with their capacities
print("Graph created with nodes:", G.nodes)
print("Graph created with edges:")
for i in G.edges(data=True):
    print(i)
