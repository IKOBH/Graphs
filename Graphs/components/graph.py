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


class Graph(_AttrObject):
    """
    classdocs
    """

    def __init__(self, nodes=None, edges=None, nodes_attributes=None, edges_attributes=None, **attributes):
        """
        Constructor

        :param nodes: graph's _nodes. iterable of Hashable type.
        :param edges: graph's _edges.iterable of iterable of Hashable type.
        :param nodes_attributes: _nodes default attributes. iterable of key-value type or None.
        :param edges_attributes: _edges default attributes. iterable of key-value type or None.
        :param **attributes: graph's default attributes.
        """

        _AttrObject.__init__(self, **attributes)
        self._nodes = {}
        self._edges = {}

        if nodes:
            try:
                self.add_nodes_from(*nodes, **nodes_attributes)
            except TypeError:
                self.add_nodes_from(*nodes)

        if edges:
            try:
                self.add_edges_from(*edges, nodes_attributes=nodes_attributes, **edges_attributes)
            except TypeError:
                self.add_edges_from(*edges, nodes_attributes=nodes_attributes)

    def __str__(self):
        return str(self.id)

    # TODO : Might want to use __repr__ or __str__ of _Node object.
    @property
    def nodes_data(self):
        """
        :return: graph's node's get_attrs. type = dictionary valued dictionary.
        """

        return {node.key: node.get_attrs for node in self.nodes}

    # TODO : Might want to use __repr__ or __str__ of _Edge object.
    @property
    def edges_data(self):
        """
        :return: graph's edge's get_attrs. type = dictionary valued dictionary.
        """

        return {frozenset(node.key for node in edge.nodes): edge.get_attrs for edge in self.edges}

    # TODO : Might want to use __repr__ or __str__.
    @property
    def get_attrs(self):
        """
        :return: graph's get_attrs. type = dictionary valued dictionary.
        """

        return {'_nodes': self.nodes_data, '_edges': self.edges_data}

    def get_node(self, key):
        """
        Return node with 'key' if exists, else return None.

        :param key: node's key.
        :type key: Hashable.
        :rtype _Node | None
        """

        try:
            return self._nodes[key]
        except TypeError as err:
            logger.warning(err)
            return None
        except KeyError as err:
            logger.debug(err)
            return None

    def get_nodes_from(self, *keys):
        """
        Return graph's _nodes, s.t. node's name in 'names' if exists, else return None.
        :param keys: _nodes names.
        :type keys: Iterable[Hashable].
        :rtype set(_Node | None) | None.
        """

        return {self.get_node(key) for key in keys}

    def set_node(self, key, **attributes):
        """
        Set 'key' named node attributes using 'attributes'.

        :param key: node's key.
        :type key: Hashable.
        :param attributes: node's new attributes.
        :type attributes: Mapping.
        :return: node.
        :rtype: _Node | None
        """

        node = self.get_node(key)

        try:
            node.set_attrs(**attributes)
        except AttributeError as err:
            logger.debug(err)

        return node

    def set_nodes_from(self, *keys, **attributes):
        """
        Set _nodes named from 'names' with 'attributes'.

        :param keys: _nodes names.
        :type keys: Iterable[Hashable]
        :param attributes: _nodes new attributes
        :type attributes: Mapping.
        :return: _nodes with new attributes.
        :rtype: Iterable[_Node] | None
        """

        return {self.set_node(key, **attributes) for key in keys}

    def add_node(self, key, overwrite=True, **attributes):
        """
        Add new node named 'key' if not exists, else override node's attributes if 'override' is True.

        :param key: node's key.
        :type key: Hashable.
        :param overwrite: if true, & node named 'key' exists, override its attributes.
        Else return existing node with old attributes.
        :type overwrite: bool.
        :param attributes: node's attributes.
        :type attributes: Mapping.
        :return: node named 'key'.
        :rtype: _Node.
        """

        node = self.set_node(key, **attributes) if overwrite else self.get_node(key)
        if node is None:
            node = _Node(key, **attributes)
            self._nodes[key] = node

        return node

    def add_nodes_from(self, *keys, overwrite=True, **attributes):
        """
        Add new _nodes named key, s.t key in 'key', if not exist.

        :param keys: _nodes names.
        :type keys: Iterable[Hashable].
        :param overwrite: ??
        :type overwrite: bool
        :param attributes: _nodes attributes.
        :type attributes: Mapping.
        :return: set of _nodes.
        :rtype: set(_Node) | None
        """

        return {self.add_node(key, overwrite=overwrite, **attributes) for key in keys}

    def del_node(self, key):
        """
        Delete node named 'key', if exists.

        :param key: node's key.
        :type key: _Node.
        :return: deleted node.
        :rtype: _Node.
        """

        node = self.get_node(key)

        try:
            self.del_edges_from(node.edges_keys)
        except AttributeError as err:
            logger.debug(err)
        else:
            del self._nodes[key]

        return node

    def del_nodes_from(self, *keys):
        """
        Delete _nodes named key, s.t. key in 'names' from  graph's _nodes.

        :param keys: _nodes names.
        :type keys: Iterable[Hashable]
        :return: deleted _nodes.
        :rtype: set(_Node).
        """

        return {self.del_node(key) for key in keys}

    # TODO: Doesn't supports multi graph.
    def get_edge(self, *key):
        """
        Return edge from  graph's _edges if exists, else returns None

        :param key: edge'd _nodes names.
        :type key: Iterable[Hashable].
        :rtype _Edge | None
        :note Graph should not contain an edge object with empty set of _nodes.
        """

        try:
            return self._edges[frozenset(key)]  # TODO: Use of 'frozenset' requires decoupling.
        except KeyError as err:
            logger.debug(err)
            return None

    def get_edges_from(self, *keys):

        return {self.get_edge(*key) for key in keys}

    def set_edge(self, *key, **attributes):
        """
         Set 'key' named edge attributes using 'attributes'.

         :param key: edge's key.
         :type key: Hashable.
         :param attributes: edge's new attributes.
         :type attributes: Mapping.
         :return: edge.
         :rtype: _Edge | None
         """

        edge = self.get_edge(*key)

        try:
            edge.set_attrs(**attributes)
        except AttributeError as err:
            logger.debug(err)

        return edge

    def set_edges_from(self, *keys, **attributes):
        """
        Set edges named from 'keys' with 'attributes'.

        :param keys: edges keys.
        :type keys: Iterable[Hashable]
        :param attributes: _edges new attributes
        :type attributes: Mapping.
        :return: _edges with new attributes.
        :rtype: Iterable[_Edge] | None
        """

        return {self.set_edge(*key, **attributes) for key in keys}

    # TODO: Improve implementation.
    # TODO: use new syntax for parameters. PEP 3102.
    # TODO: Create a mechanism for users to add 'attributes', handle them and view documentation about them.
    # TODO: move 'nodes_attributes' & 'multi' from function declaration into 'attributes' handling.
    # TODO: Add 'overwrite' option like in 'add_node'.
    # TODO: on setting edge as multi, ensure all other _edges are multi.
    def add_edge(self, *key, overwrite_nodes=True, nodes_attributes=None, multi=False, overwrite=True, **attributes):
        """
        Add new edge with _nodes named 'key' if not exists or 'multi' is True.

        If edge exists & 'multi' is false, return existing edge.
        :param key: edge's _nodes names.
        :type key: Iterable[Hashable]
        :param nodes_attributes: edge's _nodes attributes.
        :type nodes_attributes: Mapping | None.
        :param multi: multi edge.
        :type multi: bool.
        :param overwrite: if true, overrides edge's attributes.
        :type overwrite: bool
        :param attributes: edge's attributes.
        :type attributes: Mapping.
        :return: edge if received valid arguments, None otherwise.
        :rtype: _Edge.
        """

        edge = self.set_edge(*key, **attributes) if overwrite else self.get_edge(*key)

        if edge is None or multi:
            existing_nodes = set(self.get_nodes_from(*key))
            existing_nodes.discard(None)
            new_nodes_keys = set(key) - {node.key for node in existing_nodes}
            new_key = new_nodes_keys | existing_nodes

            edge = _Edge(new_key, overwrite_nodes, nodes_attributes, multi=multi, **attributes)
            self._edges[edge.key] = edge
            for node in edge.nodes:
                self._nodes[node.key] = node

        return edge

    def add_edges_from(self, *keys, **attributes):
        """
        Add new _edges from edges_names.

        :param keys: Each edge_name contains key.
        :type keys: Iterable[Iterable[Hashable]]
        :param attributes: _edges attributes.
        :type attributes: Iterable[Mapping]
        :return: set of _edges.
        :rtype: set(_Edge) | None
        """

        return {self.add_edge(*key, **attributes) for key in keys}

    def del_edge(self, *key):
        """
        Delete edge with 'names' _nodes.

        :param key: edge's _nodes names.
        :type key: Iterable[Hashable]
        :return: deleted edge.
        :rtype: _Edge.
        """

        edge = self.get_edge(*key)

        try:
            for node in edge.nodes:
                node.del_edge(*key)
        except AttributeError as err:
            logger.debug(err)
        else:
            del self._edges[edge.key]

        return edge

    def del_edges_from(self, *keys):
        """
        Delete _edges between 'names_iterable' _nodes.

        :param keys: iterable of Hashable type.
        :type keys: Iterable[Iterable[Hashable]]
        :return: deleted _edges.
        :rtype: set(_Edge) | None
        """

        return {self.del_edge(*key) for key in keys}

    @property
    def nodes(self):
        return self._nodes.values()

    @property
    def edges(self):
        return self._edges.values()


