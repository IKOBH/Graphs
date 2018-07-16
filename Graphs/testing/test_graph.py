"""
Created on Jan 27, 2018

:author: iko
"""
import pytest
from components import graph


class _AttrObject(object):

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
        # TODO: Check node creation without name attribute. Should raise an exception.
        cls.node0 = graph._Node(name=0)
        cls.node1 = graph._Node(name='My node', color='Red', weight=1, friend=cls.node0)
        # cls.node2 = graph._Node(name=[1,2,3]) BAD FLOW ON PURPUSE.

    def test_create_node(self):
        assert self.node0 is not self.node1
        assert self.node1.id != self.node0.id

        assert self.node0.name == 0
        assert self.node0.degree == 0
        assert self.node0.edges == set()
        assert self.node0.get_attrs == {'id': self.node0.id,
                                        '_name': 0,
                                        'edges': set()}

        assert self.node1.name == 'My node'
        assert self.node1.degree == 0
        assert self.node1.edges == set()
        assert self.node1.color == 'Red'
        assert self.node1.weight == 1
        assert self.node1.friend == self.node0
        assert self.node1.get_attrs == {'id': self.node1.id,
                                        '_name': 'My node',
                                        'edges': set(),
                                        'color': 'Red',
                                        'weight': 1,
                                        'friend': self.node0}

    def test_set_attr(self):
        self.node0.set_attr('name', 1)
        assert self.node0.name == 1

        # self.node0.set_attr('name', [1, 2])

    @classmethod
    def teardown_class(cls):
        cls.node0 = None
        cls.node1 = None


class TestEdge(object):

    @classmethod
    def setup_class(cls):
        # cls.invalid_edge = graph._Edge({}) TODO: check error is raised
        cls.edge0 = graph._Edge({0})
        cls.edge12 = graph._Edge({1, 2}, color='Blue', weight=2, friend=cls.edge0)
        cls.edge012 = graph._Edge({0, 1, 2}, color='Green', weight=3)

    def test_create_edge(self):
        assert self.edge0 is not (self.edge12 or self.edge012)
        assert self.edge0.id != self.edge12.id != self.edge012.id

        assert len(self.edge0.nodes) == 1
        assert self.edge0.nodes_names == {0}
        # TODO: Does it check anything?
        assert self.edge0.get_attrs == {'id': self.edge0.id, '_nodes': self.edge0.nodes,
                                        '_nodes_names': self.edge0.nodes_names}

        assert len(self.edge12.nodes) == 2
        assert self.edge12.nodes_names == {1, 2}
        assert self.edge12.color == 'Blue'
        assert self.edge12.weight == 2
        assert self.edge12.friend == self.edge0
        # TODO: Does it check anything?
        assert self.edge12.get_attrs == {'id': self.edge12.id,
                                         '_nodes': self.edge12.nodes,
                                         '_nodes_names': self.edge12.nodes_names,
                                         'color': 'Blue',
                                         'weight': 2,
                                         'friend': self.edge0}

        # assert self.edge012.nodes == ?
        assert self.edge012.nodes_names == {0, 1, 2}
        assert self.edge012.color == 'Green'
        assert self.edge012.weight == 3
        # TODO: Does it check anything?
        assert self.edge012.get_attrs == {'id': self.edge012.id,
                                          '_nodes': self.edge012.nodes,
                                          '_nodes_names': self.edge012.nodes_names,
                                          'color': 'Green',
                                          'weight': 3}

    def test_set_attr(self):
        pass

    @classmethod
    def teardown_class(cls):
        cls.node0 = None

        cls.node1 = None
        cls.edge01 = None
        cls.edge12 = None


