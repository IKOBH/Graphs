'''
Created on Dec 13, 2017

@author: iko
'''
#from platform import node

class Graph:
    '''
    classdocs
    '''
    def __init__(self, id, nodes = None, edges = None):

        '''
        Constructor
        '''
        self.id     = id
        self.nodes  = (set(), nodes)[nodes != None]
        self.edges  = (set(), edges)[edges != None]

    def __str__(self):
        return str(self.id)

    def get_nodes(self):
        return self.nodes
    
    def get_edges(self):
        return self.edges
    
    def get_id(self):
        return self.id
    
    def add_node(self, node):
        self.nodes.add(node)
        
    def add_edge(self, edge):
        self.edges.add(edge)
        
    def update_nodes(self, nodes):
        for node in nodes:
            self.nodes.add(node)
    
    def update_edges(self, edges):
        for edge in edges:
            self.edges.add(edge)
            
    def del_node(self, node):
        self.nodes.discard(node)
        
    def del_edge(self, edge):
        self.edges.discard(edge)
    
    '''
    @param nodeCount: #nodes in graph
    @param edgeCount: #edges in graph
    @invariant: edgeCount <= nodeCount*(nodeCount -1)
    @return: Graph with max(nodeCount, #self.nodes) nodes & 
            max(edgeCount, #self.edges) edges
    '''    
    def generate_graph(self, nodeCount = 0, edgeCount = 0): 
            
        while (nodeCount < 0):
            self.add_node() #TODO: create new node
            nodeCount -= 1
            
        while (edgeCount < 0):
            self.add_edge() #TODO: create new edge
            edgeCount -= 1
        
        
class Edge:
    '''
    classdocs
    '''

    def __init__(self, fromNode, toNode):
        '''
        Constructor
        '''
        self.id         = (fromNode.get_id(), toNode.get_id())
        self.fromNode   = fromNode
        self.toNode     = toNode
        
    def __str__(self):
        return str(self.id)
    
    def get_from_node(self):
        return self.fromNode
    
    def get_to_node(self):
        return self.toNode
    
    def get_id(self):
        return self.id
            
class Node:
    '''
    classdocs
    '''

    def __init__(self, id = None):
        '''
        Constructor
        '''
        self.id = id
        
    def __str__(self):
        return str(self.id)
        
    def get_id(self):
        return self.id
    