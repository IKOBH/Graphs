'''
Created on Jan 27, 2018

@author: iko
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
        
        assert 0 == self.node0.data
        assert 0 == self.node0.exit_degree
        assert 0 == self.node0.enter_degree
        assert 0 == self.node0.degree
        assert set() == self.node0.exit_edges
        assert set() == self.node0.enter_edges
        assert set() == self.node0.adjacencies_edges
        
        assert "My node" == self.node1.data
        assert 0 == self.node1.exit_degree
        assert 0 == self.node1.enter_degree
        assert 0 == self.node1.degree
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
        
class TestGraph():
    
    def setup_method(self):
        self.graph0 = graph.Graph()
        self.graph1 = graph.Graph([0,1],[(0,1),(1,0)])

    def test_nodes_data(self):
        assert set() ==  self.graph0.nodes_data
        assert set([0,1]) == self.graph1.nodes_data
    
    def test_edges_data(self):
        assert set() == self.graph0.edges_data
        assert set([(0,1) == (1,0)])
        
    def test_create_graph(self):
        graph1_nodes_data = self.graph1.nodes_data
        graph1_edges_data = self.graph1.edges_data
   
        assert self.graph0.id != self.graph1.id
        
        assert set() == self.graph0.nodes
        assert set() == self.graph0.edges
        
        assert set([0,1]) == graph1_nodes_data
        assert set([(0,1),(1,0)]) == graph1_edges_data
        
    def test_get_node_by_obj(self):
        assert self.graph0.get_node_by_obj("No such node") is None
        
        assert self.graph1.get_node_by_obj(None) is None
        assert self.graph1.get_node_by_obj("No such node") is None
        assert type(self.graph1.get_node_by_obj(0)) is graph.Node
        assert 0 == self.graph1.get_node_by_obj(0).data
        
        assert type(self.graph1.get_node_by_obj(1)) is graph.Node
        assert 1 == self.graph1.get_node_by_obj(1).data
    
    def test_get_edge_by_objs(self):
        assert self.graph0.get_edge_by_objs("exit obj","enter obj") is None
        
        assert self.graph1.get_edge_by_objs(None, None) is None
        assert self.graph1.get_edge_by_objs(0,2) is None
        assert self.graph1.get_edge_by_objs(2,0) is None
        assert self.graph1.get_edge_by_objs(0,0) is None
        
        assert type(self.graph1.get_edge_by_objs(0,1)) is graph.Edge
        assert 0 == self.graph1.get_edge_by_objs(0,1).exit_node.data
        assert 1 == self.graph1.get_edge_by_objs(0,1).enter_node.data
        
        assert type(self.graph1.get_edge_by_objs(1,0)) is graph.Edge
        assert 1 == self.graph1.get_edge_by_objs(1,0).exit_node.data
        assert 0 == self.graph1.get_edge_by_objs(1,0).enter_node.data    
            
    def test_add_node(self):
        node0 = self.graph0.add_node("My node")
        node1 = self.graph0.add_node(0)
        node2 = self.graph0.add_node(0)
        
        assert type(node0) is graph.Node
        assert type(node1) is graph.Node
        assert type(node2) is graph.Node
        
        assert node1 is node2
        
        assert None not in self.graph0.nodes
        assert node0 in self.graph0.nodes
        assert node1 in self.graph0.nodes
        
        assert "My node" == node0.data
        assert 0 == node1.data
        assert 0 == node0.exit_degree
        assert 0 == node1.exit_degree
        assert 0 == node0.enter_degree
        assert 0 == node1.enter_degree
        assert 0 == node0.degree
        assert 0 == node1.degree
        assert set() == node0.exit_edges
        assert set() == node1.exit_edges
        assert set() == node0.enter_edges
        assert set() == node1.enter_edges
        assert set() == node0.adjacencies_edges
        assert set() == node1.adjacencies_edges
        
        assert 2 == len(self.graph0.nodes)     
    
    def test_add_directed_edge(self):        
        assert 0 == len(self.graph0.nodes)
        
        edge0 = self.graph0.add_directed_edge(0,1)
        edge1 = self.graph0.add_directed_edge(1,0)
        edge2 = self.graph0.add_directed_edge(1,0)
        
        assert type(edge0) is graph.Edge
        assert type(edge1) is graph.Edge
        assert type(edge2) is graph.Edge
        
        assert edge1 is edge2
        assert 2 == len(self.graph0.nodes)
                
        assert 0 == edge0.exit_node.data        
        assert 1 == edge0.enter_node.data
        assert 1 == edge1.exit_node.data        
        assert 0 == edge1.enter_node.data
        
        assert edge0 in edge0.exit_node.exit_edges
        assert edge1 in edge1.exit_node.exit_edges
        assert edge1 in edge0.exit_node.enter_edges
        assert edge0 in edge1.exit_node.enter_edges
        assert set([edge0, edge1]) == edge0.exit_node.adjacencies_edges
        assert set([edge0, edge1]) == edge1.exit_node.adjacencies_edges
        
        assert 1 == edge0.exit_node.exit_degree
        assert 1 == edge1.exit_node.exit_degree
        assert 1 == edge0.exit_node.enter_degree
        assert 1 == edge1.exit_node.enter_degree
        assert 2 == edge0.exit_node.degree
        assert 2 == edge1.exit_node.degree
    
    def test_add_nodes_from(self):
        nodes_bunch = self.graph0.add_nodes_from(range(10))
        
        assert 10 == len(self.graph0.nodes)
        
        for node in nodes_bunch:
            assert  type(node) is graph.Node
    
    def test_add_edges_from(self):
        edges_bunch = self.graph0.add_edges_from(zip(range(10), range(10,20)))
            
        assert 20 == len(self.graph0.nodes)
        assert 10 == len(self.graph0.edges)
        
        for edge in edges_bunch:
            assert  type(edge) is graph.Edge
    
    @pytest.mark.skip(reason="No way of currently testing this.")
    def test_remove_edge(self):
        pass
    
    @pytest.mark.skip(reason="No way of currently testing this.")
    def test_remove_edges_from(self):
        pass
    
    def test_del_node(self):
        node0 = self.graph0.add_node(0)
        node1 = self.graph0.add_node(1)        
        assert 0 == node0.data
        assert 1 == node1.data
        assert 2 == len(self.graph0.nodes)
        
        node1 = self.graph0.del_node(1)
        assert 1 == len(self.graph0.nodes)
        assert 0 == self.graph0.nodes.pop().data
    
    def test_del_edge(self):
        edge0 = self.graph0.add_directed_edge(0, 1)
        edge0 = self.graph0.add_directed_edge(1, 2)        
        assert 3 == len(self.graph0.nodes)
        assert 2 == len(self.graph0.edges)
        
        edge0 = self.graph0.del_edge(1, 2)
        assert 3 == len(self.graph0.nodes)
        assert 1 == len(self.graph0.edges)
    
    def test_del_nodes_from(self):
        nodes_bunch = self.graph0.add_nodes_from(range(10))
        assert 10 == len(self.graph0.nodes)
        
        new_nodes_bunch = self.graph0.del_nodes_from(range(4))
        assert 6 == len(self.graph0.nodes)
        
        new_nodes_bunch = self.graph0.del_nodes_from(range(4))
        assert 6 == len(self.graph0.nodes)
        
        new_nodes_bunch = self.graph0.del_nodes_from(range(5,8))
        assert 3 == len(self.graph0.nodes)    
    
    def test_del_edges_from(self):
        edges_bunch = self.graph0.add_edges_from(zip(range(10), range(10,20)))
        assert 20 == len(self.graph0.nodes)
        assert 10 == len(self.graph0.edges)
        
        new_edges_bunch = self.graph0.del_edges_from(zip(range(4),range(10,14)))
        assert 20 == len(self.graph0.nodes)
        assert 6 == len(self.graph0.edges)
        
        new_edges_bunch = self.graph0.del_edges_from(zip(range(4),range(10,14)))
        assert 20 == len(self.graph0.nodes)
        assert 6 == len(self.graph0.edges)
        
        new_edges_bunch = self.graph0.del_edges_from(zip(range(5,8),range(15,18)))
        assert 20 == len(self.graph0.nodes)
        assert 3 == len(self.graph0.edges)

    def teardown_method(self):
        #super(TestGraph, self).tearDown()(self):
        self.graph0 = None
        self.graph1 = None

