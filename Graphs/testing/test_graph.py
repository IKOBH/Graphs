'''
Created on Jan 27, 2018

@author: iko
'''
import unittest
from components import graph

class TestGraph(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        #super(TestGraph, cls).setUpClass()(self):
        cls.node0 = graph.Node()
        cls.node1 = graph.Node("My node")
        cls.edge01 = graph.Edge(cls.node0,cls.node1)
        cls.edge10 = graph.Edge(cls.node1,cls.node0)
        cls.graph0 = graph.Graph()
        cls.graph1 = graph.Graph([cls.node0,cls.node1],[cls.edge01,cls.edge10])
                
    def test1_create_node(self):
        self.assertNotEqual(self.node1.id, self.node0.id, "Error: Two nodes has the same id.")
        
        self.assertEqual(None, self.node0.data, "Error: Node's data isn't None.")
        self.assertEqual(1, self.node0.exit_degree, "Error: Node's exit degree isn't zero.")
        self.assertEqual(1, self.node0.enter_degree, "Error: Node's enter degree isn't zero.")
        self.assertEqual(2, self.node0.full_degree, "Error: Node's full degree isn't zero.")
        
        self.assertEqual("My node", self.node1.data, "Error: Node's data isn't \"My node\".")
        self.assertEqual(1, self.node1.exit_degree, "Error: Node's exit degree isn't zero.")
        self.assertEqual(1, self.node1.enter_degree, "Error: Node's enter degree isn't zero.")
        self.assertEqual(2, self.node1.full_degree, "Error: Node's full degree isn't zero.")

    def test2_create_edge(self):
        self.assertNotEqual(self.edge01.id, self.edge10.id, "Error: Two edges has the same id.")
        
        self.assertIs(self.node0, self.edge01.exit_node, "Error: Edge's exit node is incorrect.")
        self.assertIs(self.node1, self.edge01.enter_node, "Error: Edge's enter node is incorrect.")
        
        self.assertIs(self.node1, self.edge10.exit_node, "Error: Edge's exit node is incorrect.")
        self.assertIs(self.node0, self.edge10.enter_node, "Error: Edge's enter node is incorrect.")
        
    def test3_create_graph(self):
        self.assertNotEqual(self.graph0.id, self.graph1.id, "Error: Two graphs has the same id.")
        
        self.assertSetEqual(set(), self.graph0.nodes, "Error: Couldn't create a simple graph.")
        self.assertSetEqual(set(), self.graph0.edges, "Error: Couldn't create a simple graph.")
        
        self.assertSetEqual(set([self.node0,self.node1]), self.graph1.nodes, "Error: Couldn't create a simple graph.")
        self.assertSetEqual(set([self.edge01,self.edge10]), self.graph1.edges, "Error: Couldn't create a simple graph.")
        
    def test4_get_node_by_obj(self):
        self.assertIs(self.graph0.get_node_by_obj("My node"), None, "Error: get_node_by_obj failed.")
        
        self.assertIs(self.graph1.get_node_by_obj(None), None, "Error: get_node_by_obj failed.")
        self.assertIs(self.graph1.get_node_by_obj("No such node"), None, "Error: get_node_by_obj failed.")
        self.assertIs(self.graph1.get_node_by_obj("My node"), self.node1, "Error: get_node_by_obj failed.")
        
    def test5_get_exit_edges(self):
        edge_generator = self.graph1.get_exit_edges(self.node0)
        self.assertIs(next(edge_generator), self.edge01, "Error: get_exit_edge failed.")
        self.assertRaises(StopIteration, next, edge_generator)
        
        edge_generator = self.graph1.get_exit_edges(self.node1)
        self.assertIs(next(edge_generator), self.edge10, "Error: get_exit_edge failed.")
        self.assertRaises(StopIteration, next, edge_generator)
    
    def test6_get_enter_edges(self):
        edge_generator = self.graph1.get_enter_edges(self.node0)
        self.assertIs(next(edge_generator), self.edge10, "Error: get_enter_edge failed.")
        self.assertRaises(StopIteration, next, edge_generator)
        
        edge_generator = self.graph1.get_enter_edges(self.node1)
        self.assertIs(next(edge_generator), self.edge01, "Error: get_enter_edge failed.")
        self.assertRaises(StopIteration, next, edge_generator)
    
    def test7_get_edges(self):
        edge_generator = self.graph1.get_edges(self.node0)
        self.assertIn(next(edge_generator), self.graph1.edges, "Error: get_edge failed.")
        self.assertIn(next(edge_generator), self.graph1.edges, "Error: get_edge failed.")
        self.assertRaises(StopIteration, next, edge_generator)
        
        edge_generator = self.graph1.get_edges(self.node1)
        self.assertIn(next(edge_generator), self.graph1.edges, "Error: get_edge failed.")
        self.assertIn(next(edge_generator), self.graph1.edges, "Error: get_edge failed.")
        self.assertRaises(StopIteration, next, edge_generator)
        
    def test8_add_node(self):
        self.graph0.add_node(self.node0)
        self.graph0.add_node(self.node1)
        self.graph0.add_node(2)
        self.graph0.add_node(3)
        self.graph0.add_node(3)
        nodes_data_list = [node.data for node in self.graph0.nodes]
        
        self.assertIn(None, nodes_data_list, "Error: add_node failed.")
        self.assertIn("My node", nodes_data_list, "Error: add_node failed.")        
        self.assertIn(2, nodes_data_list, "Error: add_node failed.")
        self.assertIn(3, nodes_data_list, "Error: add_node failed.")
        self.assertEqual(4, len(self.graph0.nodes), "Error: add_node failed.")
    
    def test9_add_directed_edge(self):
        self.graph0.add_directed_edge(self.node1, )
    
    def test10_add_nodes_from(self):
        pass
    
    def test11_add_edges_from(self):
        pass
    
    def test12_attach_node(self):
        pass
    
    def test13_attach_edge(self):
        pass
    
    def test14_attach_edges_from(self):
        pass
    
    def test15_remove_node(self):
        pass
    
    def test16_remove_edge(self):
        pass
    
    def test17_remove_edges_from(self):
        pass
    
    def test18_del_node(self):
        pass
    
    def test19_del_edge(self):
        pass
    
    def test20_del_nodes_from(self):
        pass
    
    def test20_del_edges_from(self):
        pass

    @classmethod
    def tearDownClass(cls):
        #super(TestGraph, cls).tearDownClass()(self):
        cls.node0 = None
        cls.node1 = None
        cls.edge01 = None
        cls.edge10 = None
        cls.graph0 = None
        cls.graph1 = None

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()