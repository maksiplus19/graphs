from typing import Callable, Dict, Optional

from graph.graph import Graph


def minus(l, r):
    if l:
        return False if r else True
    return False


class Operation:
    operation: Dict[str, Callable[[bool, bool], bool]] = {
        'and': lambda left, right: left and right,
        'or': lambda left, right: left or right,
        'xor': lambda left, right: left != right,
        'minus': minus,
        'eq': lambda left, right: left == right,
        'impl': lambda left, right: (not left) or right,
        'coimpl': lambda left, right: not ((not left) or right),
        'sheph': lambda left, right: not (left and right),
        'pirs': lambda left, right: not (left or right)
    }

    def __init__(self, op: str):
        self.op = op

    def __call__(self, left: bool, right: bool) -> bool:
        return self.operation[self.op](left, right)


def binary_operation(a: Graph, b: Graph, op: str) -> Optional[Graph]:
    if a.size() != b.size():
        return None
    if a.size() < b.size():
        a, b = b, a
    size = a.size()
    g = [[0 for i in range(size)] for i in range(size)]
    operation = Operation(op)
    a = a.to_matrix()
    b = b.to_matrix()

    for i in range(size):
        for j in range(size):
            if i == j:
                continue
            g[i][j] = int(operation(a[i][j], b[i][j]))

    return Graph.from_matrix(g)
