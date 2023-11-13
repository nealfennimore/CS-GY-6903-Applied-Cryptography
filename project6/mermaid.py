from typing import Any, Callable, List, Optional


class Node:
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    parent: Optional["Node"] = None
    _value: Optional[str] = None


class Mermaid:
    @staticmethod
    def in_order_traversal(
        node: Optional[Node],
        formatter: Callable[[Any, str], str],
        paths: List[str],
        path: str = "",
        prefix="_ROOT",
        level=0,
    ):
        if node is not None:
            path = (
                f"{path} --> {formatter(node, prefix)}"
                if path != ""
                else formatter(node, prefix)
            )
            Mermaid.in_order_traversal(
                node.left, formatter, paths, path, f"{prefix}-L{level + 1}", level + 1
            )
            paths.append(path)
            Mermaid.in_order_traversal(
                node.right, formatter, paths, path, f"{prefix}-R{level + 1}", level + 1
            )

    @staticmethod
    def reduce_paths(paths: List[str]):
        container = [path.split(" --> ") for path in sorted(paths)]

        for idx in range(len(container) - 1):
            curr = container[idx]

            for j_idx in range(idx + 1, len(container)):
                nxt = container[j_idx]

                s = 0
                while s < len(curr) and s < len(nxt) and curr[s] == nxt[s]:
                    s += 1

                if s > 0:
                    container[j_idx] = nxt[s - 1 :]

        return [" --> ".join(path) for path in container]

    @staticmethod
    def render_binary_search_tree(
        node: Node,
        formatter=lambda node, prefix: f"{prefix}[{node.value}]",
        classDefs: str = "",
    ):
        assert node is not None

        paths = []
        Mermaid.in_order_traversal(node, formatter, paths)
        paths = Mermaid.reduce_paths(paths)
        paths = "\n".join(paths)

        return f"""
```mermaid
flowchart TD
{classDefs}
{paths}
```
"""
