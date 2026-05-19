class Drone:
    def __init__(self, drone_id, path, graph):
        self.drone_id = drone_id
        self.graph = graph

        self.path = path
        self.path_index = 0

        self.current_location = path[0] if path else None
        self.destination = None

    def is_in_zone(self):
        return self.current_location.__class__.__name__ == "Zone"

    def is_in_connection(self):
        return self.current_location.__class__.__name__ == "Connection"

    def has_next_location(self):
        return self.path_index + 1 < len(self.path)

    def get_destination(self):
        if not self.has_next_location():
            self.destination = None
            return None

        if self.is_in_zone():
            next_location = self.path[self.path_index + 1]
            
            if next_location.type == "restricted":
                self.destination = self.graph.get_connection(
                    self.current_location,
                    next_location
                )
            else:
                self.destination = next_location
        else:
            self.destination = self.current_location.end

        return self.destination

    def move(self):
        if self.destination is None:
            return
        
        print(f"current_locatine the {self.current_location.name} is {self.current_location.current_drones}")

        if self.current_location.current_drones <= self.current_location.capacity:
            self.current_location.current_drones -= 1

        self.current_location = self.destination

        if self.is_in_zone():
            self.path_index += 1
        
        self.current_location.current_drones += 1