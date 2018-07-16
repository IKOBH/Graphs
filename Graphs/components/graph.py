"""
Created on Dec 13, 2017

:author: iko
"""

import yaml
import logging.config
from definitions import CONFIG_PATH
from collections import Hashable, Iterable, Mapping

with open(str(CONFIG_PATH)) as f:
    config_dict = yaml.load(f)

logging.config.dictConfig(config_dict)
logger = logging.getLogger(__name__)


# TODO: Delete this class.
class _AttrObject(object):
    """
    classdocs
    """

    def __init__(self, **attributes_dict):
        """
        Constructor
        """
        self.id = id(self)
        self.set_attrs(**attributes_dict)

    @property # TODO: arrange property get\set\del attrs. or delete entire _AttrObject.
    def get_attrs(self):
        """
        :return: Object's get_attrs.
        """
        return self.__dict__

    def set_attr(self, attr, val):
        """
        Set object's attribute 'attr' to val.

        :param attr:
        :param val:
        """
        setattr(self, attr, val)

    def set_attrs(self, **attributes):
        """
        Set object's attributes.

        :param attributes:
        """
        for attr, val in attributes.items():
            self.set_attr(attr, val)

    def del_attr(self, attr):
        """
        Delete object's attribute.

        :param attr: type = string.
        """
        delattr(self, attr)

    def del_attrs(self, attributes):
        """
        Delete object's attributes.

        :param attributes: iterable of attribute strings.
        """
        for attr in attributes:
            self.del_attr(attr)


