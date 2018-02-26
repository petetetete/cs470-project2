# Metadata
__author__ = "Peter Huettl"

# Imports
from search import GraphSearch
from search import Heuristics


# Test GraphSearch

gs = GraphSearch("DEPTH", "test_data/300.txt", Heuristics.hSLD, False, False)
gs.set_start("DG")
gs.set_goal("GR")
gs.go()
