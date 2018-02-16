# Metadata
__author__ = "Peter Huettl"

# Imports
from graph import GraphViz
from search import GraphSearch

import sys


# def load_graph(file_name):

#   # Get file contents
#   with open(file_name) as file:
#     lines = [line.rstrip() for line in file]

#   # Iterate over file lines
#   for line in lines:

#     # Remove unecessary characters
#     line = line.replace('\'', '')\
#                .replace('[', '').replace(']', '').replace(' ', '').strip('()')

#     # Unpack line into variables
#     [n1, n2, ev, x1, y1, x2, y2] = line.split(",")
#     print(ev)


# load_graph("data/30.txt")

# g = GraphViz()
# g.loadGraphFromFile("test_data/30.txt")
# g.plot()
# g.markStart("U")
# g.markGoal("T")

print(sys.argv)
