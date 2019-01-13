from metro import Graph
from train import Train


class Algo(Graph):
    def __init__(self):
        super().__init__()

    def process_path(self):
        def is_conflicted(path1, path2):
            intersects = list(set(path1).intersection(path2))
            tmp = path1[::-1]
            intersects.remove(self.start_node)
            intersects.remove(self.end_node)
            if intersects:
                return True
            return False
        idx = 0
        while idx < len(self.all_path) - 1:
            idx_check = idx + 1
            while idx_check < len(self.all_path):
                if is_conflicted(self.all_path[idx], self.all_path[idx_check]):
                    self.all_path.pop(idx_check)
                    idx_check -= 1
                idx_check += 1
            idx += 1
        self.all_path.reverse()

    def set_path(self):
        for idx, train in enumerate(self.start_node.visited):
            set = False
            while self.all_path and not set:
                check_num = self.n_turns(self.all_path[-1])
                check_num += 2 * (len(self.start_node.visited) - idx - 1)
                if self.n_turns(self.all_path[0]) <= check_num:
                    train.path = self.all_path[0]
                    set = True
                else:
                    self.all_path.pop(0)


graph = Algo()
graph.create_nodes('delhi-metro-stations')
tmp = int(graph.trains)
graph.trains = []
for x in range(tmp):
    tmp = Train(graph.start_line, graph.end_line, 'T' + str(x + 1))
    graph.trains.append(tmp)
    graph.start_node.visited.append(tmp)
all_path = graph.find_all_path()
graph.process_path()
graph.set_path()
while len(graph.end_node.visited) < len(graph.trains):
    graph.run_train()
    graph.train_position()
    graph.print_pos()
