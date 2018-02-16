# Metadata
__author__ = "Peter Huettl"

# Imports
# from graph import GraphViz


class GraphSearch:

  graph = None

  def __init__(self, graph_file):

    # Load file if parameter is present
    if graph_file is not None:
      self.graph = self.load_graph(graph_file)

  def load_graph(self, file_name):

    # Get file contents
    with open(file_name) as file:
      lines = [line.rstrip() for line in file]

    # Iterate over file lines
    for line in lines:

      # Remove unecessary characters
      line = line.replace('\'', '').replace('[', '')\
                 .replace(']', '').replace(' ', '').strip('()')

      # Unpack line into variables
      [n1, n2, ev, x1, y1, x2, y2] = line.split(",")


# Test the class
if __name__ == "main":
  print("[TODO] Tests here...")
