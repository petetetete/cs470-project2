# Metadata
__author__ = "Peter Huettl"


class SearchNode:

  # Member variables
  label = "#"
  value = -1

  def __init__(self, label, value):
    self.label = label
    self.value = value

  def __str__(self):
    return "(" + self.label + ", " + str(self.value) + ")"
