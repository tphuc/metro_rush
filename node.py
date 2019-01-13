class Node:
    def __init__(self, name, line, x=0, y=0, intersect=False):
        self.name = name
        self.x = x
        self.y = y
        self.line = line
        self.neighbors = []
        self.parent = None
        self.intersect = intersect
        self.visited = []
        self.able = True
