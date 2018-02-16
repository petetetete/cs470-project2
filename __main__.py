# Metadata
__author__ = "Peter Huettl"

# Imports
import scipy.spatial as graph
from graph.graphviz import GraphViz


def load_graph(file_name):

  # Get file contents
  with open(file_name) as file:
    lines = [line.rstrip() for line in file]

  # Iterate over file lines
  for line in lines:

    # Remove unecessary characters
    line = line.replace('\'', '')\
               .replace('[', '').replace(']', '').replace(' ', '').strip('()')

    # Unpack line into variables
    [n1, n2, ev, x1, y1, x2, y2] = line.split(",")
    print(ev)


# load_graph("data/30.txt")

g = GraphViz()
g.loadGraphFromFile("data/30.txt")
g.plot()
