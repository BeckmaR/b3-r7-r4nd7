"""
Script that computes the shortest path between two nodes in a graph.
"""

import requests
from graph import Graph

__author__ = "René Beckmann"
__email__ = "rene.bckmnn@gmail.com"

JSON_URL = "https://www.get-in-it.de/imgs/it/codingCompetition/graph/generatedGraph.json"

START = "Erde"
TARGET = "b3-r7-r4nd7"

def get_json():
    """
    Load the json-formatted map data from the server.
    :return: The data in dictionary form.
    """
    response = requests.get(JSON_URL)
    if response.status_code != 200:
        raise Exception("Could not not load json file!")
    return response.json()


# Load data from URL
data = get_json()

# Build graph from nodes and edges
graph = Graph(data["nodes"], data["edges"])

start_node = graph[START]
target_node = graph[TARGET]

path = graph.shortest_path(start_node, target_node)

print("\nPath computed:")
print(path)
print("Distance:")
print(target_node.distance)
