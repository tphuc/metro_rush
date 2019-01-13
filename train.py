class Train:
    def __init__(self, start_line, end_line, name):
        self.name = name
        self.path = []
        self.current_line = start_line
        self.end_line = end_line
        self.pos = 0

    def go_next(self):
        if len(self.path) > 1:
            self.path[self.pos].able = True
            self.path[self.pos].visited.remove(self)
            self.pos += 1
            self.path[self.pos].visited.append(self)
            if len(self.path) - 1 > self.pos:
                self.path[self.pos].able = False

    def transfer(self):
        tmp1 = self.path[self.pos].line
        tmp2 = self.path[self.pos + 1].line
        self.current_line = list(set(tmp1).intersection(tmp2))[0]
