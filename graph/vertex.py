class Vertex:
    """Класс вершиный содержит её имя и координаты"""
    def __init__(self, name: str, x: float, y: float):
        self.y = y
        self.x = x
        self.name = name
        self.color = None

    def to_dict(self):
        return self.__dict__
