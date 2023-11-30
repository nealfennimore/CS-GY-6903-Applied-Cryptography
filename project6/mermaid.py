from abc import ABC, abstractmethod
from base64 import b64encode
from typing import Any, Callable, List, Optional

from IPython.core.display import Image, Markdown, display


class Node(ABC):
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    parent: Optional["Node"] = None
    _value: Optional[str] = None

    @abstractmethod
    def value(self) -> Any:
        pass


class Output(str):
    def to_markdown(self) -> Markdown:
        return display(
            Markdown(
                f"""```mermaid
{self}
```"""
            )
        )

    def to_url(self) -> str:
        graphbytes = self.encode("utf8")
        base64_bytes = b64encode(graphbytes)
        base64_string = base64_bytes.decode("ascii")
        return "https://mermaid.ink/img/" + base64_string

    def to_image(self) -> Image:
        return display(Image(url=self.to_url()))


def formatter(node: Node, prefix: str) -> str:
    original_value = f" '{node._value}'" if node._value is not None else "B"
    return f"{prefix}[{node.value}{original_value}]"


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
        formatter=formatter,
        classDefs: str = "",
    ):
        assert node is not None

        paths = []
        Mermaid.in_order_traversal(node, formatter, paths)
        paths = Mermaid.reduce_paths(paths)
        paths = "\n".join(paths)

        return Output(
            f"""
flowchart TD
{classDefs}
{paths}
"""
        )
