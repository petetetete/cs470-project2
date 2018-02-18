# Metadata
__author__ = "Peter Huettl"

# Imports
from search import GraphSearch
from search import SearchNode

# Test GraphSearch

# Initialize graph search
print("Loading graph file")
gs = GraphSearch("test_data/30.txt")
print("Graph loaded:", gs.graph)

# Set goals
gs.set_start("U")
gs.set_goal("T")
gs.show_open()

# Generate successors
successors = gs.generate_successors(gs.open_list[0])
print("'U' Successors:", successors)

# Insert successors and re-show open
gs.insert_nodes(successors, "order")
gs.show_open()

# Test duplicates
gs.insert_nodes([SearchNode("K", 500),
                 SearchNode("C", 19),
                 SearchNode("J", 10)])
gs.show_open()