class TestGraph(object):

    def setup_method(self):
        self.graph0 = graph.Graph()
        self.graph1 = graph.Graph({0, 1, 2}, {(0, 1), (1, 0)})
        self.graph2 = graph.Graph(None, {(0,), (0, 1, 2), (2, 3, 4, 'node')}, nickname='iko')
        self.graph3 = graph.Graph(None, {(0, 1), (2, 3)}, {'color': 'white'}, {'weight': 2}, nickname='iko3')

        self.n0_g1 = self.graph1.get_node(0)
        self.n1_g1 = self.graph1.get_node(1)
        self.n2_g1 = self.graph1.get_node(2)
        self.e2_g1 = self.graph1.get_edge(0, 1)

        self.n0_g2 = self.graph2.get_node(0)
        self.n1_g2 = self.graph2.get_node(1)
        self.n2_g2 = self.graph2.get_node(2)
        self.n3_g2 = self.graph2.get_node(3)
        self.n4_g2 = self.graph2.get_node(4)
        self.node_g2 = self.graph2.get_node('node')
        self.e1_g2 = self.graph2.get_edge(0)
        self.e3_g2 = self.graph2.get_edge(0, 1, 2)
        self.e4_g2 = self.graph2.get_edge(2, 3, 4, 'node')

        self.n0_g3 = self.graph3.get_node(0)
        self.n1_g3 = self.graph3.get_node(1)
        self.n2_g3 = self.graph3.get_node(2)
        self.n3_g3 = self.graph3.get_node(3)
        self.e01_g3 = self.graph3.get_edge(0, 1)
        self.e23_g3 = self.graph3.get_edge(2, 3)

    def test_create_graph(self):
        assert self.graph0.id is not (self.graph1.id or self.graph2.id or self.graph3.id)
        assert self.graph1.id is not (self.graph2.id or self.graph3.id)
        assert self.graph2.id is not self.graph3.id
        assert self.graph0.id != self.graph1.id != self.graph2.id != self.graph3.id

        assert self.graph0.nodes == set()
        assert self.graph0.edges == set()
        assert len(self.graph0.nodes) == 0
        assert len(self.graph0.edges) == 0

        assert self.graph1.nodes == {self.n0_g1, self.n1_g1, self.n2_g1}
        assert self.graph1.edges == {self.e2_g1}
        assert len(self.graph1.nodes) == 3
        assert len(self.graph1.edges) == 1

        assert self.graph2.nodes == {self.n0_g2, self.n1_g2, self.n2_g2, self.n3_g2, self.n4_g2, self.node_g2}
        assert self.graph2.edges == {self.e1_g2, self.e3_g2, self.e4_g2}
        assert len(self.graph2.nodes) == 6
        assert len(self.graph2.edges) == 3
        assert self.graph2.nickname == 'iko'

        assert self.graph3.nodes == {self.n0_g3, self.n1_g3, self.n2_g3, self.n3_g3}
        assert self.graph3.edges == {self.e01_g3, self.e23_g3}
        assert len(self.graph3.nodes) == 4
        assert len(self.graph3.edges) == 2
        assert self.graph3.nickname == 'iko3'

        assert self.n0_g1.degree == 1
        assert self.n1_g1.degree == 1
        assert self.n0_g2.degree == 3  # Self loop os counted twice.
        assert self.n1_g2.degree == 1
        assert self.n2_g2.degree == 2
        assert self.n3_g2.degree == 1
        assert self.n4_g2.degree == 1

    def test_nodes_data(self):
        assert self.graph0.nodes_data.keys() == set()
        assert self.graph0.nodes_data == {}

        assert self.graph1.nodes_data.keys() == {0, 1, 2}
        assert self.graph1.nodes_data == {0: {'_name': 0, 'id': self.n0_g1.id, 'edges': self.n0_g1.edges},
                                          1: {'_name': 1, 'id': self.n1_g1.id, 'edges': self.n1_g1.edges},
                                          2: {'_name': 2, 'id': self.n2_g1.id, 'edges': self.n2_g1.edges}}

        assert self.graph2.nodes_data.keys() == {0, 1, 2, 3, 4, 'node'}
        assert self.graph2.nodes_data == {0: {'_name': 0, 'id': self.n0_g2.id, 'edges': self.n0_g2.edges},
                                          1: {'_name': 1, 'id': self.n1_g2.id, 'edges': self.n1_g2.edges},
                                          2: {'_name': 2, 'id': self.n2_g2.id, 'edges': self.n2_g2.edges},
                                          3: {'_name': 3, 'id': self.n3_g2.id, 'edges': self.n3_g2.edges},
                                          4: {'_name': 4, 'id': self.n4_g2.id, 'edges': self.n4_g2.edges},
                                          'node': {'_name': 'node', 'id': self.node_g2.id, 'edges': self.node_g2.edges}}

        assert self.graph3.nodes_data.keys() == {0, 1, 2, 3}
        assert self.graph3.nodes_data == {0: {'_name': 0, 'id': self.n0_g3.id, 'edges': self.n0_g3.edges,
                                              'color': 'white'},
                                          1: {'_name': 1, 'id': self.n1_g3.id, 'edges': self.n1_g3.edges,
                                              'color': 'white'},
                                          2: {'_name': 2, 'id': self.n2_g3.id, 'edges': self.n2_g3.edges,
                                              'color': 'white'},
                                          3: {'_name': 3, 'id': self.n3_g3.id, 'edges': self.n3_g3.edges,
                                              'color': 'white'}}

    @pytest.mark.skip
    def test_edges_data(self):
        assert self.graph0.edges_data.keys() == set()
        assert self.graph0.edges_data == {}

        assert self.graph1.edges_data.keys() == {frozenset({0, 1})}
        assert self.graph1.edges_data == {frozenset({0, 1}): {'id': self.e2_g1.id, 'nodes': self.e2_g1.nodes}}

        assert self.graph2.edges_data.keys() == {frozenset({0}), frozenset({0, 1, 2}), frozenset({2, 3, 4, "node"})}
        assert self.graph2.edges_data == {frozenset({0}): {'id': self.e1_g2.id, 'nodes': self.e1_g2.nodes},
                                          frozenset({0, 1, 2}): {'id': self.e3_g2.id, 'nodes': self.e3_g2.nodes},
                                          frozenset({2, 3, 4, "node"}): {'id': self.e4_g2.id, 'nodes': self.e4_g2.nodes}}

        assert self.graph3.edges_data.keys() == {frozenset({0, 1}), frozenset({2, 3})}
        assert self.graph3.edges_data == {frozenset({0, 1}): {'id': self.e01_g3.id, 'nodes': self.e01_g3.nodes,
                                                              'weight': 2},
                                          frozenset({2, 3}): {'id': self.e23_g3.id, 'nodes': self.e23_g3.nodes,
                                                              'weight': 2}}

    def test_data(self):
        assert self.graph0.get_attrs == {'nodes': {}, 'edges': {}}
        assert self.graph1.get_attrs == {'nodes': self.graph1.nodes_data, 'edges': self.graph1.edges_data}
        assert self.graph2.get_attrs == {'nodes': self.graph2.nodes_data, 'edges': self.graph2.edges_data}

    def test_get_node_by_name(self):
        assert self.graph0.get_node(None) is None
        assert self.graph0.get_node("No such node") is None

        assert self.graph1.get_node(None) is None
        assert self.graph1.get_node("No such node") is None
        assert isinstance(self.n0_g1, graph._Node)
        assert isinstance(self.n1_g1, graph._Node)
        assert self.n0_g1.name == 0
        assert self.n1_g1.name == 1

        assert self.graph2.get_node(None) is None
        assert self.graph2.get_node("No such node") is None
        assert isinstance(self.n0_g2, graph._Node)
        assert isinstance(self.n1_g2, graph._Node)
        assert isinstance(self.n2_g2, graph._Node)
        assert isinstance(self.n3_g2, graph._Node)
        assert isinstance(self.n4_g2, graph._Node)
        assert isinstance(self.node_g2, graph._Node)
        assert self.n0_g2.name == 0
        assert self.n1_g2.name == 1
        assert self.n2_g2.name == 2
        assert self.n3_g2.name == 3
        assert self.n4_g2.name == 4
        assert self.node_g2.name == "node"

    def test_get_edge_by_name(self):
        assert self.graph0.get_edge() is None
        assert self.graph0.get_edge(None) is None
        assert self.graph0.get_edge("No such node 0", "No such node 1") is None

        assert self.graph1.get_edge() is None
        assert self.graph1.get_edge(None, None) is None
        assert self.graph1.get_edge("No such node 0", "No such node 1") is None
        assert self.graph1.get_edge(0, "No such node") is None
        assert self.graph1.get_edge(0, 2) is None
        assert self.graph1.get_edge(0, 0) is None
        assert isinstance(self.graph1.get_edge(0, 1), graph._Edge)
        assert self.graph1.get_edge(0, 1) is self.graph1.get_edge(1, 0)

        assert self.graph2.get_edge() is None
        assert self.graph2.get_edge(None, None) is None
        assert self.graph2.get_edge("No such node 0", "No such node 1") is None
        assert self.graph2.get_edge(0, "No such node") is None
        assert self.graph2.get_edge(0, 1) is None
        assert self.graph2.get_edge(1, 1) is None
        assert self.graph2.get_edge(0, 1, 2, "No such node") is None
        assert isinstance(self.graph2.get_edge(0), graph._Edge)
        assert isinstance(self.graph2.get_edge(0, 0), graph._Edge)
        assert isinstance(self.graph2.get_edge(0, 1, 2), graph._Edge)
        assert isinstance(self.graph2.get_edge(0, 1, 2, 0, 1, 2), graph._Edge)
        assert isinstance(self.graph2.get_edge(2, 3, 4, "node"), graph._Edge)
        assert self.graph2.get_edge(0) is self.graph2.get_edge(0, 0)
        assert self.graph2.get_edge(0, 1, 2) is self.graph2.get_edge(2, 1, 0)
        assert self.graph2.get_edge(2, 3, 4, "node") is self.graph2.get_edge(3, 4, "node", 2)

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

        assert node0.name == 0
        assert node0.degree == 0
        assert node0.edges == set()

        assert node1.name == '1'
        assert node1.degree == 0
        assert node1.edges == set()
        assert node1.color == 'Black'
        assert node1.type == graph._Node

        node0_modified = self.graph0.add_node(0, nickname='iko')
        node1_modified = self.graph0.add_node('1', color='White')

        assert node0 is node0_modified
        assert node0.name == 0
        assert node0.degree == 0
        assert node0.edges == set()
        assert node0.nickname == 'iko'

        assert node1 is node1_modified
        assert node1.name == '1'
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

        assert self.graph0.get_node(0).edges == {edge01, edge012}
        assert self.graph0.get_node(1).edges == {edge01, edge012}
        assert self.graph0.get_node(2).edges == {edge012}
        assert self.graph0.get_node('My edge').edges == {edge_loop}

        assert self.graph0.get_node(0).degree == 2
        assert self.graph0.get_node(1).degree == 2
        assert self.graph0.get_node(2).degree == 1
        assert self.graph0.get_node('My edge').degree == 2

        edge012_modified = self.graph0.add_edge(0, 1, 2, type='hyper')
        edge_loop_modified = self.graph0.add_edge('My edge', weight=2)

        assert len(self.graph0.nodes) == 4
        assert len(self.graph0.edges) == 3

        assert edge_loop is edge_loop_modified
        assert edge_loop.weight == 2
        assert edge_loop.type == 'loop'

        assert edge012 is edge012_modified
        assert edge012.type == 'hyper'

    def test_add_edge_with_nodes_attrs(self):
        edge_with_nodes_attrs = self.graph0.add_edge(0, 1, nodes_attributes={'color':'white'})
        self.n0_g0 = self.graph0.get_node(0)
        self.n1_g0 = self.graph0.get_node(1)

        assert len(edge_with_nodes_attrs.nodes) == 2

        for node in edge_with_nodes_attrs.nodes:
            assert node.color =='white'

        assert self.n0_g0.color == 'white'

    @pytest.mark.skip
    def test_add_directed_edge(self):
        edge_directed = self.graph0.add_edge(0, 1, 2, 3, 4, direction=(0, 1, 2))
        self.n0_g0 = self.graph0.get_node(0)
        self.n1_g0 = self.graph0.get_node(1)
        self.n2_g0 = self.graph0.get_node(2)
        self.n3_g0 = self.graph0.get_node(3)
        self.n4_g0 = self.graph0.get_node(4)

        assert hasattr(edge_directed, 'directed')
        assert hasattr(edge_directed, 'exit_nodes')
        assert hasattr(edge_directed, 'enter_nodes')
        assert edge_directed.directed is True
        assert edge_directed.exit_nodes == {self.n0_g0, self.n1_g0, self.n2_g0}
        assert edge_directed.enter_nodes == {self.n3_g0, self.n4_g0}
        assert edge_directed.exit_nodes.union(edge_directed.enter_nodes) == edge_directed.nodes

        for node in edge_directed.exit_nodes:
            assert hasattr(node, 'exit_edges')
            assert edge_directed in node.exit_edges
