# класс графа
class Graph:
    def __init__(self):
        # граф хранится в виде списк смежности
        self.adjacency_list = {}

    def load_from_adjacency_list(self, file_name: str):
        with open(file_name, mode='r') as file:
            # построчное чтение файла
            for line in file:
                # убираем комментарии
                line = line.split('%', maxsplit=2)[0]
                # разделяем строку на номера вершин
                vertices = line.split(' ')
                if len(vertices) == 0:
                    continue
                # сохраняем первую и создаем для нее список
                v = int(vertices[0])
                self.adjacency_list[v] = []
                # добавляем смежные вершины
                for i in range(1, len(vertices)):
                    self.adjacency_list[v].append(int(vertices[i]))
