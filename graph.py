from connections import Connection

class Graph:
    def __init__(self):
        self.nb_drones = 0
        self.zones = {}
        self.connections = {}
        self.start_zone = None
        self.end_zone = None
        self.path = None
        

    def add_zone(self, zone):
        if zone.name == "start":
            self.start_zone = zone
        elif zone.name == "goal":
            self.end_zone = zone

        self.zones.update({zone.name: zone})

    def add_connections(self, zone1, zone2):
        connection = Connection(zone1, zone2)
        self.connections.update({(zone1.name, zone2.name): connection})

        zone1.neighbors.append(zone2)
        zone2.neighbors.append(zone1)

        return connection

    def get_zone(self, name):
        return self.zones.get(name, None)

    def get_neighbors(self, zone):
        return list(zone.neighbors)
    
    def get_connection(self, zone1, zone2):
        return self.connections[(zone1.name, zone2.name)]
