class Zone:
    def __init__(self):
        self.name = None
        self.location = None
        self.type = None
        self.capacity = 1
        self.color = None
        self.neighbors = []
        self.cost = 1
        self.current_drones = 0

    def zone_capacity(self, drones_leaving=0):

       res = self.current_drones - drones_leaving
       return res < self.capacity
