# Metadata
__author__ = "Peter Huettl"

# Imports
from search import GraphSearch


# Straight light distance heuristic
def hSLD(graph_node, goal_nodes):

  # Calculate the Straight Line Distance to each goal node
  distances = []
  for goal_node in goal_nodes:
    a = (graph_node.x_coord, graph_node.y_coord, 1)
    b = (goal_node.x_coord, goal_node.y_coord, 1)
    distances.append(((a[0] - b[0])**2 + (a[1] - b[1])**2)**(1 / 2))

  # Return the closest value
  return min(distances)


# Test GraphSearch

gs = GraphSearch("BEST", "test_data/10.txt", hSLD, True, False)
gs.set_start("f")
gs.set_goal("d")
gs.go()


# # Initialize graph search
# print("Loading graph file")
# gs = GraphSearch("test_data/30.txt")
# print("Graph loaded:", gs.graph)

# # Set goals
# gs.set_start("U")
# gs.set_goal("T")
# gs.show_open()

# # Generate successors
# print("\nTest Successors")
# successors = gs.generate_successors(gs.open_list[0])
# print("'U' Successors:", successors)

# # Insert successors and re-show open
# print("\nTest 'In-Order' Insert")
# gs.insert_nodes(successors, "order")
# gs.show_open()

# # Test duplicates
# print("\nTest Duplicate Node Insert")
# gs.insert_nodes([SearchNode("K", 500),
#                  SearchNode("C", 19),
#                  SearchNode("J", 10)])
# gs.show_open()

# print("\nStraight Line Distance Heuristic Tests")

# print("V:", end=" ")
# gs.hSLD(gs.__find_node("V"))
# print("AC:", end=" ")
# gs.hSLD(gs.__find_node("AC"))
# print("J:", end=" ")
# gs.hSLD(gs.__find_node("J"))
