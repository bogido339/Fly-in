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
    
    def is_move_valid(self, drone: Drone, target) -> bool:
        return True

    def tick(self) -> None:
        turn_moves = []

        for drone in self.drones:
            if drone.current_location == self.graph.end_zone:
                continue
            if drone.destination.__class__.__name__ == "Zone":
                if (self.is_move_valid(drone, drone.destination)
                    and drone.destination.current_drones < drone.destination.capacity):
                    
                    drone.current_location.current_drones -= 1
                    
                    drone.move_to_next()
                    
                    turn_moves.append(f"D{drone.drone_id}-{drone.current_location.name}")
                    drone.destination.current_drones += 1
                    drone.get_destination()
                    
                else:
                    pass
            else:
                drone.move_to_next()
                drone.get_destination()


        if turn_moves:
            print(" ".join(turn_moves))
        
        self.turn_count += 1

    def run(self) -> None:
        if not self.is_finished():
            self.tick()
        elif self.is_fist_own:
            self.is_fist_own = False
            print(f"Simulation finished in {self.turn_count} turns.")
