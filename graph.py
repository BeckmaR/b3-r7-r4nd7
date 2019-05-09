"""
An implementation of the Dijkstra algorithm that searches for the shortest path between two nodes
Source and Target in a graph of nodes and edges.
"""

__author__ = "René Beckmann"
__email__ = "rene.bckmnn@gmail.com"

class Node:
    """
    Class that describes a single node in the graph.
    """
    def __init__(self, label):
        # A label that describes the node.
        self.label = label
        # Dictionary of nodes to distances
        self._neighbors = {}
        # The accumulated distance of this node to the source node. Initialized with infinity.
        self.distance = float("inf")
        # The n-1th node on the shortest path from the source node to this one
        self.shortest_source = None
        # Whether this node was already visited by the algorithm
        self.visited = False

    def add_neighbor(self, neighbor, distance):
        """
        Add a new neighbor to this node.
        :param neighbor: A Node object that is directly connected to this one via an edge.
        :param distance: The distance between this node and the neighbor node.
        """
        self._neighbors[neighbor] = distance

    def is_neighbor(self, node):
        """
        Checks if a given node is directly reachable from this node.
        :param node: Node to test
        :return: Boolean
        """
        return node in self._neighbors

    def get_unvisited_neighbors(self):
        """
        All neighbors that were not yet visited.
        :return: iterator of Node objects
        """
        return filter(lambda node : not node.visited, self._neighbors.keys())

    def update_distance(self, source, distance):
        """
        Potentially update the accumulated distance of this node to the source node.
        If the given distance is lower than self.distance, self.distance is set to the new value
        and the source node is saved as self.shortest_source.
        :param source: A neighboring node
        :param distance: The accumulated distance of this node to the source node.
        """
        if distance < self.distance and source.is_neighbor(self):
            self.shortest_source = source
            self.distance = distance

    def get_distance_to(self, node):
        """
        The distance from this node to the given neighboring node.
        :param node: A node that must be a neighbor if this node.
        :return: The distance between this node and the other node if it is a neighbor, else infinity.
        """
        if node in self._neighbors:
            return self._neighbors[node]
        else:
            return float("inf")

    def __iter__(self):
        """
        The standard python __iter__ method to retrieve an iterator of this object.
        In this case, the iterator produces the nodes that form the path from
        the source node to this one.
        :return: an iterator of nodes.
        """
        if self.shortest_source is not None:
            yield from self.shortest_source.__iter__()
        yield self

    def __repr__(self):
        """
        The standard python __repr__ method. The return value does not conform to the standard,
        because the node can't be fully restored from the returned string including its neighbors.
        Usually, this should be returned from __str__ instead. However, to be able to print a list of nodes
        as a list of labels, __repr__ was used.
        :return: A string representation of this node (its label).
        """
        return self.label


class Graph:
    """
    A graph consisting of nodes and edges that connect the nodes.
    A graph can be directed or undirected. If it is undirected, the graph will interpret the
    edges in both directions, else only the target node of an edge will become a neighbor
    of the source node.
    """
    def __init__(self, nodes, edges, directed=False):
        """
        Create a new graph.
        :param nodes: List of dictionaries including a label, e.g. {"label": "node_0"}.
        :param edges: List of dictionaries specifying source, target and cost of an edge, e.g.:
        {"source": 0, "target": 1, "cost": 3.14}. Source and target must be indizes or names of nodes in the node list
        :param directed: Whether the graph is directed. If it is, an edge will only be constructed from
        source to target, else it will be used in both directions.
        """
        # The nodes of the graph in the order they were given.
        self.nodes = [Node(node["label"]) for node in nodes]
        # A map of node label to index. Is used to retreive nodes via label.
        self.node_indizes = {node.label: index for index, node in enumerate(self.nodes)}

        for edge in edges:
            source_node = self[edge["source"]]
            target_node = self[edge["target"]]
            cost = edge["cost"]
            source_node.add_neighbor(target_node, cost)
            if not directed:
                target_node.add_neighbor(source_node, cost)

    def shortest_path(self, source, target):
        """
        Find the shortest path from source to target through the graph.
        Implements the Dijkstra algorithm.
        :param source: The node where the path shall begin.
        :param target: The node where the path shall end.
        :return: A list of nodes that denotes the path, including source and target.
        """
        # Initialize source node with distance 0
        source.distance = 0
        # Run until the target was visited.
        while not target.visited:
            # Select the node that has the lowest accumulated distance and was not yet visited
            current_node = self.closest_unvisited_node()
            # Remember this node was visited
            current_node.visited = True
            # Iterate through all the node's unvisited neighbors and check if the path
            # to the neighbor through this node is shorter than the path that was found before.
            for node in current_node.get_unvisited_neighbors():
                distance = current_node.get_distance_to(node) + current_node.distance
                node.update_distance(current_node, distance)
        return [node for node in target]

    def __getitem__(self, item):
        """
        Allows to retreive a node via index or via label (graph[42] or graph["node_42"].
        :param item: An int index or a str label.
        :return: A node, if available.
        """
        if isinstance(item, int):
            return self.nodes[item]
        if isinstance(item, str):
            return self.nodes[self.node_indizes[item]]
        raise TypeError("Incompatible key type: " + type(item))

    def _unvisited_nodes(self):
        """
        All nodes that were not yet visited.
        :return: An iterator of nodes.
        """
        return filter(lambda node: not node.visited, self.nodes)

    def closest_unvisited_node(self):
        """
        The node that has the lowest accumulated distance to the source node and is not yet visited.
        May raise an exception if no nodes are left unvisited.
        :return: A Node.
        """
        return sorted(self._unvisited_nodes(), key=lambda node: node.distance)[0]