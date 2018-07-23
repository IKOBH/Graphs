"""
Created on Dec 13, 2017

:author: iko
"""

from collections import Hashable, Counter
import logging.config
import yaml
from definitions import CONFIG_PATH

with open(str(CONFIG_PATH)) as f:
    configuration = yaml.load(f)

logging.config.dictConfig(configuration)
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


# TODO: use new syntax for parameters. PEP 3102.
# TODO: check if need to change all docstrings to 'parameter' or 'arg'.
# TODO: Check also 'numpy docstring conventions'.
# TODO: change  '**attributes' to 'attributes'
# TODO: Create a mechanism for users to add 'attributes', handle them and view documentation about them.
# TODO: use named tuples for edges keys(first is '_edges_multiplicity', second is 'nodes_keys')
class Graph(_AttrObject):
    """
    classdocs
    """

    def __init__(self, nodes=None, edges=None, nodes_attributes=None, edges_attributes=None, **attributes):
        """
        Constructor

        :param nodes: graph's nodes.
        :type nodes: Iterable[Hashable] | None
        :param edges: graph's _edges.
        :type edges: Iterable[Iterable[Hashable]] | None
        :param nodes_attributes: nodes attributes.
        :type nodes_attributes: Mapping | None
        :param edges_attributes: edges attributes.
        :type Mapping | None
        :param attributes: graph's attributes.
        :type attributes: Mapping
        """

        _AttrObject.__init__(self, **attributes)
        self._nodes = {}
        self._edges = {}
        self._edges_multiplicity = Counter()

        try:
            self.add_nodes_from(*nodes, **nodes_attributes)
        except TypeError:
            try:
                self.add_nodes_from(*nodes)
            except TypeError as err:
                logger.debug(err)

        try:
            self.add_edges_from(*edges, nodes_attributes=nodes_attributes, **edges_attributes)
        except TypeError:
            try:
                self.add_edges_from(*edges, nodes_attributes=nodes_attributes)
            except TypeError as err:
                logger.debug(err)

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
        Return graph's node with '_key' if exists, else return None.

        :param key: node's _key.
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
        Return graph's nodes with 'keys'.

        :param keys: nodes keys.
        :type keys: Iterable[Hashable].
        :return: nodes.
        :rtype set(_Node | None)
        """

        return {self.get_node(key) for key in keys}

    def set_node(self, key, **attributes):
        """
        Set node with '_key' using 'attributes'.

        :param key: node's _key.
        :type key: Hashable.
        :param attributes: node's attributes.
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
        Set nodes with 'keys' using 'attributes'.

        :param keys: nodes keys.
        :type keys: Iterable[Hashable]
        :param attributes: nodes attributes.
        :type attributes: Mapping.
        :return: _nodes.
        :rtype: Iterable[_Node]
        """

        return {self.set_node(key, **attributes) for key in keys}

    def add_node(self, key, overwrite=True, **attributes):
        """
        Add node with '_key'.

        Set node's attributes using 'attributes'.
        If 'overwrite' is True, node's attributes will be overwritten.

        :param key: node's _key.
        :type key: Hashable.
        :param overwrite: enable node's attributes overwriting.
        :type overwrite: bool.
        :param attributes: node's attributes.
        :type attributes: Mapping.
        :return: added node.
        :rtype: _Node.
        """

        node = self.set_node(key, **attributes) if overwrite else self.get_node(key)
        if node is None:
            node = _Node(key, **attributes)
            self._nodes[key] = node

        return node

    def add_nodes_from(self, *keys, **attributes):
        """
        Add nodes with 'keys' using 'attributes'.

        :param keys: nodes keys.
        :type keys: Iterable[Hashable].
        :param overwrite: enable nodes attributes overwriting.
        :type overwrite: bool
        :param attributes: nodes attributes.
        :type attributes: Mapping.
        :return: added nodes.
        :rtype: set(_Node)
        """

        return {self.add_node(key, **attributes) for key in keys}

    def del_node(self, key):
        """
        Delete node with '_key'.

        :param key: node's _key.
        :type key: Hashable.
        :return: deleted node.
        :rtype: _Node | None
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
        Delete graph's nodes with 'keys'.

        :param keys: nodes keys.
        :type keys: Iterable[Hashable]
        :return: deleted nodes.
        :rtype: set(_Node | None).
        """

        return {self.del_node(key) for key in keys}

    def get_edge(self, *nodes_keys, multi_id=0):
        """
        Return graph's edge with key=('multi_id', 'nodes_keys') if exists, None otherwise.

        :param nodes_keys: edge's nodes keys.
        :type nodes_keys: Iterable[Hashable].
        :param multi_id: edge's multi_id identifier.
        :type multi_id: int
        :return: edge.
        :rtype _Edge | None
        """

        try:
            return self._edges[multi_id, frozenset(nodes_keys)]
        except KeyError as err:
            logger.warning(err)
            return None

    def get_edges_from(self, *keys, multi=False):
        """
        Return graph's edges with 'keys', or None for each non existing _key.

        When searching multi edges, a single key is comprised of a sequence of two elements.
        First element holds a multiplicity edge indicator.
        Second element holds edge nodes keys.
        :param keys: edges keys.
        :type keys: Iterable[Sequence[int, Iterable[Hashable]] | Iterable[Hashable]]
        :param multi: enable multi edge search.
        :type multi: bool
        :return: edges
        :rtype: set(_Edge | None)
        """

        try:
            return {self.get_edge(*key[1:], multi_id=key[0]) if multi else self.get_edge(*key) for key in keys}
        except (TypeError, IndexError) as err:
            logger.warning(err)
            return None

    def set_edge(self, *nodes_keys, multi_id=0, **attributes):
        """
        Sets graph's edge with key=('multi_id', 'nodes_keys') if exists, using 'attributes'.

         :param nodes_keys: edge's nodes keys.
         :type nodes_keys: Iterable[Hashable].
         :param multi_id: edge's multi_id identifier.
         :type multi_id: int
         :param attributes: edge's attributes.
         :type attributes: Mapping.
         :return: edge.
         :rtype: _Edge | None
         """

        edge = self.get_edge(*nodes_keys, multi_id=multi_id)

        try:
            edge.set_attrs(**attributes)
        except AttributeError as err:
            logger.debug(err)

        return edge

    def set_edges_from(self, *keys, multi=False,  **attributes):
        """
        Set edges with 'keys' using 'attributes'.

        :param keys: edges keys.
        :type keys: Iterable[Sequence[int, Iterable[Hashable]] | Iterable[Hashable]]
        :param multi: enable multi edge search.
        :type multi: bool
        :param attributes: edges attributes.
        :type attributes: Mapping.
        :return: set edges.
        :rtype: Iterable[_Edge]
        """

        try:
            return {self.set_edge(*key[1:], multi_id=key[0], **attributes) if multi else
                    self.set_edge(*key, **attributes) for key in keys}
        except (TypeError, IndexError) as err:
            logger.warning(err)
            return None

    def add_edge(self, *nodes_keys, multi_id=0, overwrite_nodes=False, overwrite=True, **attributes):
        """
        Add edge with 'nodes_keys'.

        Use 'multi _id' to find specific edge. (use negative number to ensure parallel edge addition)
        If edge not found, generate sequential 'multi _id' for the added edge.
        Set edge's nodes attributes using 'nodes_attributes'.
        If 'overwrite_nodes' is True, existing nodes attributes will be overwritten.
        Set edge's attributes using 'attributes'.
        If 'overwrite' is True, edge's attributes will be overwritten.

        :param nodes_keys: edge's _key.
        :type nodes_keys: Iterable[Hashable]
        :param overwrite_nodes: enable edge's nodes attributes overwriting.
        :type overwrite_nodes: bool.
        :param multi_id: edge's multiplicity id.
        :type multi_id: int
        :param overwrite: enable edge's attributes overwriting.
        :type overwrite: bool
        :param attributes: edge's attributes.
        :type attributes: Mapping.
        :return: edge.
        :rtype: _Edge.
        """

        edge = self.set_edge(*nodes_keys, multi_id=multi_id, **attributes) if overwrite else \
            self.get_edge(*nodes_keys, multi_id=multi_id)

        if edge is None:
            multi_id = self.get_multiplicity(*nodes_keys)
            existing_nodes = set(self.get_nodes_from(*nodes_keys))
            existing_nodes.discard(None)
            new_nodes_keys = set(nodes_keys) - {node.key for node in existing_nodes}
            new_nodes = new_nodes_keys | existing_nodes
            edge = _Edge(new_nodes, multi_id, overwrite_nodes, **attributes)

            self._edges[edge.key] = edge
            self._edges_multiplicity += Counter({edge.nodes_keys: 1})
            for node in edge.nodes:
                self._nodes[node.key] = node

        return edge

    def add_edges_from(self, *keys, multi=False, **attributes):
        """
        Add edges with 'keys' using 'attributes'.

        :param keys: edges keys.
        :type keys: Iterable[Iterable[Hashable]]
        :param multi: enable multi edge addition.
        :type multi: bool
        :param attributes:  edges attributes.
        :type attributes: Iterable[Mapping]
        :return: edges.
        :rtype: set(_Edge)
        """

        return {self.add_edge(*key[1:], multi_id=key[0], **attributes) if multi else self.add_edge(*key, **attributes)
                for key in keys}

    def del_edge(self, *nodes_keys, multi_id=0):
        """
        Delete '_key' edge from graph's edges.

         If _edges_multiplicity is None, delete of all '_key' sharing child-edges.

        :param nodes_keys: edge's _nodes names.
        :type nodes_keys: Iterable[Hashable]
        :param multi_id: enable parallel edges.
        :type multi_id: int | None
        :return: deleted edge.
        :rtype: _Edge.
        """

        edge = self.get_edge(*nodes_keys, multi_id=multi_id)

        try:
            (node.del_edges(edge) for node in edge.nodes)
        except AttributeError as err:
            logger.debug(err)
        else:
            del self._edges[multi_id, frozenset(nodes_keys)]
            self._edges_multiplicity -= Counter({edge.nodes_keys: 1})

        return edge

    def del_edges_from(self, *keys, multi=False):
        """
        Delete edges with 'keys'.

        :param keys: edges keys.
        :type keys: Iterable[Iterable[Hashable]]
        :param multi: enable multi edge deletion.
        :type multi: bool
        :return: deleted edges.
        :rtype: set(_Edge)
        """

        return {self.del_edge(*key[1:], multi_id=key[0]) if multi else self.del_edge(*key) for key in keys}

    def get_multiplicity(self, *nodes_keys):
        """
        Return 'nodes_keys' based multi_id-edge's  multi_id.

        Return None if 'nodes_keys' type is invalid.
        :param nodes_keys: multi_id-edge's nodes_keys
        :type nodes_keys: Iterable[Hashable]
        :return: multi_id of multi_id-edge with 'nodes_keys'
        :type: int | None
        """

        try:
            return self._edges_multiplicity[frozenset(nodes_keys)]
        except TypeError as err:
            logger.warning(err)
            return None

    def get_multi_edge(self, *nodes_keys):
        """
        :param nodes_keys: edge's nodes keys.
        :type nodes_keys: Iterable[Hashable]
        :return: multi edge (nodes shared set of edges, differed only by multi_id number).
        :rtype: set(_Edge) | None
        """

        try:
            return {self.get_edge(*nodes_keys, multi_id=multi_id) for multi_id in
                    range(self.get_multiplicity(*nodes_keys))}
        except TypeError as err:
            logger.warning(err)
            return None

    def set_multi_edge(self, *nodes_keys, **attributes):
        """
         Set multi edge with 'nodes_keys' using 'attributes'.

         :param nodes_keys: edge's _key.
         :type nodes_keys: Iterable[Hashable].
         :param attributes: edge's attributes.
         :type attributes: Mapping.
         :return: multi edge (set of edges sharing nodes, differed only by multi_id number).
         :rtype: set(_Edge) | None
         """

        multi_edge = self.get_multi_edge(*nodes_keys)

        try:
            (edge.set_attrs(**attributes) for edge in multi_edge)
        except (TypeError, AttributeError) as err:
            logger.warning(err)

        return multi_edge

    def del_multi_edge(self, *nodes_keys):
        """
         Delete multi edge with 'nodes_keys'.

         :param nodes_keys: edge's _key.
         :type nodes_keys: Iterable[Hashable].
         :return: deleted multi edge.
         :rtype: set(_Edge) | None
         """

        multi_edge = self.get_multi_edge(*nodes_keys)

        try:
            (self.del_edge(edge.key) for edge in multi_edge)
        except TypeError as err:
            logger.warning(err)

        return multi_edge

    @property
    def nodes(self):
        """
        :return: graph's nodes.
        :rtype: Iterable[_Node]
        """

        return self._nodes.values()

    @property
    def edges(self):
        """
        :return: graph's edges.
        :rtype: Iterable[_Edge]
        """

        return self._edges.values()


class _Edge(_AttrObject):
    """
    classdocs
    """

    def __init__(self, nodes, multi_id=0, overwrite=False, nodes_attributes=None, **attributes):
        """
        Construct an edge using 'nodes'.

        From 'nodes', use _Node objects or create new ones from the remaining Hashable items to construct edge.
        Set edge's nodes attributes using 'nodes_attributes'.
        Existing nodes attributes will be overwritten.
        Set edge attributes using 'attributes'.
        Supports: hyper graph, _edges_multiplicity graph.

        :param nodes: edge's nodes.
        :type nodes: Iterable[_Node | Hashable]
        :invariant nodes: is not empty.
        :param overwrite: enable edge's nodes attribute overwriting.
        :type overwrite: bool
        :param nodes_attributes: edge's nodes attributes.
        :type nodes_attributes: Mapping.
        :param multi_id: edge's multiplicity identifier.
        :type multi_id: int
        :param attributes: edge's attributes.
        :type attributes: Mapping.
        """

        _AttrObject.__init__(self, **attributes)
        if not nodes:
            logger.exception("Non empty '_nodes' Iterable[_Node | Hashable] expected,"
                             " got {0}".format(type(nodes).__name__))
            raise TypeError("Non empty '_nodes' Iterable[_Node | Hashable] expected,"
                            " got {0}".format(type(nodes).__name__))

        self._multi_id = multi_id
        self._nodes = {node.key: node for node in filter(lambda node: isinstance(node, _Node), nodes)}

        if overwrite:
            self.set_nodes(attributes)

        try:
            self._nodes.update({node_key: _Node(node_key, **nodes_attributes) for node_key in
                                filter(lambda node: not isinstance(node, _Node), nodes)})
        except TypeError as err:
            self._nodes.update({node_key: _Node(node_key) for node_key in
                                filter(lambda node: not isinstance(node, _Node), nodes)})
            logger.debug(err)

        for node in self.nodes:
            node.add_edges(self)

    def __str__(self):
        return str(self.id)

    @property
    def key(self):
        """
        A _key is derived from the keys of edge's nodes.

        Another Hashable identifier is added to support MultiGraphs (a  parallel edge).
        :return: edge's _key.
        :rtype: Sequence[int, Hashable]
        """

        return self.multi_id, self.nodes_keys

    @property
    def multi_id(self):
        """
        :return: edge's multi_id serial nummber.
        :rtype: int
        """

        return self._multi_id

    @property
    def nodes(self):
        """
        :return: edge's nodes.
        :rtype: Iterable[_Node]
        """

        return self._nodes.values()

    @property
    def nodes_keys(self):
        """
        :return: edge's nodes keys.
        :rtype: Iterable[Hashable]
        """

        return frozenset(self._nodes.keys())

    @property
    def is_loop(self):
        """
        :return: True if is edge a loop, False otherwise.
        :rtype: bool
        """

        return True if len(self.nodes) == 1 else False

    def set_nodes(self, attributes):
        """
        Set edge's nodes using 'attributes'.

        :param attributes:
        :type attributes: Mapping
        :return: None
        """

        (node.set_attrs(**attributes) for node in self.nodes)


class _Node(_AttrObject):
    """
    classdocs
    """

    def __init__(self, key, **attributes):
        """
        Constructor

        :param key: node's _key.
        :type key: Hashable
        :param attributes: node's attributes.
        :type attributes: Mapping
        """

        if not isinstance(key, Hashable):
            logger.exception("Hashable 'key' expected, got {0}".format(type(key).__name__))
            raise TypeError("Hashable 'key' expected, got {0}".format(type(key).__name__))

        _AttrObject.__init__(self, **attributes)
        self._key = key
        self._edges = {}

    def __str__(self):
        return str(self.id)

    @property
    def key(self):
        """
        :return: node's key.
        :rtype: Hashable
        """

        return self._key

    @property
    def edges(self):
        """
        :return: node's edges.
        :rtype: Iterable[_Edge]
        """

        return self._edges.values()

    @property
    def edges_keys(self):
        """
        :return: node's edges keys.
        :rtype: Iterable[Iterable[Hashable]]
        """

        return self._edges.keys()

    @property
    def degree(self):
        """
        :invariant: degree >= 0
        :return: node's degree.
        :rtype: int
        """

        return len(self.edges) + sum(edge.is_loop for edge in self.edges)

    def add_edges(self, edges):
        """
        Add 'edges' to node's edges.

        :param edges: edge to be attached.
        :type edges: Iterable[_Edge] | _Edge
        :return: None
        """

        try:
            self._edges.update({edge.key: edge for edge in edges})
        except TypeError:
            try:
                self._edges[edges.key] = edges
            except (TypeError, AttributeError) as err:
                logger.warning(err)
            except KeyError as err:
                logger.debug(err)
        except AttributeError as err:
            logger.warning(err)

    def set_edges(self, edges, attributes):
        """
        Set 'edges' using 'attributes'.

        :param edges: set edges.
        :type edges: Iterable[_Edge] | _Edge
        :param attributes: edge's attributes
        :type attributes: Mapping
        """

        try:
            (self._edges[edge.key].set_attrs(attributes) for edge in edges)
        except TypeError:
            try:
                self._edges[edges.key].set_attrs(attributes)
            except (TypeError, AttributeError) as err:
                logger.warning(err)
            except KeyError as err:
                logger.debug(err)
        except AttributeError as err:
            logger.warning(err)
        except KeyError as err:
            logger.debug(err)

    def del_edges(self, edges):
        """
        Delete node's 'edges'.

        :param edges: edge's _key.
        :type edges: Iterable[_Edge] | _Edge
        :return: None.
        """

        try:
            for edge in edges:
                del self._edges[edge.key]
        except TypeError:
            try:
                del self._edges[edges.key]
            except (TypeError, AttributeError) as err:
                logger.warning(err)
            except KeyError as err:
                logger.debug(err)
        except AttributeError as err:
            logger.warning(err)
        except KeyError as err:
            logger.debug(err)