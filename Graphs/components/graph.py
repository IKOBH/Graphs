'''
Created on Dec 13, 2017

@author: iko
'''
from itertools import count, repeat

def generate_node(self, n = 0):
        for _ in repeat(None, n):
            self.nodes.add(Node())
            
def generate_edges(self):
    pass #TODO: add implementation.

def generate_graph(self, nodeCount = 0, edgeCount = 0):
    '''
    Generate a graph using #nodeCount nodes & #edgeCount edges, and update self.
     
    :param nodeCount: #nodes in graph
    :param edgeCount: #edges in graph
    :invariant: edgeCount <= nodeCount*(nodeCount -1)
    :return: Graph with max(nodeCount, #self.nodes) nodes & max(edgeCount, #self.edges) edges
    '''
    while (nodeCount < 0):
        self.add_node() #TODO: create new node
        nodeCount -= 1
        
    while (edgeCount < 0):
        self.add_edge() #TODO: create new edge
        edgeCount -= 1

class Graph:
    '''
    classdocs
    '''
    ids = count(0)
    def __init__(self, nodes = set(), edges = set()):

        '''
        Constructor
        :todo: verify nodes & edges are of iterable type.
        '''
        self.id = next(self.ids)
        self.nodes  = set(nodes) #TODO: Verify nodes are of iterable type
        self.edges  = set(edges) #TODO: Verify edges are of iterable type

    def __str__(self):
        return str(self.id)

    def get_id(self):
        ''' Get self id'''
        return self.id
    
    def get_nodes(self):
        ''' Get self nodes'''
        return self.nodes
    
    def get_edges(self):
        '''Get self edges'''
        return self.edges
    
    def add_node(self, id):
        '''
        Create a new node with id. If id not in self.get_nodes, add it .
        
        :param id: hashable object.
        '''
        self.attach_node(Node(id))
        
    def add_edge(self, fromNode, toNode):
        '''
        Add a user specified edge to graph.
        
        :param fromNode: edge starting node.
        :param toNode:   edge ending node.
        '''
        self.attach_edge(Edge(fromNode, toNode))
        
    def add_nodes_from(self, ids = set()):
        for id in ids:
            self.add_node(id)
    
    def add_edges_from(self):
        pass
        
    def attach_node(self, node):
        '''
        Attach node to self.
        
        :param node: type Node.
        '''
        if node.__class__ != Node:
            raise TypeError("Node object expected, got" + node.__class__.__name__)
        elif node.id in set([node.id for node in self.get_nodes()]):
            raise RuntimeError("Node id already exists in graph(%s)" % node.get_id())
        else:
            self.nodes.add(node) 
    
    def attach_edge(self, edge):
        '''
        Attach edge to self.
        
        :param edge: type Edge.
        '''
        if edge.__class__ != Edge:
            raise TypeError("Edge object expected, got" + edge.__class__.__name__)
        elif edge.id in set([node.id for node in self.get_nodes()]):
            raise RuntimeError("Edge id already exists in graph(%s)" % node.get_id())
        else:
            self.edges.add(edge)
    
    def attach_nodes(self, nodes):
        '''
        Attach nodes to self.
        
        :param nodes: iterable of type Node.
        '''
        for node in nodes:
            self.nodes.add(node)
    
    def attach_edges(self, edges):
        '''
        Attach edges to self.
        
        :param edges: iterable of type Edge.
        '''
        for edge in edges:
            self.edges.add(edge)
                      
    def del_node(self, node):
        self.nodes.discard(node)
        
    def del_edge(self, edge):
        self.edges.discard(edge)        
        
class Edge:
    '''
    classdocs
    '''
    ids = count(0)
    def __init__(self, fromNode, toNode):
        '''
        Constructor
        '''
        self.id         = next(self.ids)
        #TODO: Delete - self.id         = (fromNode.get_id(), toNode.get_id())
        self.fromNode   = fromNode
        self.toNode     = toNode
        
    def __str__(self):
        return str(self.id)
    
    def get_id(self):
        return self.id
    
    def get_from_node(self):
        return self.fromNode
    
    def get_to_node(self):
        return self.toNode
            
class Node:
    '''
    classdocs
    '''
    
    ids = count(0)
    def __init__(self, id = None):
        '''
        Constructor
        '''
        self.id = next(self.ids) if id == None else id
        
    def __str__(self):
        return str(self.id)
        
    def get_id(self):
        return self.id
