'''
Created on Dec 13, 2017

:author: iko
'''
from itertools import repeat
from collections import Hashable


def generate_node(self, num=0):
    for _ in repeat(None, num):
        self.nodes.add(_Node())


def generate_edges(self):
    pass


def generate_graph(self, node_count=0, edge_count=0):
    '''
    Generate a graph using #node_count nodes & #edge_count edges, and update self.

    :param node_count: #nodes in graph
    :param edge_count: #edges in graph
    :invariant: edge_count <= node_count*(node_count -1)
    :return: Graph with max(node_count, #self.nodes) nodes & max(edge_count, #self.edges) edges
    '''
    while node_count < 0:
        self.add_node()
        node_count -= 1

    while edge_count < 0:
        self.add_edge()
        edge_count -= 1


class _Attr_Object(object):
    '''
    classdocs
    '''

    def __init__(self, **attrs_dict):
        '''
        Constructor
        '''
        self.id = id(self)
        self.set_attrs(**attrs_dict)

    @property
    def data(self):
        '''
        :return: Object's data.
        '''
        return self.__dict__

    def set_attr(self, attr, val):
        '''
        Set node's attribute 'attr' to val.
        
        :param attr:
        :param val:
        '''
        setattr(self, attr, val)

    def set_attrs(self, **attrs):
        '''
        Set node's attributes.
        
        :param **attr:  
        '''
        for attr, val in attrs.items():
            self.set_attr(attr, val)

    def del_attr(self, attr):
        '''
        Delete node's attribute.
        
        :param attr: type = strings. 
        '''
        delattr(self, attr)

    def del_attrs(self, attrs):
        '''
        Delete node's attributes.
        
        :param attrs: iterable of attribute strings. 
        '''
        for attr in attrs:
            self.del_attr(attr)


class Graph(_Attr_Object):
    '''
    classdocs
    '''

    def __init__(self, nodes=None, edges=None, nodes_attrs=None, edges_attrs=None, **attrs):
        '''
        Constructor

        :param nodes: graph's nodes. iterable of Hashable type.
        :param edges: graph's edges.iterable of iterable of Hashable type.
        :param nodes_attrs: nodes default attributes. iterable of key-value type or None.
        :param edges_attrs: edges default attributes. iterable of key-value type or None.
        :param **attrs: graph's default attributes.
        '''
        _Attr_Object.__init__(self, **attrs)
        self.nodes = set()
        self.edges = set()

        nodes = set() if nodes is None else nodes
        edges = set() if edges is None else edges
        nodes_attrs = {} if nodes_attrs is None else nodes_attrs
        edges_attrs = {} if edges_attrs is None else edges_attrs

        self.add_nodes_from(nodes, **nodes_attrs)
        self.add_edges_from(edges, nodes_attrs, **edges_attrs)

    def __str__(self):
        return str(self.id)

    @property
    def nodes_data(self):
        '''
        :return: graph's node's data. type = dictionary valued dictionary.
        '''
        return {node.name: node.data for node in self.nodes}

    @property
    def edges_data(self):
        '''
        :return: graph's edge's data. type = dictionary valued dictionary.
        '''
        return {frozenset(node.name for node in edge.nodes): edge.data for edge in self.edges}

    @property
    def data(self):
        '''
        :return: graph's data. type = dictionary valued dictionary.
        '''
        return {'nodes' : self.nodes_data, 'edges' : self.edges_data}

    def get_node_by_name(self, name):
        '''
        Return node from self.nodes s.t. node.data = name, if exists. Else return None.

        :param name: any object.
        '''
        for node in self.nodes:
            if node.name == name:
                return node

        return None

    def get_edge_by_names(self, *names):  # TODO: Change to support parallel edges.
        '''
        Return edge from self.edges.

        If exists return edge s.t data of edge.nodes = obj0 & names.
        Else return None.

        :param names: any object.
        :attention: Graph should not contain an edge object with empty set of nodes.
        '''
        for edge in self.edges:
            if {node.name for node in edge.nodes} == set(names):
                return edge

        return None

    def add_node(self, name, **attrs):
        '''
        Add a new node with name as it's data, if not exists.

        :param name: Hashable object.
        :param attrs: sequence of key-value pairs.
        :return: node. type(node) = _Node
        '''
        node = self.get_node_by_name(name)
        if node is None:
            node = _Node(name=name, **attrs)
            self.nodes.add(node)
        else:
            node.set_attrs(**attrs)

        return node

    def add_edge(self, *names, nodes_attrs={}, **attrs):  # TODO: Add multi edge support.
        '''
        Add a new edge with names as its nodes data & attrs as its attributes.
        
        Add edge only if not exists. Distinguish between attrs & undirected edges.

        :todo: Add parallel edges support.
        :param names: sequence of Hashable.
        :param nodes_attrs: iterable of key-value pairs.
        :param attrs: sequence of key-value pairs.
        :return: edge. type(edge) = _Edge.
        '''
        if nodes_attrs == None:
            raise ValueError("nodes_attrs must be a mapping, not NoneType")
        edge = self.get_edge_by_names(*names)
        if edge is None:
            nodes = self.add_nodes_from(names, **nodes_attrs)
            edge = _Edge(nodes, **attrs)
            self.edges.add(edge)

            for node in nodes:
                node.edges.add(edge)
        else:
            edge.set_attrs(**attrs)

        return edge

    def add_nodes_from(self, names, **attrs):
        '''
        Add new nodes with objects from names as their data, if not exist.

        :param names: iterable of Hashable type.
        :param attrs: sequences of key-value pairs.
        :return: set(nodes). for node in nodes, type(node) = _Node
        '''
        return {self.add_node(name, **attrs) for name in names}

    def add_edges_from(self, names_iterable, nodes_attrs={}, **attrs):
        '''
        Add new edges with objects from names_iterable as their data, if not exist.

        :param names_iterable: iterable of Hashable type.
        :param nodes_attrs: iterable of key-value pairs.
        :param attrs: iterable of sequences of key-value pairs.
        :return: set(edges). for edge in edges, type(edge) = _Edge
        '''
        return {self.add_edge(*names, nodes_attrs=nodes_attrs, **attrs) for names in names_iterable}

    def _remove_edge(self, edge):
        '''
        Remove edge from self.edges.

        Raises TypeError if edge not of _Edge type.
        Raises KeyError if not present.
        :param edge: type _Edge.
        '''
        if not isinstance(edge, _Edge):
            raise TypeError("_Edge object expected, got %s" % type(edge).__name__)
        else:
            for node in edge.nodes:
                node.edges.remove(edge)

            self.edges.remove(edge)

    def _remove_edges_from(self, edges):
        '''
        Remove edges from self.edges.

        Raises TypeError if edge not of _DiEdge type.
        Raises KeyError if not present.
        :param edges: iterable of type _DiEdge.
        '''
        return {self._remove_edge(edge) for edge in set(edges)}

    def del_node(self, name):
        '''
        Delete node with data = name, if exists.

        :param name: any object.
        :return: deleted node. Type _Node.
        '''
        node = self.get_node_by_name(name)
        if node != None:
            self._remove_edges_from(node.edges)
            self.nodes.discard(node)

        return node

    def del_edge(self, *names):
        '''
        Delete edge with 'names' nodes.

        :param names: Hashable object.
        :return: deleted edge. Type _DiEdge.
        '''
        edge = self.get_edge_by_names(*names)
        if edge != None:
            self._remove_edge(edge)

        return edge

    def del_nodes_from(self, names):
        '''
        Delete nodes with name in names, if exists.
        Delete names from self.nodes.

        :param names: iterable of Hashable type.
        :return: deleted nodes. Type _Node set.
        '''
        return {self.del_node(name) for name in set(names)}

    def del_edges_from(self, names_iterable):
        '''
        Delete edges.

        Delete edges between nodes with data = names from names_iterable. 

        :param names_iterable: iterable of Hashable type.
        :return: deleted edges. Type _DiEdge set.
        '''
        return {self.del_edge(*names) for names in set(names_iterable)}


