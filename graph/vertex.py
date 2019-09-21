class Vertex:
    """Класс вершиный содержит её имя и координаты"""
    def __init__(self, name: str, x: int, y: int):
        self.y = y
        self.x = x
        self.name = name

    def to_dict(self):
        return self.__dict__
