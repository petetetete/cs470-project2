# Metadata
__author__ = "Peter Huettl"

# Imports
from graph import GraphViz
from search import GraphSearch

import sys

# g = GraphViz()
# g.loadGraphFromFile("test_data/30.txt")
# g.plot()
# g.markStart("U")
# g.markGoal("T")

x = GraphSearch("test_data/30.txt")
x.set_start("U")
x.set_start("T")

# print(sys.argv)
