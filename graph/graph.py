class Graph:
    """Класс графа"""
    def __init__(self):
        # граф хранится в виде словаря.
        # Каждой вершине соответсвуеет словарь вершин,
        # до которых есть дуги и список их весов
        # vertexes = dict(name, dict(name, list))
        self.vertexes = {}

    def add_edge(self, v_from: str, v_to: str, weight: int = 1):
        pass

    def add_vertex(self, name: str, x: int, y: float):
        pass

    def del_edge(self, v_from: str, v_to: str, weight: int):
        pass

    def del_vertex(self):
        pass

    def clear(self):
        self.vertexes.clear()
