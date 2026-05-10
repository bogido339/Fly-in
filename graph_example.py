class Zone:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Connection:
    def __init__(self, start: Zone, end: Zone) ->None:
        self.start = start
        self.end = end

    def __repr__(self):
        return f"{self.start.name} <-> {self.end.name}"


class Graph:
    def __init__(self):
        self.zones = {}
        self.connections = {}

    def add_zone(self, zone):
        self.zones[zone.name] = zone
        self.connections[zone.name] = []

    def add_connection(self, zone1, zone2):
        connection = Connection(zone1, zone2)

        self.connections[zone1.name].append(connection)
        self.connections[zone2.name].append(connection)

    def get_neighbors(self, zone):
        neighbors = []

        for connection in self.connections[zone.name]:
            if connection.start == zone:
                neighbors.append(connection.end)
            else:
                neighbors.append(connection.start)

        return neighbors

    def show(self):
        for zone_name in self.connections:
            print(zone_name, "->", self.get_neighbors(self.zones[zone_name]))


# -------------------
# Example usage
# -------------------

graph = Graph()

start = Zone("start")
a = Zone("A")
b = Zone("B")
goal = Zone("goal")

graph.add_zone(start)
graph.add_zone(a)
graph.add_zone(b)
graph.add_zone(goal)

graph.add_connection(start, a)
graph.add_connection(a, b)
graph.add_connection(b, goal)
print(graph.__dict__)
# graph.show()