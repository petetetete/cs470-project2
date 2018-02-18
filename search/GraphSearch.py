# Metadata
__author__ = "Peter Huettl"

# Imports
from graph import GraphViz
from .SearchNode import SearchNode
from .GraphNode import GraphNode


class GraphSearch:

  graph = []
  graph_viz = None
  verbose = False
  open_list = []
  start_node = None
  end_node = None

  def __init__(self, graph_file=None):

    self.graph_viz = GraphViz()

    # Load file if parameter is present
    if graph_file is not None:
      self.load_graph(graph_file)

  def load_graph(self, file_name):

    # Loading feedback and initialize viz
    print("Loading graph file...")
    self.graph_viz.loadGraphFromFile(file_name)
    self.graph_viz.plot()

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

      # Get or create node 1
      node1 = self.find_node(n1)
      if node1 is None:
        node1 = GraphNode(n1, x1, y1)
        self.graph.append(node1)

      # Get or create node 2
      node2 = self.find_node(n2)
      if node2 is None:
        node2 = GraphNode(n2, x2, y2)
        self.graph.append(node2)

      # Add edges to the nodes
      node1.add_edge((node2, ev))
      node2.add_edge((node1, ev))

    # Load complete feedback
    print("Graph loaded: ", self.graph, "\n")

  def show_open(self):
    print("Open list:", self.open_list)

  def set_start(self, label):

    # Catch unloaded graph error
    if self.graph is None:
      print("Error: Graph is not loaded")
      return

    # Find specified node
    node = self.find_node(label)
    if node is None:
      print("Error: Unable to find starting node label")
      return

    # Set member variables
    self.start_node = node
    self.graph_viz.markStart(label)

  def set_end(self, label):

    # Catch unloaded graph error
    if self.graph is None:
      print("Error: Graph is not loaded")
      return

    # Find specified node
    node = self.find_node(label)
    if node is None:
      print("Error: Unable to find ending node label")
      return

    # Set member variables
    self.end_node = node
    self.graph_viz.markGoal(label)

  def find_node(self, label):
    return next((node for node in self.graph if node.label == label), None)

  def insert_node(self, graph_node):
    self.open_list.append(SearchNode(graph_node.label, 0))


# Test the class
if __name__ == "main":
  print("[TODO] Tests here...")