class _Edge(_AttrObject):
    """
    classdocs
    """

    # TODO: Improve implementation.
    def __init__(self, nodes, overwrite=True, nodes_attributes=None, **attributes):
        """
        Constructor

        Construct new edge using newly created _nodes from 'key' and existing '_nodes' objects.
        Set all node objects (newly created & existing ones) attributes using 'nodes_attributes'.
        Existing node attributes will be overwritten.
        Set edge attributes using 'attributes'.
        Supports: hyper graph, multi graph.

        :todo check if need to change all docstrings to 'parameter' or 'arg'.Check also 'numpy docstring conventions'.
        :param nodes: _nodes from graph.
        :type nodes: Iterable[_Node | Hashable]
        :param nodes_attributes: default _nodes attributes to be used.
        :type nodes_attributes: Mapping.
        """

        _AttrObject.__init__(self, **attributes)
        if not nodes:
            logger.exception("Non empty '_nodes' Iterable[_Node | Hashable] expected,"
                             " got {0}".format(type(nodes).__name__))
            raise TypeError("Non empty '_nodes' Iterable[_Node | Hashable] expected,"
                            " got {0}".format(type(nodes).__name__))

        self._nodes = {node.key: node for node in filter(lambda node: isinstance(node, _Node), nodes)}

        try:
            if overwrite:
                for node in self.nodes:
                    node.set_attrs(**nodes_attributes)

            self._nodes.update({node_key: _Node(node_key, **nodes_attributes) for node_key in
                                filter(lambda node: not isinstance(node, _Node), nodes)})
        except TypeError as err:
            logger.debug(err)
            self._nodes.update({node_key: _Node(node_key) for node_key in
                                filter(lambda node: not isinstance(node, _Node), nodes)})

        for node in self.nodes:
            node.attach_edge(self)

    def __str__(self):
        return str(self.id)

    # TODO: Currently returns same as self._nodes. Will be changed when Multi support will be added.
    @property
    def key(self):
        return frozenset(self._nodes.keys())

    @property
    def nodes(self):
        return self._nodes.values()

    # TODO: Why I am not using this? check if necessary.
    @property
    def nodes_keys(self):
        return self._nodes.keys()

    @property
    def is_loop(self):
        return True if len(self.nodes) == 1 else False


