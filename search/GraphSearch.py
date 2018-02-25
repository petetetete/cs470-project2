# Metadata
__author__ = "Peter Huettl"

# Imports
from graph import GraphViz
from .SearchNode import SearchNode
from .GraphNode import GraphNode


class GraphSearch:

  def __init__(self, search_type="BREADTH", graph_file=None,
               verbose=False, heuristic=None):

    # Initialize variables
    self.graph_viz = GraphViz()
    self.search_type = search_type
    self.verbose = verbose
    self.heuristic = heuristic

    self.graph = []
    self.open_list = []
    self.expansion_history = []

    self.start_node = None
    self.goal_nodes = []

    # Stats
    self.frontier_sizes = []
    self.branching_sizes = []

    # Load file if parameter is present
    if graph_file is not None:
      self.load_graph(graph_file)

    print("Loaded search type", search_type)

  # Load graph file into search
  def load_graph(self, file_name):

    # Initialize viz
    self.graph_viz.loadGraphFromFile(file_name)
    self.graph_viz.plot()
    self.graph_file = file_name

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
      node1.add_edge(node2, ev)
      node2.add_edge(node1, ev)

    print("Loaded map in file", file_name)

  # Print the open list
  def show_open(self):
    print("Open list:", self.open_list)

  # Set the starting node of the graph
  def set_start(self, label):

    label = label.upper()  # Ensure label is capitalized

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
    self.__insert_nodes([SearchNode(label)])  # Insert initial search node

  # Set the goal node of the graph
  def set_goal(self, label):

    label = label.upper()  # Ensure label is capitalized

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
    self.goal_nodes.append(node)
    self.graph_viz.markGoal(label)

  # Method used to insert nodes into the open list
  def __insert_nodes(self, search_nodes, type="front"):

    skip_labels = [n.label for n in self.open_list] + self.expansion_history
    search_nodes = [n for n in search_nodes if n.label not in skip_labels]

    if type == "front":
      self.open_list = search_nodes + self.open_list
    elif type == "back":
      self.open_list = self.open_list + search_nodes
    else:  # "order"
      self.open_list = sorted(search_nodes + self.open_list,
                              key=lambda n: n.value)

  # Method used to generate all successor nodes of a search node
  def __generate_successors(self, search_node):

    # Find graph node and create list of new nodes
    graph_node = self.__find_node(search_node.label)
    new_nodes = []

    # TODO: Consider
    # history_labels = [n.label for n in search_node.path_history]
    # new_edges = [n for n in graph_node.edges if n[0].label
    #              not in history_labels]

    # Create new SearchNodes and append past node's history
    for edge in graph_node.edges:
      node = SearchNode(edge[0].label, search_node.depth + 1,
                        search_node.path_cost + edge[1])
      node.path_history = search_node.path_history + [search_node]
      new_nodes.append(node)

    return sorted(new_nodes)

  # Method to find a node in the graph
  def __find_node(self, label):
    return next((node for node in self.graph if node.label == label), None)

  def __print_stats(self, end_node):

    # Calculate missing stats
    node_count = len(self.graph)
    expand_count = len(self.expansion_history)
    short_history = [n.label for n in end_node.path_history] + [end_node.label]
    frontier_average = round(sum(self.frontier_sizes) /
                             len(self.frontier_sizes), 2)
    frontier_max = max(self.frontier_sizes)
    branching_average = round(sum(self.branching_sizes) /
                              len(self.branching_sizes), 2)

    # Print out final stats
    print("------------------------")
    print("SEARCH SUMMARY STATS:")
    print("Search Type:", self.search_type + ".",
          "Map file:", self.graph_file,
          "Total Nodes in Graph:", node_count)
    print("Start node:", self.start_node.label,
          "; Goal node(s):", self.goal_nodes)
    print("Searched total of", expand_count,
          "nodes out of total", node_count, "in graph")
    print("Ended at Node:", end_node.label,
          "with path cost:", end_node.path_cost)
    print("Path (" + str(len(short_history)) + "):", short_history)
    print("Frontier size: Average =", frontier_average,
          "; Max Depth =", frontier_max)
    print("Average branching factor =", branching_average)
    print("Order of Node Expansion:", self.expansion_history)

  # Execute the search!
  def go(self):

    # Initial kick off print
    print(self.search_type, "search: from",
          self.start_node.label, "to", self.goal_nodes)

    # While there are any nodes to explore
    while len(self.open_list) > 0:

      # Get the current node to explore
      explore_node = self.open_list.pop(0)

      # Update stats
      self.expansion_history.append(explore_node.label)
      self.frontier_sizes.append(len(self.open_list))

      # We found the goal
      if any(n.label == explore_node.label for n in self.goal_nodes):
        self.__print_stats(explore_node)
        return

      # Generate and insert successors
      successors = self.__generate_successors(explore_node)
      self.branching_sizes.append(len(successors))
      self.__insert_nodes(successors, "back")

      # Provide feedback if verbose mode is enabled
      if self.verbose:
        print("Exploring node:", explore_node.label)
        print("Open list:", self.open_list)
