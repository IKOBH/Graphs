'''
Created on Jan 27, 2018

@author: iko
'''
import unittest
from itertools import count
from components import graph

class TestGraph(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        #super(TestGraph, cls).setUpClass()(self):
        cls.graph0  = graph.Graph()
        cls.graph1  = graph.Graph()
        cls.node0   = graph.Node()
        cls.node1   = graph.Node()
        cls.edge01  = graph.Edge(cls.node0,cls.node1)
        cls.edge10  = graph.Edge(cls.node1,cls.node0)
                
    def test_create_node(self):
        self.assertEqual(0, self.node0.get_id(), "Error: Couldn't create a simple node.")
        self.assertEqual(1, self.node1.get_id(), "Error: Couldn't create a simple node.")

    def test_create_edge(self):        
        self.assertEqual((0,1), self.edge01.get_id(), "Error: Couldn't create a simple edge.")
        self.assertEqual(self.node0, self.edge01.get_from_node(), "Error: Couldn't create a simple edge.")
        self.assertEqual(self.node1, self.edge01.get_to_node(), "Error: Couldn't create a simple edge.")
        
        self.assertEqual((1,0), self.edge10.get_id(), "Error: Couldn't create a simple edge.")
        self.assertEqual(self.node1, self.edge10.get_from_node(), "Error: Couldn't create a simple edge.")
        self.assertEqual(self.node0, self.edge10.get_to_node(), "Error: Couldn't create a simple edge.")
        
    def test_create_graph(self):
        self.assertEqual(0, self.graph0.get_id(), "Error: Couldn't create a simple graph.")
        self.assertEqual(set(), self.graph0.get_nodes(), "Error: Couldn't create a simple graph.")
        self.assertEqual(set(), self.graph0.get_edges(), "Error: Couldn't create a simple graph.")
        
        self.assertEqual(1, self.graph1.get_id(), "Error: Couldn't create a simple graph.")
        self.assertEqual(set(), self.graph1.get_nodes(), "Error: Couldn't create a simple graph.")
        self.assertEqual(set(), self.graph1.get_edges(), "Error: Couldn't create a simple graph.")

    @classmethod
    def tearDownClass(cls):
        #super(TestGraph, cls).tearDownClass()(self):
        cls.graph = None

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()