class _Node(_AttrObject):
    """
    classdocs
    """

    # TODO: Switch to new syntax with * to declare positional parameters.
    # TODO: If changed may I use attributes instead of **attributes?
    def __init__(self, key, **attributes):
        """
        Constructor

        :type key: Hashable
        :type attributes: Mapping
        :invariant: self.degree >= 0
        """

        if not isinstance(key, Hashable):
            logger.exception("Hashable 'key' expected, got {0}".format(type(key).__name__))
            raise TypeError("Hashable 'key' expected, got {0}".format(type(key).__name__))

        _AttrObject.__init__(self, **attributes)
        self.key = key
        self.edges = {}

    def __str__(self):
        return str(self.id)

    @property
    def edges(self):
        return self._edges.values()

    @edges.setter
    def edges(self, edges):
        try:
            self._edges = {edge.key: edge for edge in set(edges)}
        except (TypeError, AttributeError) as err:
            self._edges = self._edges if self._edges else {}
            logger.warning(err)

    @property
    def edges_keys(self):
        return self._edges.keys()

    def attach_edge(self, edge):
        try:
            self._edges[edge.key] = edge
        except AttributeError as err:
            logger.warning(err)

    # TODO: Might want to add a return value.
    def del_edge(self, *key):
        try:
            del self._edges[key]
        except TypeError as err:
            logger.warning(err)
        except KeyError as err:
            logger.debug(err)

    @property
    def degree(self):
        """
        Return node's degree.
        """

        return len(self.edges) + sum(edge.is_loop for edge in self.edges)
