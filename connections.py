class Connection:
    def __init__(self, zone1, zone2):
        self.start = zone1
        self.end = zone2
        self.capacity = 1
        self.current_drones = 0
        self.name = "connection"
