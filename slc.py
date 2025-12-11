"""Single linkage clustering using Kruskal's algorithm."""


# Copied from dsf.py so this file is self contained.
class DisjointSetForest:
    def __init__(self, elements):
        self._core = _DisjointSetForestCore()

        self.element_to_id = {}
        self.id_to_element = {}

        for element in elements:
            eid = self._core.make_set()
            self.element_to_id[element] = eid
            self.id_to_element[eid] = element

    def find_set(self, element):
        """Finds the representative of the set containing the element."""
        return self.id_to_element[
            self._core.find_set(
                self.element_to_id[element]
            )
        ]

    def union(self, x, y):
        """Unions the set containing `x` with the set containing `y`."""
        x_id = self.element_to_id[x]
        y_id = self.element_to_id[y]
        self._core.union(x_id, y_id)

    def in_same_set(self, x, y):
        """Determines if elements x and y are in the same set."""
        return self.find_set(x) == self.find_set(y)


class _DisjointSetForestCore:
    def __init__(self):
        self._parent = []
        self._rank = []
        self._size_of_set = []

    def make_set(self):
        x = len(self._parent)
        self._parent.append(None)
        self._rank.append(0)
        self._size_of_set.append(1)
        return x

    def find_set(self, x):
        try:
            parent = self._parent[x]
        except IndexError:
            raise ValueError(f"{x} is not in the collection.")

        if parent is None:
            return x
        root = self.find_set(parent)
        self._parent[x] = root
        return root

    def union(self, x, y):
        x_rep = self.find_set(x)
        y_rep = self.find_set(y)

        if x_rep == y_rep:
            return

        if self._rank[x_rep] > self._rank[y_rep]:
            self._parent[y_rep] = x_rep
            self._size_of_set[x_rep] += self._size_of_set[y_rep]
        else:
            self._parent[x_rep] = y_rep
            self._size_of_set[y_rep] += self._size_of_set[x_rep]
            if self._rank[x_rep] == self._rank[y_rep]:
                self._rank[y_rep] += 1


def _to_iterable(value):
    if value is None:
        return []
    if isinstance(value, dict):
        return value.keys()
    if isinstance(value, (set, list, tuple)):
        return value
    try:
        iter(value)
        return value
    except TypeError:
        return [value]


def _get_nodes(graph):
    for attr in ("get_nodes", "nodes", "vertices", "get_vertices", "all_nodes"):
        if hasattr(graph, attr):
            obj = getattr(graph, attr)
            try:
                nodes = obj() if callable(obj) else obj
            except TypeError:
                continue
            return list(_to_iterable(nodes))
    for adj_name in ("adj", "adjacency", "_adj", "_neighbors"):
        if hasattr(graph, adj_name):
            adj = getattr(graph, adj_name)
            if isinstance(adj, dict):
                return list(adj.keys())
    return []


def _neighbors(graph, node):
    for meth in (
        "get_neighbors",
        "neighbors",
        "adjacent",
        "neighbors_of",
        "get_adjacent_nodes",
    ):
        if hasattr(graph, meth):
            obj = getattr(graph, meth)
            try:
                nbrs = obj(node) if callable(obj) else obj.get(node) if isinstance(obj, dict) else None
            except TypeError:
                continue
            if nbrs is not None:
                return list(_to_iterable(nbrs))
    for adj_name in ("adj", "adjacency", "_adj", "_neighbors"):
        if hasattr(graph, adj_name):
            adj = getattr(graph, adj_name)
            if isinstance(adj, dict) and node in adj:
                return list(_to_iterable(adj[node]))
    return []


def _get_edges(graph):
    for attr in ("get_edges", "edges", "all_edges"):
        if hasattr(graph, attr):
            obj = getattr(graph, attr)
            try:
                edges_obj = obj() if callable(obj) else obj
            except TypeError:
                edges_obj = None
            if edges_obj is not None:
                normalized: Set[Tuple[Any, Any]] = set()
                for edge in _to_iterable(edges_obj):
                    if not isinstance(edge, (list, tuple)) or len(edge) < 2:
                        continue
                    u, v = edge[0], edge[1]
                    if u == v:
                        continue
                    a, b = sorted((u, v))
                    normalized.add((a, b))
                if normalized:
                    return list(normalized)

    edges = set()
    nodes = _get_nodes(graph)
    for u in nodes:
        for v in _neighbors(graph, u):
            if u == v:
                continue
            a, b = sorted((u, v))
            edges.add((a, b))
    return list(edges)


def slc(
    graph,
    d,
    k
):
    """
    Perform single linkage clustering using Kruskal's algorithm.

    Parameters
    ----------
    graph : dsc40graph.UndirectedGraph
        Input undirected graph.
    d : Callable[[Tuple[Any, Any]], float]
        Distance function taking a tuple (u, v) and returning a weight.
    k : int
        Desired number of clusters (must be positive and at most number of nodes).
    """
    nodes = _get_nodes(graph)
    if not nodes:
        return frozenset()
    if k < 1:
        raise ValueError("k must be positive.")
    if k > len(nodes):
        raise ValueError("k cannot exceed number of nodes.")

    edges = _get_edges(graph)
    if not edges and k != len(nodes):
        raise ValueError("Cannot form requested clusters without edges.")

    forest = DisjointSetForest(nodes)
    # Sort edges by weight; normalize ordering so d can rely on consistent tuples.
    edges_sorted = sorted(edges, key=lambda e: d(tuple(sorted(e))))

    clusters = len(nodes)
    for u, v in edges_sorted:
        if clusters <= k:
            break
        if not forest.in_same_set(u, v):
            forest.union(u, v)
            clusters -= 1

    if clusters > k:
        raise ValueError("Graph does not have enough connectivity to form k clusters.")

    comps = {}
    for node in nodes:
        rep = forest.find_set(node)
        comps.setdefault(rep, set()).add(node)

    return frozenset(frozenset(comp) for comp in comps.values())


__all__ = ["slc", "DisjointSetForest"]

