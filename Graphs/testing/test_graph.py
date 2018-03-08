'''
Created on Jan 27, 2018

:author: iko
'''
import pytest
from components import graph


class TestNode(object):

    @classmethod
    def setup_class(cls):
        cls.node0 = graph.Node(0)
        cls.node1 = graph.Node("My node")

    def test_create_node(self):
        assert self.node1.id != self.node0.id

        assert self.node0.data == 0
        assert self.node0.exit_degree == 0
        assert self.node0.enter_degree == 0
        assert self.node0.degree == 0
        assert set() == self.node0.exit_edges
        assert set() == self.node0.enter_edges
        assert set() == self.node0.adjacencies_edges

        assert self.node1.data == "My node"
        assert self.node1.exit_degree == 0
        assert self.node1.enter_degree == 0
        assert self.node1.degree == 0
        assert set() == self.node1.exit_edges
        assert set() == self.node1.enter_edges
        assert set() == self.node1.adjacencies_edges

    @classmethod
    def teardown_class(cls):
        cls.node0 = None
        cls.node1 = None


class TestEdge(object):

    @classmethod
    def setup_class(cls):
        cls.node0 = graph.Node(0)
        cls.node1 = graph.Node(1)
        cls.edge01 = graph.Edge(cls.node0, cls.node1)
        cls.edge10 = graph.Edge(cls.node1, cls.node0)

    def test_create_edge(self):
        assert self.edge01 is not self.edge10
        assert self.edge01.id != self.edge10.id

        assert self.node0 is self.edge01.exit_node
        assert self.node1 is self.edge01.enter_node
        assert self.node1 is self.edge10.exit_node
        assert self.node0 is self.edge10.enter_node

    @classmethod
    def teardown_class(cls):
        cls.node0 = None
        cls.node1 = None
        cls.edge0 = None
        cls.edge1 = None


