class Drone:
    def __init__(self, drone_id, path, graph):
        self.drone_id = drone_id

        self.graph = graph

        self.current_location = None

        self.path = iter(path)

        self.destination = None

        self.path_index = 0

    def is_in_zone(self):
        return self.current_location.__class__.__name__ == "Zone"

    def is_in_connection(self):
        return self.current_location.__class__.__name__ == "Connection"
    
    def get_destination(self):
        if self.is_in_zone():
            self.current_location.current_drones -= 1
            _next = next(self.path, None)
            if _next and _next.type == "restricted":
                self.destination = self.graph.get_connection(self.current_location, _next)
            else:
                self.destination = _next
                
        elif self.is_in_connection():
            self.destination = self.current_location.end


    def move(self):
        self.current_location = self.destination
        if self.current_location and self.is_in_zone():
            self.current_location.current_drones += 1
        
        
        

    # def get_next_target_from_path(self):
    #     if self.path_index < len(self.path) - 1:
    #         return self.path[self.path_index + 1]
        
    #     return None
        
    # def advance_path(self) -> None:
    #     if self.path_index < len(self.path) - 1:
    #         self.path_index += 1

    # def update_turn(self):
    #     if self.remaining_turns > 0:
    #         self.remaining_turns -= 1

    #         if self.remaining_turns == 0:
    #             self.current_location = self.destination
    #             self.destination = None

    # def __str__(self):
    #     return f"{self.drone_id}"
    
