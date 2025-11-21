from typing import Any, Dict, Set


def biggest_descendent(graph: Any, root: Any, value: Dict[Any, Any]) -> Dict[Any, Any]:
    nodes = list(graph.nodes) if hasattr(graph, "nodes") else []
    if not nodes:
        return {}

    memo: Dict[Any, Any] = {}
    visiting: Set[Any] = set()

    def dfs(node: Any) -> Any:
        if node in memo:
            return memo[node]
        if node in visiting:
            return value[node]
        visiting.add(node)
        best = value[node]
        for child in graph.neighbors(node):
            child_val = dfs(child)
            if child_val > best:
                best = child_val
        visiting.remove(node)
        memo[node] = best
        return best

    if root in value:
        dfs(root)
    for node in nodes:
        dfs(node)
    return memo