# TODO: Return generators instead of sets wherever I can.
# TODO: Make 'self.nodes = <Some iterable>' call add_nodes. Do the same with edges.
class Graph(_AttrObject):
    """
    classdocs
    """

    def __init__(self, nodes=None, edges=None, nodes_attributes=None, edges_attributes=None, **attributes):
        """
        Constructor

        :param nodes: graph's nodes. iterable of Hashable type.
        :param edges: graph's edges.iterable of iterable of Hashable type.
        :param nodes_attributes: nodes default attributes. iterable of key-value type or None.
        :param edges_attributes: edges default attributes. iterable of key-value type or None.
        :param **attributes: graph's default attributes.
        """

        _AttrObject.__init__(self, **attributes)
        self.nodes = set()
        self.edges = set()

        try:
            self.add_nodes(nodes, **nodes_attributes)
        except TypeError:
            self.add_nodes(nodes)

        try:
            self.add_edges(edges, nodes_attributes=nodes_attributes, **edges_attributes)
        except TypeError:
            self.add_edges(edges, nodes_attributes=nodes_attributes)

    def __str__(self):
        return str(self.id)

    # TODO : Might want to use __repr__ or __str__ of _Node object.
    @property
    def nodes_data(self):
        """
        :return: graph's node's get_attrs. type = dictionary valued dictionary.
        """
        return {node.name: node.get_attrs for node in self.nodes}

    # TODO : Might want to use __repr__ or __str__ of _Edge object.
    @property
    def edges_data(self):
        """
        :return: graph's edge's get_attrs. type = dictionary valued dictionary.
        """
        return {frozenset(node.name for node in edge.nodes): edge.get_attrs for edge in self.edges}

    # TODO : Might want to use __repr__ or __str__.
    @property
    def get_attrs(self):
        """
        :return: graph's get_attrs. type = dictionary valued dictionary.
        """
        return {'nodes': self.nodes_data, 'edges': self.edges_data}

    def get_node(self, name):
        """
        Return node named 'name' if exists, else return None.

        :param name: node's name.
        :type name: Hashable.
        :rtype _Node | None
        """

        try:
            return next(node for node in self.nodes if node.name == name)
        except StopIteration:
            return None

    # TODO: Implement more efficiently.
    def get_nodes(self, names):
        """
        Return graph's nodes, s.t. node's name in 'names' if exists, else return None.

        :param names: nodes names.
        :type names: Iterable[Hashable].
        :rtype set(_Node | None) | None.
        """

        try:
            return {self.get_node(name) for name in set(names)}
        except TypeError as err:
            logger.warning(err)
            return None

    def set_node(self, name, **attributes):
        """
        Set 'name' named node attributes using 'attributes'.

        :param name: node's name.
        :type name: Hashable.
        :param attributes: node's new attributes.
        :type attributes: Mapping.
        :return: node.
        :rtype: _Node | None
        """

        node = self.get_node(name)

        try:
            node.set_attrs(**attributes)
        except AttributeError as err:
            logger.warning(err)

        return node

    def set_nodes(self, names, **attributes):
        """
        Set nodes named from 'names' with 'attributes'.

        :param names: nodes names.
        :type names: Iterable[Hashable]
        :param attributes: nodes new attributes
        :type attributes: Mapping.
        :return: nodes with new attributes.
        :rtype: Iterable[_Node] | None
        """

        try:
            return {self.set_node(name, **attributes) for name in set(names)}
        except TypeError as err:
            logger.warning(err)
            return None

    def add_node(self, name=None, override=True, **attributes):
        """
        Add new node named 'name' if not exists, else override node's attributes if 'override' is True.

        :param name: node's name.
        :type name: Hashable.
        :param override: if true, & node named 'name' exists, override its attributes.
        Else return existing node with old attributes.
        :type override: bool.
        :param attributes: node's attributes.
        :type attributes: Mapping.
        :return: node named 'name'.
        :rtype: _Node.
        """

        node = self.set_node(name, **attributes) if override else self.get_node(name)
        node = _Node(name, **attributes) if node is None else node
        self.nodes.add(node)

        return node

    # TODO: Try to make implementation more efficient. maybe by using union instead of add to self.nodes.
    # TODO: For better efficiency, implement get_nodes and set_nodes in O(N) if can, or O(NlogN) using ordering.
    # TODO: Use these implemented methods to implement add_nodes.
    def add_nodes(self, names, **attributes):
        """
        Add new nodes named name, s.t name in 'name', if not exist.

        :param names: nodes names.
        :type names: Iterable[Hashable].
        :param attributes: nodes attributes.
        :type attributes: Mapping.
        :return: set of nodes.
        :rtype: set(_Node) | None
        """

        try:
            return {self.add_node(name, **attributes) for name in names}
        except TypeError as err:
            logger.warning(err)
            return None

    def del_node(self, name):
        """
        Delete node named 'name', if exists.

        :param name: node's name.
        :type name: _Node.
        :return: deleted node.
        :rtype: _Node.
        """

        node = self.get_node(name)

        try:
            self._remove_edges(node.edges)
        except AttributeError as err:
            logger.warning(err)

        else:
            self.nodes.discard(node)

        return node

    # TODO: Try to make implementation more efficient. maybe by using union instead of add to self.nodes.
    # TODO: For better efficiency, implement get_nodes and set_nodes in O(N) if can, or O(NlogN) using ordering.
    # TODO: Use these implemented methods to implement del_nodes
    def del_nodes(self, names):
        """
        Delete nodes named name, s.t. name in 'names' from  graph's nodes.

        :param names: nodes names.
        :type names: Iterable[Hashable]
        :return: deleted nodes.
        :rtype: set(_Node).
        """
        return {self.del_node(name) for name in set(names)}

    # TODO: Might combine this method with get_edge_by_node_objects to one method.
    def get_edge(self, *nodes_names):  # TODO: Change to support parallel edges.
        """
        Return edge from  graph's edges if exists, else returns None

        :param nodes_names: edge'd nodes names.
        :type nodes_names: Iterable[Hashable].
        :rtype _Edge | None
        :note Graph should not contain an edge object with empty set of nodes.
        """

        return self._get_edge_by_nodes_objects(self.get_nodes(nodes_names))

    # TODO: Doesn't supports multi graph.
    def _get_edge_by_nodes_objects(self, nodes):
        """
        Return edge from graph's edges s.t edge.nodes == 'nodes'.

        :param nodes: edge nodes.
        :type nodes: Iterable[_Node].
        :rtype _Edge | None
        :note: Graph should not contain an edge object with empty set of nodes.
        """

        try:
            return next(edge for edge in self.edges if edge.nodes == set(nodes))
        except (StopIteration, TypeError) as err:
            logger.warning(err)
            return None

    # TODO: Might want to combine set_edge with set_edges.
    def set_edge(self, names, **attributes):
        pass

    def set_edges(self, names, **attributes):
        pass

    # TODO: use new syntax for parameters. PEP 3102.
    # TODO: Create a mechanism for users to add 'attributes', handle them and view documentation about them.
    # TODO: move 'nodes_attributes' & 'parallel' from function declaration into 'attributes' handling.
    # TODO: Add 'override' option like in 'add_node'.
    # TODO: on setting edge as parallel, ensure all other edges are parallel.
    def add_edge(self, *nodes_names, nodes_attributes=None, parallel=False, override=True, **attributes):
        """
        Add new edge with nodes named 'nodes_names' if not exists or 'parallel' is True.

        If edge exists & 'parallel' is false, return existing edge.
        :param nodes_names: edge's nodes names.
        :type nodes_names: Iterable[Hashable]
        :param nodes_attributes: edge's nodes attributes.
        :type nodes_attributes: Mapping | None.
        :param parallel: parallel edge.
        :type parallel: bool.
        :param override: if true, overrides edge's attributes.
        :type override: bool
        :param attributes: edge's attributes.
        :type attributes: Mapping.
        :return: edge if received valid arguments, None otherwise.
        :rtype: _Edge.
        """

        if hasattr(self, 'directed') and self.directed and 'exit_nodes' not in attributes:
            logger.error("This is a directed graph. 'attributes' must specify 'exit_nodes'")
            raise ValueError("This is a directed graph. 'attributes' must specify 'exit_nodes'")

        existing_nodes = self.get_nodes(nodes_names)
        edge = self._get_edge_by_nodes_objects(existing_nodes)

        if edge is None or parallel:
            existing_nodes.discard(None)
            new_nodes_names = set(nodes_names) - {node.name for node in existing_nodes}
            edge = _Edge(new_nodes_names, existing_nodes, nodes_attributes, parallel=parallel, **attributes)
            self.nodes |= edge.nodes
            self.edges.add(edge)

        elif override:
            # TODO: for node in nodes_names: node.set_attrs(nodes_attributes)
            edge.set_attrs(**attributes)

        return edge

    # TODO: Try to make implementation more efficient. maybe by using union instead of add to self.edges.
    def add_edges(self, edges_names, **attributes):
        """
        Add new edges from edges_names.

        :param edges_names: Each edge_name contains nodes_names.
        :type edges_names: Iterable[Iterable[Hashable]]
        :param attributes: edges attributes.
        :type attributes: Iterable[Mapping]
        :return: set of edges.
        :rtype: set(_Edge) | None
        """

        try:
            return {self.add_edge(*nodes_names, **attributes) for nodes_names in edges_names}
        except TypeError as err:
            logger.warning(err)
            return None

    def _remove_edge(self, edge):
        """
        Remove edge from  graph's edges.

        :param edge: edge to be removed.
        :type edge: _Edge | None.
        :return: removed edge if found in graph's edges. None otherwise.
        :rtype: _Edge | None.
        """

        try:
            for node in edge.nodes:
                node.edges.remove(edge)
        except AttributeError as err:
            logger.warning(err)
            return None
        else:
            self.edges.remove(edge)

        return edge

    def _remove_edges(self, edges):
        """
        Remove edges from self.edges.

        Raises AttributeError if edge not of _Edge type.
        :param edges: edges to be removed.
        :type edges: Iterable[_Edge]
        :return: set of removed edges.
        :rtype: set(_Edge) | None
        """

        try:
            return {self._remove_edge(edge) for edge in set(edges)}
        except TypeError as err:
            logger.warning(err)
            return None

    def del_edge(self, *names):
        """
        Delete edge with 'names' nodes.

        :param names: edge's nodes names.
        :type names: Iterable[Hashable]
        :return: deleted edge.
        :rtype: _Edge.
        """
        return self._remove_edge(self.get_edge(*names))

    def del_edges(self, nodes_names_iterable):
        """
        Delete edges between 'names_iterable' nodes.

        :param nodes_names_iterable: iterable of Hashable type.
        :type nodes_names_iterable: Iterable[Iterable[Hashable]]
        :return: deleted edges.
        :rtype: set(_Edge) | None
        """
        try:
            return {self.del_edge(*names) for names in set(nodes_names_iterable)}
        except TypeError as err:
            logger.warning(err)
            return None

    def set_attr(self, attr, val):
        """
        Set graph's attributes.

        :param attr: type of strings.
        :param val: attribute value.
        """
        _AttrObject.set_attr(self, attr, val)
        if attr == 'directed' and val is True:
            _Edge.exit_nodes = set()
            _Edge.enter_nodes = set()
            _Node.exit_edges = set()
            _Node.enter_edges = set()
            _Node.exit_degree = property(lambda node_self: len(node_self.exit_edges))
            _Node.enter_degree = property(lambda node_self: len(node_self.enter_edges))

        if attr == 'directed' and val is False:
            self.del_attr('directed')

    def del_attr(self, attr):
        """
        Delete graph's attribute.

        :param attr: type of strings.
        """
        _AttrObject.del_attr(self, attr)
        if attr == 'directed':
            delattr(_Edge, 'exit_nodes')
            delattr(_Edge, 'enter_nodes')
            delattr(_Node, 'exit_edges')
            delattr(_Node, 'enter_edges')
            delattr(_Node, 'exit_degree')
            delattr(_Node, 'enter_degree')