#            assert node.exit_degree == 1
#            assert node.enter_degree == 0

        for node in edge_directed.enter_nodes:
            assert hasattr(node, 'enter_edges')
            assert edge_directed in node.enter_edges
#            assert node.exit_degree == 0
#            assert node.enter_degree == 1

    def test_directed_graph(self):
        self.test_add_directed_graph = graph.Graph({1, 2, 3, 4}, {(1, 2, 3), (2, 3, 4)},)
        # TODO: add directed graph support to graph constructor.

    def test_add_nodes_from(self):
        nodes = self.graph0.add_nodes(range(100), type='default')

        assert self.graph0.nodes == nodes
        assert len(self.graph0.nodes) == 100

        for node in self.graph0.nodes:
            assert isinstance(node, graph._Node)
            assert node.edges == set()
            assert node.degree == 0
            assert node.type == 'default'

    def test_add_edges_from(self):
        edges0 = self.graph0.add_edges(zip(range(100), range(100, 200)), weight=0)

        assert self.graph0.edges == edges0
        assert len(self.graph0.nodes) == 200
        assert len(self.graph0.edges) == 100

        for edge in self.graph0.edges:
            assert isinstance(edge, graph._Edge)
            assert len(edge.nodes) == 2
            assert edge.weight == 0

        edges1 = self.graph0.add_edges(zip(range(10), range(10, 20), range(20, 30)), type='hyper')

        assert self.graph0.edges == edges0.union(edges1)
        assert len(self.graph0.nodes) == 200
        assert len(self.graph0.edges) == 110

        for edge in edges1:
            assert isinstance(edge, graph._Edge)
            assert len(edge.nodes) == 3
            assert edge.type == 'hyper'

    def test_remove_edge(self):
        self.graph1._remove_edge(self.e2_g1)

        assert len(self.graph1.edges) == 0
        assert self.graph1._remove_edge(None) is None

    def test_remove_edges(self):
        pass

    def test_del_node(self):
        node0 = self.graph0.add_node(0)
        node1 = self.graph0.add_node(1)
        assert node0.name == 0
        assert node1.name == 1
        assert len(self.graph0.nodes) == 2

        node1 = self.graph0.del_node(1)
        assert len(self.graph0.nodes) == 1
        assert self.graph0.nodes.pop().name == 0

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
        self.graph0.add_nodes(range(10))
        assert len(self.graph0.nodes) == 10

        self.graph0.del_nodes(range(4))
        assert len(self.graph0.nodes) == 6

        self.graph0.del_nodes(range(4))
        assert len(self.graph0.nodes) == 6

        self.graph0.del_nodes(range(5, 8))
        assert len(self.graph0.nodes) == 3

    def test_del_edges_from(self):
        self.graph0.add_edges(zip(range(10), range(10, 20), range(20, 30)))
        assert len(self.graph0.nodes) == 30
        assert len(self.graph0.edges) == 10

        self.graph0.del_edges(zip(range(4), range(10, 14), range(20, 24)))
        assert len(self.graph0.nodes) == 30
        assert len(self.graph0.edges) == 6

        self.graph0.del_edges(zip(range(4), range(10, 14), range(20, 24)))
        assert len(self.graph0.nodes) == 30
        assert len(self.graph0.edges) == 6

        self.graph0.del_edges(zip(range(5, 8), range(15, 18), range(25, 28)))
        assert len(self.graph0.nodes) == 30
        assert len(self.graph0.edges) == 3

    def teardown_method(self):
        # super(TestGraph, self).tearDown()(self):
        self.graph0 = None
        self.graph1 = None
