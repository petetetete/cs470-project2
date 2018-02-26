# Metadata
__author__ = "Peter Huettl"

# Imports
from search import GraphSearch
from search import Heuristics


# Test GraphSearch

gs = GraphSearch("DEPTH", "test_data/30.txt", Heuristics.hSLD, False, True)
gs.set_start("AB")
gs.set_goal("V")
gs.go()
