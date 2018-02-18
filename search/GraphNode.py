# Metadata
__author__ = "Peter Huettl"


class GraphNode:

  edges = []  # List of tuples of the format: (GraphNode, edge_value)

  def __init__(self, label, x_coord, y_coord):
    self.label = label
    self.x_coord = x_coord
    self.y_coord = y_coord

  def add_edge(self, graph_node):
    self.edges.append(graph_node)

  def __repr__(self):
    return self.label