class _Edge(_AttrObject):
    """
    classdocs
    """

    # TODO: Try make implementation better.
    def __init__(self, nodes_names=None, nodes=None, nodes_attributes=None, **attributes):
        """
        Constructor

        Construct new edge using newly created nodes from 'nodes_names' and existing 'nodes' objects.
        Set all node objects (newly created & existing ones) attributes using 'nodes_attributes'.
        Existing node attributes will be overwritten.
        Set edge attributes using 'attributes'.
        Supports: hyper graph, multi graph.

        :todo check if need to change all docstrings to 'parameter' or 'arg'.Check also 'numpy docstring conventions'.
        :param nodes_names: names of edge's nodes.
        :type nodes_names: Iterable[Hashable] | None
        :param nodes: nodes from graph.
        :type nodes: Iterable[_Node] | None
        :param nodes_attributes: default nodes attributes to be used.
        :type nodes_attributes: Mapping.
        """

        _AttrObject.__init__(self, **attributes)
        self._nodes = None
        self.nodes = nodes
        self._nodes_names = None
        self.nodes_names = nodes_names

        if not self.nodes_names and not self.nodes:
            logger.error("Either 'nodes_names' or 'nodes' must be a non empty Iterable")
            raise ValueError("Either 'nodes_names' or 'nodes' must be a non empty Iterable")

        nodes_attributes = {} if nodes_attributes is None else nodes_attributes
        new_nodes = None if self.nodes_names is None else {_Node(node_name, **nodes_attributes)
                                                           for node_name in self.nodes_names}
        self.nodes = self.nodes or new_nodes if not (self.nodes and new_nodes) else new_nodes | self.nodes

        for node in self.nodes:
            node.edges.add(self)

    def __str__(self):
        return str(self.id)

    def set_attr(self, attr, val):
        """
        Set edge's attributes.
        """
        # if attr == 'nodes_attributes':
        #     for node in self.nodes:
        #         node.set_attrs(val)

        if attr == 'exit_nodes' and bool(set(val)):
            exit_nodes_names = set(val)
            exit_nodes = set(filter(lambda node: node.name in exit_nodes_names , self.nodes))
            enter_nodes = self.nodes - exit_nodes

            self.exit_nodes = exit_nodes
            self.enter_nodes = self.nodes - exit_nodes

            for exit_node in exit_nodes:
                if not hasattr(exit_node, 'exit_edges'):
                    exit_node.exit_edges = set()
                exit_node.exit_edges.add(self)
                exit_node.exit_degree = len(exit_node.exit_edges)

            for enter_node in enter_nodes:
                if not hasattr(enter_node, 'enter_edges'):
                    enter_node.enter_edges = set()
                enter_node.enter_edges.add(self)
                enter_node.enter_degree = len(enter_node.enter_edges)

