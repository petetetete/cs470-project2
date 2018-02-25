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
