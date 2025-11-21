from typing import Any, Callable, FrozenSet, Iterable, List, Set


def cluster(graph: Any, weights: Callable[[Any, Any], float], level: float) -> FrozenSet[FrozenSet[Any]]:
    nodes = list(graph.nodes) if hasattr(graph, "nodes") else []
    if not nodes:
        return frozenset()

    visited: Set[Any] = set()
    comps: List[FrozenSet[Any]] = []

    for start in nodes:
        if start in visited:
            continue
        stack = [start]
        visited.add(start)
        comp: Set[Any] = set()
        while stack:
            u = stack.pop()
            comp.add(u)
            for v in graph.neighbors(u):
                if weights(u, v) < level:
                    continue
                if v in visited:
                    continue
                visited.add(v)
                stack.append(v)
        comps.append(frozenset(comp))

    return frozenset(comps)


__all__ = ["cluster"]

