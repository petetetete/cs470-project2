# Metadata
__author__ = "Peter Huettl"

# Imports
from search import GraphSearch

# Test GraphSearch
x = GraphSearch("test_data/30.txt")
x.set_start("U")
x.set_goal("T")
x.show_open()
successors = x.generate_successors(x.open_list[0])
print("'U' Successors:", successors)
