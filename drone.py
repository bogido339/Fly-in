class Drone:
    def __init__(self, drone_id, path):
        self.drone_id = drone_id

        self.current_location = None

        self.path = path

        self.destination = None

        self.path_index = 0

    def is_in_zone(self):
        return self.current_location.__class__.__name__ == "Zone"

    def is_in_connection(self):
        return self.current_location.__class__.__name__ == "Connection"
    
    def get_next_target_from_path(self):
        index = self.path.index(self.destination)
        if index < 24:
            return self.path[index + 1]
        return []

    def move_to(self, destination):
        self.destination = destination

    def get_next_target_from_path(self):
        if self.path_index < len(self.path) - 1:
            return self.path[self.path_index + 1]
        
        return None
        
    def advance_path(self) -> None:
        if self.path_index < len(self.path) - 1:
            self.path_index += 1

    def update_turn(self):
        if self.remaining_turns > 0:
            self.remaining_turns -= 1

            if self.remaining_turns == 0:
                self.current_location = self.destination
                self.destination = None

    def __str__(self):
        return f"{self.drone_id}"
    
