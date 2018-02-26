# Metadata
__author__ = "Peter Huettl"

# Imports
from graph import GraphViz
from .SearchNode import SearchNode
from .GraphNode import GraphNode


class GraphSearch:

  def __init__(self, search_type="BREADTH", graph_file=None,
               heuristic=None, verbose=False, viz_enabled=True):

    # Initialize variables
    self.graph_viz = GraphViz() if viz_enabled else None
    self.search_type = search_type
    self.verbose = verbose
    self.viz_enabled = viz_enabled
    self.using_heuristic = search_type == "A*" and heuristic
    self.heuristic = heuristic if self.using_heuristic else lambda a, b, c: 0

    self.graph = []
    self.open_list = []
    self.expansion_history = []

    self.start_node = None
    self.goal_nodes = []

    # Stat variables
    self.frontier_sizes = []
    self.explore_depths = []
    self.branching_sizes = []

    # Load file if parameter is present
    if graph_file is not None:
      self.load_graph(graph_file)

    print("Loaded search type", search_type)  # Feedback print

  # Load graph file into search
  def load_graph(self, file_name):

    # Save graph file name and initialize viz (if requested)
    self.graph_file = file_name
    if self.viz_enabled:
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
      node1.add_edge(node2, ev)
      node2.add_edge(node1, ev)

    print("Loaded map in file", file_name)  # Feedback print

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
    if self.viz_enabled:
      self.graph_viz.markStart(label)
    self.__insert_nodes([SearchNode(label)], False)  # Insert initial node

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
    if self.viz_enabled:
      self.graph_viz.markGoal(label)

  # Method used to insert nodes into the open list
  def __insert_nodes(self, search_nodes, output=True):

    # Exclude nodes that have already been expanded
    search_nodes = [n for n in search_nodes
                    if n.label not in self.expansion_history]

    if self.search_type == "BREADTH":  # Breadth-first insert algorithm

      # Prioritize labels in the open_list already
      skip_labels = [n.label for n in self.open_list]
      new_nodes = [n for n in search_nodes if n.label not in skip_labels]

      # Add to the back of the list
      self.open_list = self.open_list + new_nodes

    elif self.search_type == "DEPTH":  # Depth-first insert algorithm

      # Prioritize newly added labels
      skip_labels = [n.label for n in search_nodes]
      open_list = [n for n in self.open_list if n.label not in skip_labels]

      # Add to the front of the list
      self.open_list = search_nodes + open_list

    else:  # Best-first/A* insert algorithm

      # Add new nodes to the open list and sort on value
      self.open_list = sorted(search_nodes + self.open_list,
                              key=lambda n: n.value)

      # Trim trailing duplicates from the open_list (the worse nodes)
      seen = {}
      for node in reversed(self.open_list):
        if node.label not in seen:
          seen[node.label] = node
        else:
          self.open_list.remove(seen[node.label])

    if self.verbose and output:  # Print feedback
      print("Inserting new children:", [n.label for n in search_nodes])

  # Method used to generate all successor nodes of a search node
  def __generate_successors(self, search_node):

    # Find graph node and create list of new nodes
    graph_node = self.__find_node(search_node.label)
    new_nodes = []

    for edge in graph_node.edges:

      # Calculate new node metrics
      depth = search_node.depth + 1
      path_cost = search_node.path_cost + edge[1]
      heuristic_cost = self.heuristic(graph_node, edge[0], self.goal_nodes)

      # Create new node and udate history
      node = SearchNode(edge[0].label, depth, path_cost, heuristic_cost)
      node.path_history = search_node.path_history + [search_node]
      new_nodes.append(node)

    return sorted(new_nodes)  # Sort alphabetically

  # Method to find a node in the graph
  def __find_node(self, label):
    return next((node for node in self.graph if node.label == label), None)

  def __print_stats(self, end_node):

    # Calculate missing stats
    node_count = len(self.graph)
    expand_count = len(self.expansion_history)
    path = [n.label for n in end_node.path_history] + [end_node.label]
    frontier_average = round(sum(self.frontier_sizes) /
                             len(self.frontier_sizes), 2)
    frontier_max = max(self.frontier_sizes)
    depth_average = round(sum(self.explore_depths) /
                          len(self.explore_depths), 2)
    depth_max = max(self.explore_depths)
    branching_average = round(sum(self.branching_sizes) /
                              (len(self.branching_sizes) + 1), 2)

    # Print out final stats
    if self.verbose:
      print("Success! Reached goal node", end_node.label, "with path:", path)
    print("------------------------")
    print("SEARCH SUMMARY STATS:")
    print("Search Type:", self.search_type + ".",
          "Map File:", self.graph_file,
          "(" + str(node_count), "total nodes)")
    if self.using_heuristic:
      print("Using h-function:", self.heuristic)
    print("Start Node:", self.start_node.label,
          "; Goal Node(s):", self.goal_nodes)
    print("Searched total of", expand_count,
          "nodes out of total", node_count, "in graph")
    print("Ended at Node:", end_node.label,
          "with path cost:", end_node.path_cost)
    print("Path (" + str(len(path)) + "):", path)
    print("Frontier Size: Average =", frontier_average,
          "; Max Size =", frontier_max)
    print("Depth of Search: Average =", depth_average,
          "; Max Depth =", depth_max)
    print("Average Branching Factor =", branching_average)
    if self.verbose:
      print("Order of Node Expansion:", self.expansion_history)

  # Execute the search!
  def go(self):

    # Initial kick off print
    print("------------------------")
    print(self.search_type, "search: from",
          self.start_node.label, "to", self.goal_nodes)

    # While there are any nodes to explore
    while len(self.open_list) > 0:

      # Get the current node to explore
      explore_node = self.open_list.pop(0)

      if self.verbose:  # Print out the node to be explored
        print("Exploring node:", explore_node.label)

      if self.viz_enabled:  # Paint the node as visibted if viz enabled
        curr_label = explore_node.label
        last_label = (explore_node.path_history[-1].label
                      if len(explore_node.path_history) else curr_label)
        self.graph_viz.exploreNode(curr_label, [last_label, curr_label])

      # Update stats
      self.expansion_history.append(explore_node.label)
      self.frontier_sizes.append(len(self.open_list))
      self.explore_depths.append(explore_node.depth)

      # We found the goal
      if any(n.label == explore_node.label for n in self.goal_nodes):
        self.__print_stats(explore_node)
        return

      # Generate and insert successors
      successors = self.__generate_successors(explore_node)
      self.branching_sizes.append(len(successors))
      self.__insert_nodes(successors)

      if self.viz_enabled:  # Paint added edges if viz enabled
        successor_labels = [n.label for n in successors]
        self.graph_viz.exploreEdges(curr_label, successor_labels)

      if self.verbose:  # Print out current open list
        print("Open list:", self.open_list)
