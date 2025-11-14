from collections import deque
from typing import Any, Dict, Optional


def assign_good_and_evil(graph: Any) -> Optional[Dict[Any, str]]:
    if hasattr(graph, "get_nodes"):
        nodes = graph.get_nodes()
    elif hasattr(graph, "nodes"):
        nodes_attr = graph.nodes
        nodes = nodes_attr() if callable(nodes_attr) else nodes_attr
    elif hasattr(graph, "vertices"):
        verts_attr = graph.vertices
        nodes = verts_attr() if callable(verts_attr) else verts_attr
    elif hasattr(graph, "adj"):
        nodes = list(graph.adj.keys())
    else:
        nodes = []
    if not nodes:
        return {}
    color: Dict[Any, str] = {}
    for start in nodes:
        if start in color:
            continue
        color[start] = "good"
        q = deque([start])
        while q:
            u = q.popleft()
            if hasattr(graph, "get_neighbors"):
                nbrs = graph.get_neighbors(u)
            elif hasattr(graph, "neighbors"):
                nbrs = graph.neighbors(u)
            elif hasattr(graph, "adj"):
                nbrs = graph.adj.get(u, [])
            else:
                nbrs = []
            for v in nbrs:
                if v not in color:
                    color[v] = "evil" if color[u] == "good" else "good"
                    q.append(v)
                else:
                    if color[v] == color[u]:
                        return None
    return color