# Metadata
__author__ = "Peter Huettl"


class SearchNode:

  def __init__(self, label=None, value=None):
    self.label = label
    self.value = value
    self.edges = []

  # To string method
  def __repr__(self):
    return "(" + self.label + ", " + str(self.value) + ")"

  # Method used for comparison of search nodes
  def __lt__(self, other):
    return self.label < other.label
