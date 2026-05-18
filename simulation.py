from typing import List
from drone import Drone


class Simulator:
    def __init__(self, graph):
        self.graph = graph
        self.drones = []
        self.turn_count = 0
        self.is_fist_own = True

    def create_drons(self):
        for i in range(1, self.graph.nb_drones + 1):
            drone = Drone(i, self.graph.path, self.graph)
            drone.current_location = next(drone.path)
            drone.get_destination()
            self.drones.append(drone)

    def is_finished(self) -> bool:

        for drone in self.drones:
            if drone.current_location != self.graph.end_zone:
                return False
        return True
    
    def is_next_move_valid(self, drone: Drone) -> bool:
        if drone.destination and drone.destination.__class__.__name__ == "Zone":
            print("type the destination:",drone.destination.__class__.__name__)
            if drone.current_location.capacity > drone.destination.current_drones:
                return True
            else:
                return False
        else:
            return True
        
    def is_next_move_valid(self, drone: Drone) -> bool:
        if drone.destination and drone.destination.__class__.__name__ == "Zone":

            print("type the destination:", drone.destination.__class__.__name__)

            if drone.destination.capacity > drone.destination.current_drones:
                return True
            else:
                return False

        return True

    def tick(self) -> None:
        turn_moves = []

        for drone in self.drones:
            print(f"drone_id {drone.drone_id} current location: {drone.current_location}")
            if drone.current_location == self.graph.end_zone:
                continue

            drone.get_destination()

            if self.is_next_move_valid(drone):
                drone.move()
            else:
                pass

        if turn_moves:
            print(" ".join(turn_moves))
        
        self.turn_count += 1

    def run(self) -> None:
        if not self.is_finished():
            self.tick()
        elif self.is_fist_own:
            self.is_fist_own = False
            print(f"Simulation finished in {self.turn_count} turns.")
