'''
Created on Jan 27, 2018

@author: iko
'''
import unittest
from components import graph

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.graph = graph.Graph(0)
        
    def test_create_graph(self):
        self.assertEqual(0, self.graph.get_id(), "Error: Couldn't create a simple graph.")
        self.assertEqual(set(), self.graph.get_nodes(), "Error: Couldn't create a simple graph.")
        self.assertEqual(set(), self.graph.get_edges(), "Error: Couldn't create a simple graph.")
    
class TestEdge(unittest.TestCase):
    
    def setUp(self):
        self.node0  = graph.Node(0)
        self.node1  = graph.Node(1)
        self.edge   = graph.Edge(self.node0,self.node1)
        
    def test_create_edge(self):        
        self.assertEqual((0,1), self.edge.get_id(), "Error: Couldn't create a simple edge.")
        self.assertEqual(self.node0, self.edge.get_from_node(), "Error: Couldn't create a simple edge.")
        self.assertEqual(self.node1, self.edge.get_to_node(), "Error: Couldn't create a simple edge.")
    
class TestNode(unittest.TestCase):
    
    def setUp(self):
        self.node0 = graph.Node(0)
        self.node1 = graph.Node(1)
        
    def test_create_node(self):
        self.assertEqual(0, self.node0.get_id(), "Error: Couldn't create a simple node.")
        self.assertEqual(1, self.node1.get_id(), "Error: Couldn't create a simple node.")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()