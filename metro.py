from parseline import parseLineStations

class Node:
    def __init__(self, name, line, x=0, y=0, intersect=False):
        self.name = name
        self.x = x
        self.y = y
        self.line = line
        self.neighbors = []
        self.parent = None
        self.intersect = intersect


class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.start_node = None
        self.end_node = None
        self.all_path = []

    def find_all_path(self, current_node, end_node, sort=True):
        self.start_node = current_node
        self.end_node = end_node
        self._find_all_path(current_node, end_node)
        if sort:
            return sorted(self.all_path, key=lambda x: len(x))
        return self.all_path

    def _find_all_path(self, current_node, end_node):
        if current_node == end_node :
            path = []
            while current_node != self.start_node:
                path.append(current_node)
                current_node = current_node.parent
            return path[::-1]

        """ return the list of path """
        # opened_nodes = opened_nodes
        # opened_nodes.append(current_node)

        for node in current_node.neighbors:
            opened_nodes = self.trace_back(current_node, self.start_node)
            if node not in opened_nodes:
                node.parent = current_node
                path = self._find_all_path(node, end_node)
                if path:
                    self.all_path.append(path)

    def trace_back(self, current_node, target_node):
        path = []
        path.append(current_node)
        while current_node != target_node and current_node.parent is not None:
            current_node = current_node.parent
            path.append(current_node)
        return path

    def route_cost(self, nodes):
        cost = len(nodes)
        for i in range(1, cost-1):
            if nodes[i-1].line != nodes[i+1].line and nodes[i].intersect:
                cost += 1
        return cost

def create_nodes(file):
    all_stations = []
    metro = parseLineStations(file)
    intersects = []
    for k in metro.keys():
        stations = []
        for name in metro[k]:
            if name.find("Conn") != -1: # Transfer point
                name = name[:name.find(':')]
                # If a new intersect, append to both stations and intersect list
                if name not in [s.name for s in intersects]:
                    station = Node(name, k, intersect=True)
                    stations.append(station)
                    intersects.append(station)
                    all_stations.append(station)
                # If already in intersect list
                else:
                    for station in intersects:
                        if station.name == name:
                            stations.append(station)
            else:
                station = Node(name, k)
                stations.append(station)
                all_stations.append(station)
        for i in range(0,len(stations)):
            try:
                if i:
                    stations[i].neighbors.append(stations[i-1])
                stations[i].neighbors.append(stations[i+1])
            except IndexError:
                pass
    return all_stations




nodes = create_nodes('delhi-metro-stations')
graph = Graph(nodes)

all_path = graph.find_all_path(graph.nodes[14], graph.nodes[21])

for route in all_path:
    print([node.name for node in route])
