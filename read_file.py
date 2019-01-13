from node import Node

class GenerateFile:
    def __init__(self, filename):
        self.file = filename
        self.nodes = None
        self.start_node = None
        self.end_node = None
        self.start_line = None
        self.end_line = None
        self.trains = None

    def parseLineStations(self):
        metrodict = {}
        status = {}
        n = 0
        color = None
        with open(self.file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    if line.startswith('#'):
                        metrodict.setdefault(line[1:], [])
                        color = line[1:]
                    elif line[0].isdigit():
                        metrodict[color].append(line[line.find(':')+1:])
                    elif line.startswith("START"):
                        status.setdefault('START', line[line.find('=')+1:].split(':'))
                    elif line.startswith("END"):
                        status.setdefault('END', line[line.find('=')+1:].split(':'))
                    elif line.startswith("TRAINS"):
                        n = int(line[line.find('=')+1:])
        return metrodict, status, n

    def create_nodes(self):
        all_stations = []
        metro, status, self.trains  = self.parseLineStations()
        intersects = []
        for k in metro.keys():
            stations = []
            for name in metro[k]:
                if name.find("Conn") != -1: # Transfer point
                    name = name[:name.find(':')]
                    # If a new intersect, append to both stations and intersect list
                    if name not in [s.name for s in intersects]:
                        station = Node(name, {k: len(stations) + 1}, intersect=True)
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
                    station = Node(name, [k])
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
        return all_stations


    def create_dict(self):
        all_node = self.create_nodes()
        dic = {}
        for n in all_node:
            dic[n.name] = [i.name for i in n.neighbors]
        return dic
