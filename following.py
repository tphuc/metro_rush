from metro import Graph
from train import Train
import sys
from visualizer import run, runtime_file

class Following(Graph):
    def __init__(self):
        super().__init__()

    def set_path(self):
        for train in self.start_node.visited:
            train.path = self.all_path[0]

graph = Following()
graph.create_nodes('delhi-metro-stations')
tmp = int(graph.trains)
graph.trains = []
for x in range(tmp):
    tmp = Train(graph.start_line, graph.end_line, 'T' + str(x + 1))
    graph.trains.append(tmp)
    graph.start_node.visited.append(tmp)
all_path = graph.find_all_path()
graph.set_path()
output = ""
while len(graph.end_node.visited) < len(graph.trains):
    graph.run_train()
    graph.train_position()
    output += graph.format_pos() + '\n'
    graph.print_pos()
with open(runtime_file,'w') as f:
    f.write(output.strip())

run('delhi-metro-stations')
