from graph.vertex import Vertex


class Graph:
    """Класс графа"""
    def __init__(self):
        # Граф хранится в виде словаря.
        # Каждой вершине соответсвуеет словарь вершин,
        # до которых есть дуги и список их весов
        # vertexes = dict(name, dict(name, list))
        self.vertexes = {}
        # vertexes_coordinates = dict(name, Vertex)
        self.vertexes_coordinates = {}

    def add_edge(self, v_from: str, v_to: str, weight: int = 1):
        if self.vertexes.get(v_from) is not None and self.vertexes.get(v_to) is not None:
            self.vertexes[v_from][v_to].append(weight)
            self.vertexes[v_from][v_to].sort()
        else:
            raise Exception('No vertex for adding edge')

    def add_vertex(self, name: str, x: int, y: int):
        if self.vertexes_coordinates.get(name) is None:
            self.vertexes_coordinates[name] = Vertex(name, x, y)
            self.vertexes[name] = {}

    def del_edge(self, v_from: str, v_to: str, weight: int):
        if self.vertexes.get(v_from) is not None and self.vertexes.get(v_to) is not None:
            arr = self.vertexes[v_from][v_to]
            arr.pop(arr.index(weight))

    def del_vertex(self, name: str):
        if self.vertexes_coordinates.get(name):
            self.vertexes_coordinates.pop(name)
            self.vertexes.pop(name)
            for item in self.vertexes.values():
                if name in item:
                    item.pop(name)

    def clear(self):
        self.vertexes.clear()
        self.vertexes_coordinates.clear()

    def undo(self):
        pass

    def next(self):
        pass

    def save_state(self):
        pass
