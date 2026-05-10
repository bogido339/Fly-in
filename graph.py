from connections import Connection

class Graph:
    def __init__(self):
        self.zones = {}
        self.connections = []
        self.start_zone = None
        self.end_zone = None
        self.nb_drones = 0

    def add_zone(self, zone):
        if zone.name == "start":
            self.start_zone = zone
        elif zone.name == "goal":
            self.end_zone = zone

        self.zones.update({zone.name: zone})

    def add_connections(self, zone1, zone2):
        connection = Connection(zone1, zone2)
        self.connections.append(connection)

# def add_connection(self, zone1, zone2):

#     connection = Connection(zone1, zone2)

#     self.connections.append(connection)

#     zone1.neighbors.append(zone2)
#     zone2.neighbors.append(zone1)

    def get_zone(self, name):
        return self.zones.get(name)

    def get_neighbors(self, zone):
        return list(zone.neighbors)
