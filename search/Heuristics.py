# Metadata
__author__ = "Peter Huettl"

# Imports
import numpy as np
import math


# Straight light distance heuristic
def hSLD(prev_node, graph_node, goal_nodes):

  # Calculate the straight line distance to each goal node
  distances = []
  for goal_node in goal_nodes:
    a = np.array((graph_node.x_coord, graph_node.y_coord))
    b = np.array((goal_node.x_coord, goal_node.y_coord))
    distances.append(np.linalg.norm(a - b))

  # Return the closest value
  return min(distances)


# General node direction heursitic
def hDir(prev_node, graph_node, goal_nodes):

  SCALE = 5  # Used to scale the impact of bad angles

  # Calculate the angles to each goal node
  angles = []
  for goal_node in goal_nodes:

    # Get points on the triangle formed between the 3 points
    A = np.array((graph_node.x_coord, graph_node.y_coord))
    B = np.array((goal_node.x_coord, goal_node.y_coord))
    C = np.array((prev_node.x_coord, prev_node.y_coord))

    # Get the side lengths of the triangle
    a = np.linalg.norm(B - C)
    b = np.linalg.norm(A - C)
    c = np.linalg.norm(A - B)

    # Calculate the angle between the goal node and the prospective node
    angle = math.acos((a**2 + b**2 - c**2) / (2 * a * b))
    angles.append(SCALE * angle * 180 / math.pi)

  # Return the smallest angle value
  return min(angles)
