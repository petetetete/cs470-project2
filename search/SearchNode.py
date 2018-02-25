# Metadata
__author__ = "Peter Huettl"


class SearchNode:

  def __init__(self, label=None, depth=0, path_cost=0, heuristic_cost=0):
    self.label = label
    self.depth = depth
    self.path_cost = path_cost
    self.heuristic_cost = heuristic_cost
    self.value = path_cost + heuristic_cost
    self.path_history = []
    self.edges = []

  # To string method
  def __repr__(self):
    delim = ";".join([self.label, str(self.depth), str(self.path_cost),
                      str(self.heuristic_cost), str(self.value)])
    return "'" + delim + "'"

  # Method used for comparison of search nodes
  def __lt__(self, other):
    return self.label < other.label
