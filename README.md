# Графоид
## Формат файла
### Список смежности

Вершина пробел вершина

Например, `1 2 1 5 10`, т.е. вершина `1` смежна с вершинами `2` и весом 1 и вершиной `5` с весом 10

## Файлы
Название файла  | Содержание
---|---
`window.py`     | основной файл окна
`design.py`     | файл с разметкой окна
`convert bat`   | запускает команду для преобразования `design.ui` в `design.py`
`qgraphview.py` | класс для отображения графа

## QGraphView

Класс наследованный от `QGraphicsView` для отображения графа

Поскольку QtDesigner не знает где находится реализация класса QGraphView, то после каждого запуска `convert.bat` 
нужно заменить строку `from qgraphview import QGraphView` на `from ui.sourse.qgraphview import QGraphView`
