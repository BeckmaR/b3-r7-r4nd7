import unittest
import graph


class NodeTest(unittest.TestCase):
    def test_init(self):
        node = graph.Node("label")
        self.assertEqual(node.label, "label")

    def test_neighbor(self):
        node1 = graph.Node("1")
        node2 = graph.Node("2")
        node1.add_neighbor(node2, 5.3)
        self.assertIn(node2, node1._neighbors)
        self.assertTrue(node1.is_neighbor(node2))
        self.assertNotIn(node1, node2._neighbors)
        self.assertFalse(node2.is_neighbor(node1))
        self.assertEqual(node1.get_distance_to(node2), 5.3)
        self.assertEqual(node2.get_distance_to(node1), float("inf"))

    def test_update_distance(self):
        node1 = graph.Node("1")
        node2 = graph.Node("2")
        node3 = graph.Node("3")

        node1.add_neighbor(node2, 3)
        node2.update_distance(node1, 5)
        self.assertEqual(node2.distance, 5)
        node2.update_distance(node3, 4)
        self.assertEqual(node2.distance, 5)
        node3.add_neighbor(node2, 3)
        node2.update_distance(node3, 4)
        self.assertEqual(node2.distance, 4)

    def test_unvisited_neighbors(self):
        node1 = graph.Node("1")
        node2 = graph.Node("2")
        node3 = graph.Node("3")

        node1.add_neighbor(node2, 3)
        node1.add_neighbor(node3, 4)

        self.assertEqual(list(sorted(node1.get_unvisited_neighbors(), key=lambda node: node.label)), [node2, node3])

        node3.visited = True

        self.assertEqual(list(node1.get_unvisited_neighbors()), [node2])

    def test_distance_to(self):
        node1 = graph.Node("1")
        node2 = graph.Node("2")

        node1.add_neighbor(node2, 5)
        self.assertEqual(node1.get_distance_to(node2), 5)
        self.assertEqual(node2.get_distance_to(node1), float("inf"))

    def test_path_iter(self):
        node1 = graph.Node("1")
        node2 = graph.Node("2")
        node3 = graph.Node("3")

        node3.shortest_source = node2
        node2.shortest_source = node1

        self.assertEqual([node for node in node3], [node1, node2, node3])


class GraphTest(unittest.TestCase):
    def setUp(self):
        nodes = [
            {"label": "1"},
            {"label": "2"},
            {"label": "3"}
        ]
        edges = [
            {"source": 0, "target": 1, "cost": 2.3},
            {"source": 1, "target": 2, "cost": 3.14}
        ]
        self.graph = graph.Graph(nodes, edges)

    def test_init(self):
        self.assertEqual(len(self.graph.nodes), 3)
        self.assertTrue(self.graph[0].is_neighbor(self.graph[1]))
        self.assertTrue(self.graph[1].is_neighbor(self.graph[0]))
        self.assertTrue(self.graph[1].is_neighbor(self.graph[2]))
        self.assertTrue(self.graph[2].is_neighbor(self.graph[1]))
        self.assertEqual(self.graph[0].get_distance_to(self.graph[1]), 2.3)
        self.assertEqual(self.graph[1].get_distance_to(self.graph[0]), 2.3)

    def test_itemgetter(self):
        self.assertEqual(self.graph[0].label, "1")
        self.assertEqual(self.graph["2"].label, "2")
        self.assertEqual(self.graph[0], self.graph["1"])

    def test_closest_unvisited(self):
        self.graph[0].distance = 0
        self.assertEqual(self.graph.closest_unvisited_node(), self.graph[0])
        self.graph[0].visited = True
        self.graph[1].update_distance(self.graph[0], 2)
        self.assertEqual(self.graph.closest_unvisited_node(), self.graph[1])

    def test_shortest(self):
        path = self.graph.shortest_path(self.graph[0], self.graph[2])
        self.assertEqual(path, [self.graph[0], self.graph[1], self.graph[2]])
        self.assertAlmostEqual(self.graph[2].distance, 5.44)

    def test_shortest_2(self):
        self.graph[0].add_neighbor(self.graph[2], 4)
        path = self.graph.shortest_path(self.graph[0], self.graph[2])
        self.assertEqual(path, [self.graph[0], self.graph[2]])
        self.assertAlmostEqual(self.graph[2].distance, 4)

    def test_shortest_3(self):
        self.graph[0].add_neighbor(self.graph[2], 6)
        path = self.graph.shortest_path(self.graph[0], self.graph[2])
        self.assertEqual(path, [self.graph[0], self.graph[1], self.graph[2]])
        self.assertAlmostEqual(self.graph[2].distance, 5.44)

if __name__ == "__main__":
    unittest.main()