class _Edge(_Attr_Object):
    '''
    classdocs
    '''

    def __init__(self, nodes, **attrs):
        '''
        Constructor
        :param nodes: iterable of _Node type.  
        '''
        if not any(nodes):
            raise ValueError("Edge must contain at least 1 node object in nodes, got empty set.")

        for node in nodes:
            if not isinstance(node, _Node):
                raise TypeError("_Node objects expected, got %s(%s)" % (type(node).__name__, node))

        _Attr_Object.__init__(self, **attrs)
        self.nodes = set(nodes)

    def __str__(self):
        return str(self.id)

    def set_attr(self, attr, val):
        '''
        Add or Change edge's attributes.
        '''
        _Attr_Object.set_attr(self, attr, val)
        if attr == 'directed' and self.directed:
            delattr(self, 'exit_node')
            delattr(self, 'enter_node')

    def del_attr(self, attr):
        '''
        Delete edge's attribute.
        
        :param attr: type of strings. 
        '''

        _Attr_Object.del_attr(attr)
        if attr == 'directed':
            delattr(self, 'exit_node')
            delattr(self, 'enter_node')


class _Node(_Attr_Object):
    '''
    classdocs
    '''

    def __init__(self, **attrs):
        '''
        Constructor
        
        :invariant: self.degree >= 0
        '''
        _Attr_Object.__init__(self, **attrs)
        self.edges = set()

    def __str__(self):
        return str(self.id)

    def set_attr(self, attr, val):
        if attr == 'name' and not isinstance(val, Hashable):
            raise TypeError("unhashable type: %s" % type(val).__name__)

        _Attr_Object.set_attr(self, attr, val)

    @property
    def degree(self):
        '''
        Return node's degree.
        '''
        loop_counter = len({edge for edge in self.edges if len(edge.nodes) == 1})
        return len(self.edges) + loop_counter
