'''
Created on Dec 13, 2017

@author: iko
'''
from itertools import repeat

def generate_node(self, n = 0):
        for _ in repeat(None, n):
            self.nodes.add(Node())
            
def generate_edges(self):
    pass

def generate_graph(self, node_count = 0, edge_count = 0):
    '''
    Generate a graph using #node_count nodes & #edge_count edges, and update self.
     
    :param node_count: #nodes in graph
    :param edge_count: #edges in graph
    :invariant: edge_count <= node_count*(node_count -1)
    :return: Graph with max(node_count, #self.nodes) nodes & max(edge_count, #self.edges) edges
    '''
    while (node_count < 0):
        self.add_node()
        node_count -= 1
        
    while (edge_count < 0):
        self.add_directed_edge() #TODO: create new edge
        edge_count -= 1

class Graph:
    '''
    classdocs
    '''
    def __init__(self, nodes = set(), edges = set()):

        '''
        Constructor
        
        :param nodes: iterable type.
        :param edges: iterable type. 
        '''
        self.id = id(self)
        self.nodes = set()
        self.edges = set()
       
        self.add_nodes_from(nodes)
        self.add_edges_from(edges)
        
    def __str__(self):
        return str(self.id)
    
    def get_node_by_obj(self, obj):
        '''
        Return node from self.nodes s.t. node.data = obj and obj != None, if exists.
         Else return None.
        
        :param obj: any object. 
        '''
        for node in iter(self.nodes):
            if node.data == obj and obj != None:
                return node
        
        return None
    
    def get_exit_edges(self, node):
        '''
        Return generator for edges from self.edges s.t. edge.data[0] = node, if exists.
        
        :param node: any object.
        '''
        for edge in iter(self.edges):
            if edge.exit_node == node:
                yield edge
                
    def get_enter_edges(self, node):
        '''
        Return generator for edges from self.edges s.t. edge.data[1] = node, if exists.
        
        :param node: any object.
        '''
        for edge in iter(self.edges):
            if edge.enter_node == node:
                yield edge
                
    def get_edges(self, node):
        '''
        Return generator for edges from self.edges s.t. edge.data[0] = node or edge.data[1] = node, if exists.
        
        :param node: any object.
        '''
        for edge in iter(self.edges):
            if edge.exit_node == node or edge.enter_node == node:
                yield edge
    
    def add_node(self, obj):
        '''
        Add a new node created from obj, only if:
        * obj node doesn't already exists.
        * obj is not a node in graph.
        
        :param obj: any object.
        :postcondition: (lambda ret: isinstance(ret) = Node)
        '''
        node = obj if isinstance(obj, Node) else Node(obj)#TODO: Last change. Fix doc
        self.attach_node(node)
    
    def add_directed_edge(self, exit_obj, enter_obj, parallel = False):
        '''
        Add a new edge object from exit_obj to enter_obj according to:
        *If (exit_obj,enter_obj) edge already exists in self and:
            * parallel = True, Add a new parallel (exit_obj,enter_obj) edge.
            * parallel = False, do nothing. 
        *If exit_obj, enter_obj or both are Node objects, but not part of self, attach relevant nodes to graph, and add (exit_obj,enter_obj) edge.
        *If exit_obj, enter_obj or both aren't Node objects, Create & Add relevant Node objects, and add (exit_obj,enter_obj) edge.
        
        :param exit_obj: any object.
        :param enter_obj: any object.
        :note: for obj = exit_obj\enter_obj, new node won't be added if Node(obj) already exists in graph.
        '''
            
        exit_node = exit_obj if isinstance(exit_obj, Node) else self.get_node_by_obj(exit_obj)
        exit_node = Node(exit_obj) if exit_node == None else exit_node
         
        enter_node = enter_obj if isinstance(enter_obj, Node) else self.get_node_by_obj(enter_obj)
        enter_node = Node(enter_obj) if enter_node == None else enter_node
        
        self.attach_edge(Edge(exit_node, enter_node), parallel)
        
    def add_nodes_from(self, objs):
        '''
        Add objs to self.nodes.
        
        :param objs: iterable of any type.
        '''
        for obj in objs:
            self.add_node(obj)
    
    def add_edges_from(self, objs, parallel = False):
        '''
        Add objs to self.edges.
        
        :param objs: iterable of Tuple or Edge type. Each tuple has the form of (exitObj, enterObj).
        '''
        for obj in objs:                
            if isinstance(obj, tuple):
                self.add_directed_edge(obj[0], obj[1], parallel)
            elif isinstance(obj, Edge):
                self.attach_edge(obj, parallel)
            else:
                raise TypeError("Tuple or Edge object expected, got %s" % obj.__class__.__name__)
        
    def attach_node(self, node):
        '''
        Attach node to self.nodes, only if node.data is not an object in self.nodes.
        
        :param node: type Node.
        '''
        if not isinstance(node, Node):
            raise TypeError("Node object expected, got %s" % node.__class__.__name__)
        
        if self.get_node_by_obj(node.data) == None:
            self.nodes.add(node)               
    
    def attach_edge(self, edge, parallel = False):
        '''
        Attach edge to self.edges. Verify edge's nodes are graph nodes.
        
        :param edge: type Edge.
        :precondition: type(edge[0]) = type(edge[1]) = Node
        '''
        if not isinstance(edge, Edge):
            raise TypeError("Edge object expected, got %s" % edge.__class__.__name__)
        
        if not parallel and edge.exit_node in iter(edge.exit_node for edge in self.edges) and edge.enter_node in iter(edge.enter_node for edge in self.edges):#TODO: Improvr memory usage
            print("(%s,%s) already exists in graph edges." % (edge.exit_node, edge.enter_node))
            return
        
        self.attach_node(edge.exit_node)
        self.attach_node(edge.enter_node)
        
        self.edges.add(edge)
        edge.exit_node.exit_degree += 1
        edge.enter_node.enter_degree += 1     
    
    def attach_edges_from(self, edges, parallel = False):
        '''
        Attach edges to self.edges.
        
        :param edges: iterable of type Edge.
        '''
        for edge in edges:
            self.attach_edge(edge, parallel)
                      
    def remove_node(self, node):
        '''
        Remove node from self.nodes. Raises KeyError if not present.
        
        :param node: type Node.
        '''
        if not isinstance(node, Node):
            raise TypeError("Node object expected, got %s" % node.__class__.__name__)
        else:
            self.nodes.remove(node)
            for edge in self.get_edges(node):
                self.remove_edge(edge)
    
    def remove_edge(self, edge):
        '''
        Remove edge from self.edges. Raises KeyError if not present.
        
        :param edge: type Edge.
        '''
        if not isinstance(edge, Edge):
            raise TypeError("Edge object expected, got %s" % edge.__class__.__name__)
        else:
            self.edges.remove(edge)
            edge.exit_node.exit_degree -= 1
            edge.enter_node.enter_degree -= 1
    
    def remove_edges_from(self, edges):
        '''
        Remove edges to self.edges.
        
        :param edges: iterable of type Edge.
        '''
        for edge in edges:
            self.remove_edge(edge)
            
    def del_node(self, obj):
        '''
        Delete node containing obj, if:
        * node(obj) exists.
        * obj is a node in graph.
        
        :param obj: any object.
        '''
        node = obj if isinstance(obj, Node) else self.get_node_by_obj(obj)
        if node != None:
            self.remove_node(node)
        else:
            print("obj %s is not a node in graph" % obj)
    
    def del_edge(self, exit_obj, enter_obj):
        '''
        Delete all parallel edges between (exit_obj, enter_obj).
        
        :param obj: any object.
        '''
        self.remove_edges_from(iter(edge for edge in self.edges if
                                     edge.exit_node == self.get_node_by_obj(exit_obj) and
                                      edge.enter_node == self.get_node_by_obj(enter_obj)))
    
    def del_nodes_from(self, objs):
        '''
        Remove objs from self.nodes.
        
        :param objs: iterable of any type.
        '''
        for obj in objs:
            self.del_node(obj)
    
    def del_edges_from(self, objs):
        '''
        Remove objs from self.edges.
        
        :param objs: iterable of any type.
        '''
        for obj in objs:
            self.del_edge(obj)
        
class Edge:
    '''
    classdocs
    '''
    def __init__(self, exit_node, enter_node):
        '''
        Constructor
        '''
        if not isinstance(exit_node, Node) or not isinstance(enter_node, Node):
            raise TypeError("Node objects expected, got (%s,%s)" % (exit_node.__class__.__name__,enter_node.__class__.__name__))
        
        self.id = id(self)
        self.exit_node = exit_node
        self.enter_node = enter_node
        
    def __str__(self):
        return str(self.id)

class Node:
    '''
    classdocs
    '''
    
    def __init__(self, obj = None):
        '''
        Constructor
        :invariant: self.exit_degree >= 0.
        :invariant: self.enter_degree >= 0.
        :invariant: self.full_degree >= 0
        '''
        self.id = id(self)
        self.data = obj
        self.exit_degree = 0
        self.enter_degree = 0
        
    def __str__(self):
        return str(self.id)

    def _get_full_degree(self):
        return self.exit_degree + self.enter_degree
    
    full_degree = property(_get_full_degree)