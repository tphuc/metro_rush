class Graph:
    def __init__(self, graph_dict=None):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.graph_dict = graph_dict

    def find_path(self, start, goal, path=[]):
        graph = self.graph_dict
        path = path + [start]
        if start == goal:
            return path
        if start not in graph:
            return None
        for node in graph[start]:
            if node not in path:
                new_path = self.find_path(node, goal, path)
                if new_path: return new_path
        return None

    def find_all_paths(self, start, goal, path=[]):
        graph = self.graph_dict
        path = path + [start]
        if start == goal:
            return [path]
        if start not in graph:
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                extended_paths = self.find_all_paths(node, goal, path)
                for p in extended_paths:
                    paths.append(p)
        return sorted(paths)
