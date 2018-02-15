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

class Graph(object):
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
    
    @property
    def nodes_data(self):
        '''
        Return graph's node's data as a set.
        '''
        return set([node.data for node in self.nodes])
    
    @property    
    def edges_data(self):
        '''
        Return graph's edge's data as a set of tuples (exit node_data, enter_node_data).
        '''
        return set([(edge.exit_node.data, edge.enter_node.data) for edge in self.edges])
    
    def get_node_by_obj(self, obj):
        '''
        Return node from self.nodes s.t. node.data = obj, if exists. Else return None.
        
        :param obj: any object. 
        '''
        for node in self.nodes:
            if node.data == obj:
                return node
        
        return None
    
    def get_edge_by_objs(self, exit_obj, enter_obj):
        '''
        Return edge from self.edges s.t. edge.exit_node.data = exit.obj & edge.enter_node.data = enter.obj, if exists. Else return None.
        
        :param obj: any object. 
        '''
        for edge in self.edges:
            if exit_obj == edge.exit_node.data and enter_obj == edge.enter_node.data:
                return edge
        
        return None                   
    
    def add_node(self, obj):
        '''
        Add a new node with obj as it's data, if not exists.
        
        :param obj: any object.
        :return: node. type(node) = Node
        '''
        node = self.get_node_by_obj(obj)
        if node == None:
            node = Node(obj) 
            self.nodes.add(node)
        
        return node 
    
    def add_directed_edge(self, exit_obj, enter_obj):
        '''
        Add a new edge with exit_obj as it's exit node's data & enter_obj as it's enter node's data, if not exists.
        
        :param exit_obj: any object.
        :param enter_obj: any object.
        :return: edge. type(edge) = Edge
        '''
        edge = self.get_edge_by_objs(exit_obj, enter_obj)
        if edge == None:
            exit_node = self.add_node(exit_obj)
            enter_node = self.add_node(enter_obj)
            edge = Edge(exit_node, enter_node)
            self.edges.add(edge)
            exit_node.exit_edges.add(edge)
            enter_node.enter_edges.add(edge)            
            
        return edge
            
    def add_nodes_from(self, objs):
        '''
        Add new nodes with objects from objs as their data, if not exist.
        
        :param objs: iterable of any type.
        :return: set(nodes). for node in nodes, type(node) = Node
        '''
        node_bunch = set()
        
        for obj in set(objs):
            node_bunch.add(self.add_node(obj))
        
        return node_bunch
    
    def add_edges_from(self, objs):
        '''
        Add new edges with objects from objs as their data, if not exist.
        
        :param objs: iterable of Tuple type. Each tuple has the form of (exitObj, enterObj).
        :return: set(edges). for edge in edges, type(edge) = Edge
        '''
        edge_bunch = set()
        
        for obj in set(objs):                
            if not isinstance(obj, tuple):
                raise TypeError("Tuple object expected, got %s" % obj.__class__.__name__)

            edge_bunch.add(self.add_directed_edge(obj[0], obj[1]))
        
        return edge_bunch
        
    def _remove_edge(self, edge):
        '''
        Remove edge from self.edges. 
        
        Raises TypeError if edge not of Edge type.
        Raises KeyError if not present.
        :param edge: type Edge.
        '''
        if not isinstance(edge, Edge):
            raise TypeError("Edge object expected, got %s" % edge.__class__.__name__)
        else:
            edge.exit_node.exit_edges.remove(edge)
            edge.enter_node.enter_edges.remove(edge)
            self.edges.remove(edge)
    
    def _remove_edges_from(self, edges):
        '''
        Remove edges from self.edges.
        
        Raises TypeError if edge not of Edge type.
        Raises KeyError if not present.
        :param edges: iterable of type Edge.
        '''
        for edge in set(edges):
            self._remove_edge(edge)
            
    def del_node(self, obj):
        '''
        Delete node with data = obj, if exists.
        
        :param obj: any object.
        :return: deleted node. Type Node.
        '''
        node = self.get_node_by_obj(obj)
        if node != None:
            self._remove_edges_from(node.adjacencies_edges)
            self.nodes.discard(node)
            
        return node
    
    def del_edge(self, exit_obj, enter_obj):
        '''
        Delete edge between exit node with data exit_obj & enter node with data enter_obj.
        
        :param exit_obj: any object.
        :param enter_obj: any object.
        :return: deleted edge. Type Edge.
        '''
        edge = self.get_edge_by_objs(exit_obj, enter_obj)
        if edge != None:
            self._remove_edge(edge)
            
        return edge
    
    def del_nodes_from(self, objs):
        '''
        Delete nodes with data = obj for each obj in objs, if exists.
        Delete objs from self.nodes.
        
        :param objs: iterable of any type.
        :return: deleted nodes. Type Node set.
        '''
        return set(self.del_node(obj) for obj in set(objs))
            
    def del_edges_from(self, objs):
        '''
        Delete edges between exit node with data exit_obj & enter node with data enter_obj, for each (exitObj, enterObj) tuple.

        :param objs: iterable of Tuple type. Each tuple has the form of (exitObj, enterObj).        
        :return: deleted edges. Type Edge set.
        '''
        return set(self.del_edge(obj[0], obj[1]) for obj in set(objs))
            
class Edge(object):
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

class Node(object):
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
        self.data = self.id if obj == None else obj
        self.exit_edges = set()
        self.enter_edges = set()
        
    def __str__(self):
        return str(self.id)
    
    @property            
    def adjacencies_edges(self):
        '''
        Return node adjacencies edges, if exists.
        '''
        return self.exit_edges.union(self.enter_edges)
    
    @property
    def exit_degree(self):
        '''
        Return node exit degree.
        '''
        return len(self.exit_edges)
    @property
    def enter_degree(self):
        '''
        Return node enter degree.
        '''
        return len(self.enter_edges)
    @property
    def degree(self):
        '''
        Return node full degree.
        '''
        return self.exit_degree + self.enter_degree