#            _Node.exit_degree = property(lambda node_self: len(node_self.exit_edges))
#            _Node.enter_degree = property(lambda node_self: len(node_self.enter_edges))

        else:
            _AttrObject.set_attr(self, attr, val)

    def del_attr(self, attr):
        """
        Delete edge's attribute.

        :param attr: type of strings.
        """
        if attr == 'direction':
            delattr(self, 'directed')
            delattr(self, 'exit_nodes')
            delattr(self, 'enter_nodes')
        else:
            _AttrObject.del_attr(attr)

    @property
    def is_loop(self):
        return True if len(self.nodes) == 1 else False

    @property
    def nodes_names(self):
        return self._nodes_names

    @nodes_names.setter
    def nodes_names(self, names):
        try:
            self._nodes_names = None if names is None else set(names)
        except TypeError as err:
            logger.warning(err)

    @nodes_names.deleter
    def nodes_names(self):
        del self._nodes_names

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        try:
            self._nodes = None if nodes is None else set(nodes)
        except TypeError as err:
            logger.warning(err)

    @nodes.deleter
    def nodes(self):
        del self._nodes


class _Node(_AttrObject):
    """
    classdocs
    """

    # TODO: Switch to new syntax with * to declare positional parameters.
    def __init__(self, name=None, **attributes):
        """
        Constructor

        :type name: Hashable
        :type attributes: Mapping
        :invariant: self.degree >= 0
        """

        _AttrObject.__init__(self, **attributes)
        self._name = None
        self.name = name
        self.edges = set()

    def __str__(self):
        return str(self.id)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, Hashable):
            logger.error("Hashable 'name' expected, got {0}".format(type(name).__name__))
            raise TypeError("Hashable 'name' expected, got {0}".format(type(name).__name__))

        self._name = id(self) if name is None else name

    @name.deleter
    def name(self):
        del self._name

    @property
    def degree(self):
        """
        Return node's degree.
        """

        return len(self.edges) + sum(edge.is_loop for edge in self.edges)
