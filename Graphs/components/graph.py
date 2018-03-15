'''
Created on Dec 13, 2017

:author: iko
'''
from itertools import repeat


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
        :invariant: self.exit_degree >= 0.
        :invariant: self.enter_degree >= 0.
        :invariant: self.full_degree >= 0
        '''
        self.id = id(self)
        self.set_attrs(**attrs_dict)

    @property
    def data(self):
        '''
        Return Object's data.
        :return: type = dictionary. 
        '''
        return self.__dict__

    def set_attr(self, attr, val):
        '''
        Add or Change node's attributes.
        '''
        setattr(self, attr, val)

    def set_attrs(self, **attrs):
        '''
        Add or Change node's attributes.
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

    def __init__(self, nodes=None, edges=None, **attrs):  # TODO: Consider improving implementation.
        '''
        Constructor

        :param nodes: iterable type.
        :param edges: iterable type.
        '''
        _Attr_Object.__init__(self, **attrs)
#        self.id = id(self)
        self.nodes = set()
        self.edges = set()

        nodes = set() if nodes is None else nodes
        edges = set() if edges is None else edges

        self.add_nodes_from(nodes)
        self.add_edges_from(edges)

    def __str__(self):
        return str(self.id)

    @property
    def nodes_data(self):
        '''
        Return graph's node's data as a set.
        '''
        return {node.obj for node in self.nodes}

    @property
    def edges_data(self):
        '''
        Return graph's edge's data as a set of tuples (exit node_data, enter_node_data).
        '''
        return {edge.data for edge in self.edges}

    @property
    def data(self):
        '''
        Return graph's data as a dictionary.
        '''
        return _Attr_Object.data.update({'nodes' : self.nodes_data, 'edges' : self.edges_data})

    def get_node_by_obj(self, obj):
        '''
        Return node from self.nodes s.t. node.data = obj, if exists. Else return None.

        :param obj: any object.
        '''
        for node in self.nodes:
            if node.obj == obj:
                return node

        return None

    def get_edge_by_objs(self, *objs):  # TODO: Change to support parallel edges.
        '''
        Return edge from self.edges.

        If exists return edge s.t data of edge.nodes = obj0 & objs.
        Else return None.

        :param objs: any object.
        :attention: Graph should not contain an edge object with empty set of nodes.
        '''
        for edge in self.edges:
            if set(node.obj for node in edge.nodes) == set(objs):
                return edge

        return None

    def add_node(self, obj, **attrs):
        '''
        Add a new node with obj as it's data, if not exists.

        :param obj: any object.
        :param attrs: sequence of key-value pairs.
        :return: node. type(node) = _Node
        '''
        node = self.get_node_by_obj(obj)
        if node is None:
            node = _Node(obj, **attrs)
            self.nodes.add(node)
        else:
            node.set_attrs(**attrs)

        return node

    def add_edge(self, *objs, **attrs):  # TODO: Add hyper & multi edge support.
        '''
        Add a new edge with obj & objs as its nodes data & attrs as its attributes.
        
        Add edge only if not exists. Distinguish between attrs & undirected edges.

        :todo: Add parallel edges support.
        :param objs: any object.
        :param attrs: sequence of key-value pairs.
        :return: edge. type(edge) = _DiEdge.
        '''
        edge = self.get_edge_by_objs(*objs)
        if edge is None:
            node_bunch = self.add_nodes_from(objs)
            edge = _Edge(node_bunch, **attrs)
            self.edges.add(edge)

            for node in node_bunch:
                node.edges.add(edge)
        else:
            edge.set_attrs(**attrs)

        return edge

    def add_nodes_from(self, objs, **attrs):  # TODO: Change attr default value to None.
        '''
        Add new nodes with objects from objs as their data, if not exist.

        :param objs: iterable of any type.
        :param attrs: sequences of key-value pairs.
        :return: set(nodes). for node in nodes, type(node) = _Node
        '''
        node_bunch = set()

        for obj in objs:
            node_bunch.add(self.add_node(obj, **attrs))

        return node_bunch

    def add_edges_from(self, objs_iterable, **attrs):
        '''
        Add new edges with objects from objs_iterable as their data, if not exist.

        :param objs_iterable: iterable of any obj type.
        :param attrs: iterable of sequences of key-value pairs.
        :return: set(edges). for edge in edges, type(edge) = _Edge
        '''
        edge_bunch = set()

        for objs in objs_iterable:
            edge_bunch.add(self.add_edge(*objs, **attrs))

        return edge_bunch

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
        for edge in set(edges):
            self._remove_edge(edge)

    def del_node(self, obj):
        '''
        Delete node with data = obj, if exists.

        :param obj: any object.
        :return: deleted node. Type _Node.
        '''
        node = self.get_node_by_obj(obj)
        if node != None:
            self._remove_edges_from(node.edges)
            self.nodes.discard(node)

        return node

    def del_edge(self, *objs):  # TODO: Combine with remove_edge.
        '''
        Delete edge between exit node with data objs & enter node with data enter_obj.

        :param objs: any object.
        :return: deleted edge. Type _DiEdge.
        '''
        edge = self.get_edge_by_objs(*objs)
        if edge != None:
            self._remove_edge(edge)

        return edge

    def del_nodes_from(self, objs):
        '''
        Delete nodes with data = obj for each obj in objs, if exists.
        Delete objs from self.nodes.

        :param objs: iterable of any type.
        :return: deleted nodes. Type _Node set.
        '''
        return set(self.del_node(obj) for obj in set(objs))

    def del_edges_from(self, objs_iterable):
        '''
        Delete edges.

        Delete edges between nodes with data = objs from objs_iterable. 

        :param objs_iterable: iterable of any type.
        :return: deleted edges. Type _DiEdge set.
        '''
        return set(self.del_edge(*objs) for objs in set(objs_iterable))


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


class _Node(_Attr_Object):  # TODO: Consider deleting self.obj & make it a special attribute.
    '''
    classdocs
    '''

    def __init__(self, obj, **attrs):
        '''
        Constructor
        :invariant: self.exit_degree >= 0.
        :invariant: self.enter_degree >= 0.
        :invariant: self.degree >= 0
        '''
        _Attr_Object.__init__(self, **attrs)
        self.obj = obj
        self.edges = set()

    def __str__(self):
        return str(self.id)

    @property
    def degree(self):
        '''
        Return node's degree.
        '''
        loop_counter = len([edge for edge in self.edges if len(edge.nodes) == 1])
        return len(self.edges) + loop_counter