class TestGraph(object):

    def setup_method(self):
        self.graph0 = graph.Graph()
        self.graph1 = graph.Graph([0, 1], [(0, 1), (1, 0)])

    def test_nodes_data(self):
        assert set() == self.graph0.nodes_data
        assert set([0, 1]) == self.graph1.nodes_data

    def test_edges_data(self):
        assert set() == self.graph0.edges_data
        assert set([(0, 1) == (1, 0)])

    def test_create_graph(self):
        graph1_nodes_data = self.graph1.nodes_data
        graph1_edges_data = self.graph1.edges_data

        assert self.graph0.id != self.graph1.id

        assert set() == self.graph0.nodes
        assert set() == self.graph0.edges

        assert set([0, 1]) == graph1_nodes_data
        assert set([(0, 1), (1, 0)]) == graph1_edges_data

    def test_get_node_by_obj(self):
        assert self.graph0.get_node_by_obj("No such node") is None

        assert self.graph1.get_node_by_obj(None) is None
        assert self.graph1.get_node_by_obj("No such node") is None
        assert isinstance(self.graph1.get_node_by_obj(0), graph.Node)
        assert self.graph1.get_node_by_obj(0).data == 0

        assert isinstance(self.graph1.get_node_by_obj(1), graph.Node)
        assert self.graph1.get_node_by_obj(1).data == 1

    def test_get_edge_by_objs(self):
        assert self.graph0.get_edge_by_objs("exit obj", "enter obj") is None

        assert self.graph1.get_edge_by_objs(None, None) is None
        assert self.graph1.get_edge_by_objs(0, 2) is None
        assert self.graph1.get_edge_by_objs(2, 0) is None
        assert self.graph1.get_edge_by_objs(0, 0) is None

        assert isinstance(self.graph1.get_edge_by_objs(0, 1), graph.Edge)
        assert self.graph1.get_edge_by_objs(0, 1).exit_node.data == 0
        assert self.graph1.get_edge_by_objs(0, 1).enter_node.data == 1

        assert isinstance(self.graph1.get_edge_by_objs(1, 0), graph.Edge)
        assert self.graph1.get_edge_by_objs(1, 0).exit_node.data == 1
        assert self.graph1.get_edge_by_objs(1, 0).enter_node.data == 0

    def test_add_node(self):
        node0 = self.graph0.add_node("My node")
        node1 = self.graph0.add_node(0)
        node2 = self.graph0.add_node(0)

        assert isinstance(node0, graph.Node)
        assert isinstance(node1, graph.Node)
        assert isinstance(node2, graph.Node)

        assert node1 is node2

        assert None not in self.graph0.nodes
        assert node0 in self.graph0.nodes
        assert node1 in self.graph0.nodes

        assert node0.data == "My node"
        assert node1.data == 0
        assert node0.exit_degree == 0
        assert node1.exit_degree == 0
        assert node0.enter_degree == 0
        assert node1.enter_degree == 0
        assert node0.degree == 0
        assert node1.degree == 0
        assert set() == node0.exit_edges
        assert set() == node1.exit_edges
        assert set() == node0.enter_edges
        assert set() == node1.enter_edges
        assert set() == node0.adjacencies_edges
        assert set() == node1.adjacencies_edges

        assert len(self.graph0.nodes) == 2

    def test_add_directed_edge(self):
        assert len(self.graph0.nodes) == 0

        edge0 = self.graph0.add_directed_edge(0, 1)
        edge1 = self.graph0.add_directed_edge(1, 0)
        edge2 = self.graph0.add_directed_edge(1, 0)

        assert isinstance(edge0, graph.Edge)
        assert isinstance(edge1, graph.Edge)
        assert isinstance(edge2, graph.Edge)

        assert edge1 is edge2
        assert len(self.graph0.nodes) == 2

        assert edge0.exit_node.data == 0
        assert edge0.enter_node.data == 1
        assert edge1.exit_node.data == 1
        assert edge1.enter_node.data == 0

        assert edge0 in edge0.exit_node.exit_edges
        assert edge1 in edge1.exit_node.exit_edges
        assert edge1 in edge0.exit_node.enter_edges
        assert edge0 in edge1.exit_node.enter_edges
        assert set([edge0, edge1]) == edge0.exit_node.adjacencies_edges
        assert set([edge0, edge1]) == edge1.exit_node.adjacencies_edges

        assert edge0.exit_node.exit_degree == 1
        assert edge1.exit_node.exit_degree == 1
        assert edge0.exit_node.enter_degree == 1
        assert edge1.exit_node.enter_degree == 1
        assert edge0.exit_node.degree == 2
        assert edge1.exit_node.degree == 2

    def test_add_nodes_from(self):
        nodes_bunch = self.graph0.add_nodes_from(range(10))

        assert len(self.graph0.nodes) == 10

        for node in nodes_bunch:
            assert  isinstance(node, graph.Node)

    def test_add_edges_from(self):
        edges_bunch = self.graph0.add_edges_from(zip(range(10), range(10, 20)))

        assert len(self.graph0.nodes) == 20
        assert len(self.graph0.edges) == 10

        for edge in edges_bunch:
            assert  isinstance(edge, graph.Edge)

    @pytest.mark.skip(reason="No way of currently testing this.")
    def test_remove_edge(self):
        pass

    @pytest.mark.skip(reason="No way of currently testing this.")
    def test_remove_edges_from(self):
        pass

    def test_del_node(self):
        node0 = self.graph0.add_node(0)
        node1 = self.graph0.add_node(1)
        assert node0.data == 0
        assert node1.data == 1
        assert len(self.graph0.nodes) == 2

        node1 = self.graph0.del_node(1)
        assert len(self.graph0.nodes) == 1
        assert self.graph0.nodes.pop().data == 0

    def test_del_edge(self):
        edge0 = self.graph0.add_directed_edge(0, 1)
        edge1 = self.graph0.add_directed_edge(1, 2)
        assert edge0.exit_node.data == 0
        assert edge0.enter_node.data == 1
        assert edge1.exit_node.data == 1
        assert edge1.enter_node.data == 2
        assert len(self.graph0.nodes) == 3
        assert len(self.graph0.edges) == 2

        edge1 = self.graph0.del_edge(1, 2)
        assert edge1.exit_node.data == 1
        assert edge1.enter_node.data == 2
        assert len(self.graph0.nodes) == 3
        assert len(self.graph0.edges) == 1

    def test_del_nodes_from(self):
        self.graph0.add_nodes_from(range(10))
        assert len(self.graph0.nodes) == 10

        self.graph0.del_nodes_from(range(4))
        assert len(self.graph0.nodes) == 6

        self.graph0.del_nodes_from(range(4))
        assert len(self.graph0.nodes) == 6

        self.graph0.del_nodes_from(range(5, 8))
        assert len(self.graph0.nodes) == 3

    def test_del_edges_from(self):
        self.graph0.add_edges_from(zip(range(10), range(10, 20)))
        assert len(self.graph0.nodes) == 20
        assert len(self.graph0.edges) == 10

        self.graph0.del_edges_from(zip(range(4), range(10, 14)))
        assert len(self.graph0.nodes) == 20
        assert len(self.graph0.edges) == 6

        self.graph0.del_edges_from(zip(range(4), range(10, 14)))
        assert len(self.graph0.nodes) == 20
        assert len(self.graph0.edges) == 6

        self.graph0.del_edges_from(zip(range(5, 8), range(15, 18)))
        assert len(self.graph0.nodes) == 20
        assert len(self.graph0.edges) == 3

    def teardown_method(self):
        # super(TestGraph, self).tearDown()(self):
        self.graph0 = None
        self.graph1 = None
