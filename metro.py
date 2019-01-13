from parselinestation import parseLineStations
from node import Node


class Graph:
    def __init__(self):
        self.nodes = None
        self.start_node = None
        self.end_node = None
        self.start_line = None
        self.end_line = None
        self.trains = None
        self.all_path = []
        self.position = []

    def create_nodes(self, file):
        all_stations = []
        metro, status, self.trains = parseLineStations(file)
        intersects = []
        for k in metro.keys():
            stations = []
            for name in metro[k]:
                if name.find("Conn") != -1:  # Transfer point
                    name = name[:name.find(':')]
                    # If a new intersect, append to stations and intersect list
                    if name not in [s.name for s in intersects]:
                        station = Node(name, {k: len(stations) + 1}, True)
                        stations.append(station)
                        intersects.append(station)
                        all_stations.append(station)
                    # If already in intersect list
                    else:
                        for idx, station in enumerate(intersects):
                            if station.name == name:
                                intersects[idx].line[k] = len(stations) + 1
                                stations.append(intersects[idx])
                else:
                    station = Node(name, {k: len(stations) + 1})
                    stations.append(station)
                    all_stations.append(station)
            for i in range(len(stations)):
                try:
                    if i:
                        stations[i].neighbors.append(stations[i-1])
                    stations[i].neighbors.append(stations[i+1])
                except IndexError:
                    pass
            if k == status['START'][0] and not self.start_node:
                self.start_node = stations[int(status['START'][1])-1]
            if k == status['END'][0] and not self.end_node:
                self.end_node = stations[int(status['END'][1])-1]
        self.nodes = all_stations
        self.start_line = status['START'][0]
        self.end_line = status['END'][0]

    def n_turns(self, path):
        length = 0
        for idx in range(1, len(path) - 1):
            if not any(i in path[idx - 1].line for i in path[idx + 1].line):
                length += 1
        return length + len(path) - 1

    def find_all_path(self):
        self.__find_all_path(self.start_node, self.end_node)
        self.all_path = sorted(self.all_path, key=lambda x: self.n_turns(x))

    def __find_all_path(self, current_node, end_node):
        if current_node == end_node:
            path = []
            path.append(end_node)
            while current_node != self.start_node:
                current_node = current_node.parent
                path.append(current_node)
            return path[::-1]
        for node in current_node.neighbors:
            opened_nodes = self.trace_back(current_node, self.start_node)
            if node not in opened_nodes:
                node.parent = current_node
                path = self.__find_all_path(node, end_node)
                if path:
                    self.all_path.append(path)

    def trace_back(self, current_node, target_node):
        path = []
        path.append(current_node)
        while current_node != target_node and current_node.parent is not None:
            current_node = current_node.parent
            path.append(current_node)
        return path

    def run_train(self):
        for train in self.trains:
            if len(train.path) > train.pos + 1:
                # stand in transfer point and need to transfer
                if train.current_line not in train.path[train.pos + 1].line:
                    train.transfer()
                else:
                    # go to the next station
                    if train.path[train.pos + 1].able:
                        if train.path[train.pos + 1] != self.end_node:
                            train.go_next()
                        else:
                            # next station is end node
                            if train.current_line == self.end_line:
                                train.go_next()
                            elif self.end_node.able:  # from another line
                                train.go_next()
                                self.end_node.able = False
            elif len(train.path) == train.pos + 1:
                if train.current_line != self.end_line:
                    train.current_line = self.end_line
                    self.end_node.able = True

    def train_position(self):
        self.position = []
        for train in self.trains:
            if train.path[train.pos].name not in [x[0] for x in self.position]:
                tmp = []
                tmp.append(train.path[train.pos].name)
                tmp.append(train.current_line)
                tmp.append(train.path[train.pos].line[train.current_line])
                tmp.append([train.name])
                self.position.append(tmp)
            else:
                name = train.path[train.pos].name
                pos = [x[0] for x in self.position].index(name)
                self.position[pos][3].append(train.name)

    def format_pos(self):
        position = []
        for idx, elem in enumerate(self.position):
            string = elem[0] + '(' + elem[1] + ', ' + str(elem[2]) + ')'
            string += '-' + ','.join(elem[3])
            position.append(string)
        return '|'.join(position)

    def print_pos(self):
        print(self.format_pos())
