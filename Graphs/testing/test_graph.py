'''
Created on Jan 27, 2018

:author: iko
'''
import pytest
from components import graph


class _Attr_object(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_set_attr(self):
        pass

    def test_set_attrs(self):
        pass

    def test_del_attr(self):
        pass

    def test_del_attrs(self):
        pass

    @classmethod
    def teardown_class(cls):
        pass


class TestNode(object):

    @classmethod
    def setup_class(cls):
        cls.node0 = graph._Node(0)
        cls.node1 = graph._Node("My node", color='Red', weight=1, friend=cls.node0)

    def test_create_node(self):
        assert self.node0 is not self.node1
        assert self.node1.id != self.node0.id

        assert self.node0.obj == 0
        assert self.node0.degree == 0
        assert self.node0.edges == set()
        assert self.node0.data == {'id': self.node0.id, 'obj': 0, 'edges': set()}

        assert self.node1.obj == "My node"
        assert self.node1.degree == 0
        assert self.node1.edges == set()
        assert self.node1.color == 'Red'
        assert self.node1.weight == 1
        assert self.node1.friend == self.node0

    @classmethod
    def teardown_class(cls):
        cls.node0 = None
        cls.node1 = None


class TestEdge(object):

    @classmethod
    def setup_class(cls):
        cls.node0 = graph._Node(0)
        cls.node1 = graph._Node(1)
        cls.node2 = graph._Node(2)
        cls.edge0 = graph._Edge((cls.node0,))
        cls.edge12 = graph._Edge((cls.node1, cls.node2), color='Blue', weight=2, friend=cls.edge0)
        cls.edge012 = graph._Edge((cls.node0, cls.node1, cls.node2), color='Green', weight=3)

    def test_create_edge(self):
        assert self.edge0 is not self.edge12 is not self.edge012
        assert self.edge0.id != self.edge12.id != self.edge012.id

        assert self.edge0.nodes == set([self.node0])
#        assert self.edge0.data == {'id': self.edge0.id, 'nodes': set([self.node0.obj])}

        assert self.edge12.nodes == set([self.node1, self.node2])
        assert self.edge12.color == 'Blue'
        assert self.edge12.weight == 2
        assert self.edge12.friend == self.edge0
#        assert self.edge12.data == {1, 2}

        assert self.edge012.nodes == set([self.node0, self.node1, self.node2])
        assert self.edge012.color == 'Green'
        assert self.edge012.weight == 3
#        assert self.edge012.data == {0, 1, 2}

    @classmethod
    def teardown_class(cls):
        cls.node0 = None
        cls.node1 = None
        cls.edge01 = None
        cls.edge12 = None


class TestGraph(object):

    def setup_method(self):
        self.graph0 = graph.Graph()
        self.graph1 = graph.Graph([0, 1, 2], [(0, 1), (1, 0)])
        self.graph2 = graph.Graph(None, [(0,), (0, 1, 2), (2, 3, 4, 'node')])

        self.n0_g1 = self.graph1.get_node_by_obj(0)
        self.n1_g1 = self.graph1.get_node_by_obj(1)
        self.n2_g1 = self.graph1.get_node_by_obj(2)

        self.n0_g2 = self.graph2.get_node_by_obj(0)
        self.n1_g2 = self.graph2.get_node_by_obj(1)
        self.n2_g2 = self.graph2.get_node_by_obj(2)
        self.n3_g2 = self.graph2.get_node_by_obj(3)
        self.n4_g2 = self.graph2.get_node_by_obj(4)
        self.node_g2 = self.graph2.get_node_by_obj('node')

    def test_create_graph(self):
        assert self.graph0.id is not self.graph1.id is not self.graph2.id
        assert self.graph0.id != self.graph1.id != self.graph2.id

        assert self.graph0.nodes == set()
        assert self.graph0.edges == set()
        assert len(self.graph0.nodes) == 0
        assert len(self.graph0.edges) == 0

        assert len(self.graph1.nodes) == 3
        assert len(self.graph1.edges) == 1

        assert len(self.graph2.nodes) == 6
        assert len(self.graph2.edges) == 3

    def test_nodes_data(self):
        assert self.graph0.nodes_data == set()
        assert self.graph1.nodes_data == ({'obj': 0, 'id': self.n0_g1.id, 'edges': self.n0_g1.edges},
                                           {'obj': 1, 'id': self.n1_g1.id, 'edges': self.n1_g1.edges},
                                            {'obj': 2, 'id': self.n2_g1.id, 'edges': self.n2_g1.edges})
        # assert self.graph2.nodes_data == {0, 1, 2, 3, 4, "node"}

    def test_edges_data(self):
        assert self.graph0.edges_data == set()
        # assert self.graph1.edges_data == {frozenset([0, 1])}
        # assert self.graph2.edges_data == {frozenset([0, ]), frozenset([0, 1, 2]), frozenset([2, 3, 4, "node"])}

    def test_data(self):
        pass
        # assert self.graph0.obj == {'nodes' : set(), 'edges' : set()}
        # assert self.graph1.obj == {'nodes' : {0, 1, 2}, 'edges' : {frozenset([0, 1])}}
        # assert self.graph2.obj == {'nodes' : {0, 1, 2, 3, 4, "node"}, 'edges' : {frozenset([0, ]), frozenset([0, 1, 2]), frozenset([2, 3, 4, "node"])}}

    def test_get_node_by_obj(self):
        assert self.graph0.get_node_by_obj(None) is None
        assert self.graph0.get_node_by_obj("No such node") is None

        assert self.graph1.get_node_by_obj(None) is None
        assert self.graph1.get_node_by_obj("No such node") is None
        assert isinstance(self.n0_g1, graph._Node)
        assert isinstance(self.n1_g1, graph._Node)
        assert self.n0_g1.obj == 0
        assert self.n1_g1.obj == 1

        assert self.graph2.get_node_by_obj(None) is None
        assert self.graph2.get_node_by_obj("No such node") is None
        assert isinstance(self.n0_g2, graph._Node)
        assert isinstance(self.n1_g2, graph._Node)
        assert isinstance(self.n2_g2, graph._Node)
        assert isinstance(self.n3_g2, graph._Node)
        assert isinstance(self.n4_g2, graph._Node)
        assert isinstance(self.node_g2, graph._Node)
        assert self.n0_g2.obj == 0
        assert self.n1_g2.obj == 1
        assert self.n2_g2.obj == 2
        assert self.n3_g2.obj == 3
        assert self.n4_g2.obj == 4
        assert self.node_g2.obj == "node"

    def test_get_edge_by_objs(self):
        assert self.graph0.get_edge_by_objs() is None
        assert self.graph0.get_edge_by_objs(None) is None
        assert self.graph0.get_edge_by_objs("No such node 0", "No such node 1") is None

        assert self.graph1.get_edge_by_objs() is None
        assert self.graph1.get_edge_by_objs(None, None) is None
        assert self.graph1.get_edge_by_objs("No such node 0", "No such node 1") is None
        assert self.graph1.get_edge_by_objs(0, "No such node") is None
        assert self.graph1.get_edge_by_objs(0, 2) is None
        assert self.graph1.get_edge_by_objs(0, 0) is None
        assert isinstance(self.graph1.get_edge_by_objs(0, 1), graph._Edge)
        assert self.graph1.get_edge_by_objs(0, 1) is self.graph1.get_edge_by_objs(1, 0)

        assert self.graph2.get_edge_by_objs() is None
        assert self.graph2.get_edge_by_objs(None, None) is None
        assert self.graph2.get_edge_by_objs("No such node 0", "No such node 1") is None
        assert self.graph2.get_edge_by_objs(0, "No such node") is None
        assert self.graph2.get_edge_by_objs(0, 1) is None
        assert self.graph2.get_edge_by_objs(1, 1) is None
        assert self.graph2.get_edge_by_objs(0, 1, 2, "No such node") is None
        assert isinstance(self.graph2.get_edge_by_objs(0), graph._Edge)
        assert isinstance(self.graph2.get_edge_by_objs(0, 0), graph._Edge)
        assert isinstance(self.graph2.get_edge_by_objs(0, 1, 2), graph._Edge)
        assert isinstance(self.graph2.get_edge_by_objs(0, 1, 2, 0, 1, 2), graph._Edge)
        assert isinstance(self.graph2.get_edge_by_objs(2, 3, 4, "node"), graph._Edge)
        assert self.graph2.get_edge_by_objs(0) is self.graph2.get_edge_by_objs(0, 0)
        assert self.graph2.get_edge_by_objs(0, 1 , 2) is self.graph2.get_edge_by_objs(2, 1, 0)
        assert self.graph2.get_edge_by_objs(2, 3, 4, "node") is self.graph2.get_edge_by_objs(3, 4, "node", 2)

    def test_add_node(self):
        assert len(self.graph0.nodes) == 0

        node0 = self.graph0.add_node(0)
        node00 = self.graph0.add_node(0)
        node1 = self.graph0.add_node('1', color='Black', type=graph._Node)

        assert len(self.graph0.nodes) == 2

        assert node0 is node00
        assert isinstance(node0, graph._Node)
        assert isinstance(node1, graph._Node)

        assert None not in self.graph0.nodes
        assert node0 in self.graph0.nodes
        assert node1 in self.graph0.nodes

        assert node0.obj == 0
        assert node0.degree == 0
        assert node0.edges == set()

        assert node1.obj == '1'
        assert node1.degree == 0
        assert node1.edges == set()
        assert node1.color == 'Black'
        assert node1.type == graph._Node

        node0_modified = self.graph0.add_node(0, name='iko')
        node1_modified = self.graph0.add_node('1', color='White')

        assert node0 is node0_modified
        assert node0.obj == 0
        assert node0.degree == 0
        assert node0.edges == set()
        assert node0.name == 'iko'

        assert node1 is node1_modified
        assert node1.obj == '1'
        assert node1.degree == 0
        assert node1.edges == set()
        assert node1.color == 'White'
        assert node1.type == graph._Node

    def test_add_edge(self):
        assert len(self.graph0.nodes) == 0
        assert len(self.graph0.edges) == 0

        edge01 = self.graph0.add_edge(0, 1)
        edge10 = self.graph0.add_edge(1, 0)
        edge10_replica = self.graph0.add_edge(1, 0)
        edge012 = self.graph0.add_edge(0, 1, 2)
        edge_loop = self.graph0.add_edge('My edge', weight=1, type='loop')

        assert len(self.graph0.nodes) == 4
        assert len(self.graph0.edges) == 3

        assert edge01 is edge10 is edge10_replica
        assert isinstance(edge01, graph._Edge)
        assert isinstance(edge012, graph._Edge)
        assert isinstance(edge_loop, graph._Edge)

        assert len(edge01.nodes) == 2
        assert len(edge012.nodes) == 3
        assert len(edge_loop.nodes) == 1

        assert edge_loop.weight == 1
        assert edge_loop.type == 'loop'

        assert self.graph0.get_node_by_obj(0).edges == {edge01, edge012}
        assert self.graph0.get_node_by_obj(1).edges == {edge01, edge012}
        assert self.graph0.get_node_by_obj(2).edges == {edge012}
        assert self.graph0.get_node_by_obj('My edge').edges == {edge_loop}

        assert self.graph0.get_node_by_obj(0).degree == 2
        assert self.graph0.get_node_by_obj(1).degree == 2
        assert self.graph0.get_node_by_obj(2).degree == 1
        assert self.graph0.get_node_by_obj('My edge').degree == 2

        edge012_modified = self.graph0.add_edge(0, 1, 2, type='hyper')
        edge_loop_modified = self.graph0.add_edge('My edge', weight=2)

        assert len(self.graph0.nodes) == 4
        assert len(self.graph0.edges) == 3

        assert edge_loop is edge_loop_modified
        assert edge_loop.weight == 2
        assert edge_loop.type == 'loop'

        assert edge012 is edge012_modified
        assert edge012.type == 'hyper'

    def test_add_nodes_from(self):
        nodes = self.graph0.add_nodes_from(range(100), name='default')

        assert self.graph0.nodes == nodes
        assert len(self.graph0.nodes) == 100

        for node in self.graph0.nodes:
            assert isinstance(node, graph._Node)
            assert node.edges == set()
            assert node.degree == 0
            assert node.name == 'default'

    def test_add_edges_from(self):
        edges0 = self.graph0.add_edges_from(zip(range(100), range(100, 200)), weight=0)

        assert self.graph0.edges == edges0
        assert len(self.graph0.nodes) == 200
        assert len(self.graph0.edges) == 100

        for edge in self.graph0.edges:
            assert isinstance(edge, graph._Edge)
            assert len(edge.nodes) == 2
            assert edge.weight == 0

        edges1 = self.graph0.add_edges_from(zip(range(10), range(10, 20), range(20, 30)), type='hyper')

        assert self.graph0.edges == edges0.union(edges1)
        assert len(self.graph0.nodes) == 200
        assert len(self.graph0.edges) == 110

        for edge in edges1:
            assert isinstance(edge, graph._Edge)
            assert len(edge.nodes) == 3
            assert edge.type == 'hyper'

    @pytest.mark.skip(reason="No way of currently testing this.")
    def test_remove_edge(self):
        pass

    @pytest.mark.skip(reason="No way of currently testing this.")
    def test_remove_edges_from(self):
        pass

    def test_del_node(self):
        node0 = self.graph0.add_node(0)
        node1 = self.graph0.add_node(1)
        assert node0.obj == 0
        assert node1.obj == 1
        assert len(self.graph0.nodes) == 2

        node1 = self.graph0.del_node(1)
        assert len(self.graph0.nodes) == 1
        assert self.graph0.nodes.pop().obj == 0

    def test_del_edge(self):
        edge0 = self.graph0.add_edge(0)
        edge1 = self.graph0.add_edge(0, 1)
        edge2 = self.graph0.add_edge(2, 3, 4)
        assert len(self.graph0.nodes) == 5
        assert len(self.graph0.edges) == 3

        not_edge = self.graph0.del_edge(1, 2)
        assert not_edge is None
        assert len(self.graph0.edges) == 3

        deleted_edge = self.graph0.del_edge(0)
        assert deleted_edge is edge0
        assert len(self.graph0.edges) == 2

        deleted_edge = self.graph0.del_edge(0, 1)
        assert deleted_edge is edge1
        assert len(self.graph0.edges) == 1

        deleted_edge = self.graph0.del_edge(2, 3, 4)
        assert deleted_edge is edge2
        assert len(self.graph0.edges) == 0

        assert len(self.graph0.nodes) == 5

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
        self.graph0.add_edges_from(zip(range(10), range(10, 20), range(20, 30)))
        assert len(self.graph0.nodes) == 30
        assert len(self.graph0.edges) == 10

        self.graph0.del_edges_from(zip(range(4), range(10, 14), range(20, 24)))
        assert len(self.graph0.nodes) == 30
        assert len(self.graph0.edges) == 6

        self.graph0.del_edges_from(zip(range(4), range(10, 14), range(20, 24)))
        assert len(self.graph0.nodes) == 30
        assert len(self.graph0.edges) == 6

        self.graph0.del_edges_from(zip(range(5, 8), range(15, 18), range(25, 28)))
        assert len(self.graph0.nodes) == 30
        assert len(self.graph0.edges) == 3

    def teardown_method(self):
        # super(TestGraph, self).tearDown()(self):
        self.graph0 = None
        self.graph1 = None
