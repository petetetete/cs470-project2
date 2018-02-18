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

    # Initialize visualizer
    self.graph_viz = GraphViz()

    # Load file if parameter is present
    if graph_file is not None:
      self.load_graph(graph_file)

  # Load graph file into search
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
      node1 = self.__find_node(n1)
      if node1 is None:
        node1 = GraphNode(n1, x1, y1)
        self.graph.append(node1)

      # Get or create node 2
      node2 = self.__find_node(n2)
      if node2 is None:
        node2 = GraphNode(n2, x2, y2)
        self.graph.append(node2)

      # Add edges to the nodes
      node1.add_edge((node2, int(ev)))
      node2.add_edge((node1, int(ev)))

    # Load complete feedback
    print("Graph loaded: ", self.graph)

  # Print the open list
  def show_open(self):
    print("Open list:", self.open_list)

  # Set the starting node of the graph
  def set_start(self, label):

    # Catch unloaded graph error
    if self.graph is None:
      print("Error: Graph is not loaded")
      return

    # Find specified node
    node = self.__find_node(label)
    if node is None:
      print("Error: Unable to find starting node label")
      return

    # Set member variables
    self.start_node = node
    self.graph_viz.markStart(label)
    self.insert_node(label)

  # Set the goal node of the graph
  def set_goal(self, label):

    # Catch unloaded graph error
    if self.graph is None:
      print("Error: Graph is not loaded")
      return

    # Find specified node
    node = self.__find_node(label)
    if node is None:
      print("Error: Unable to find ending node label")
      return

    # Set member variables
    self.end_node = node
    self.graph_viz.markGoal(label)

  # Method used to insert nodes into the open list
  def insert_node(self, label):
    self.open_list.append(SearchNode(label, 0))

  # Method used to generate all successor nodes of a search node
  def generate_successors(self, search_node):

    # Find graph node and create list of new nodes
    graph_node = self.__find_node(search_node.label)
    new_nodes = sorted(list(map(
      lambda e: SearchNode(e[0].label, search_node.value + e[1]),
      graph_node.edges)))

    return new_nodes

  # Helper methods

  # Method to find a node in the graph
  def __find_node(self, label):
    return next((node for node in self.graph if node.label == label), None)


# Test the class
if __name__ == "main":
  print("[TODO] Tests here...")
