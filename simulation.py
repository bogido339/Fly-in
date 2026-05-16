from typing import List
from drone import Drone
import random

class Simulator:
    def __init__(self, graph):

        self.graph = graph
        self.drones = []
        self.turn_count = 0

    def create_drons(self):
        for dron_id in range(1, self.graph.nb_drones + 1):
            drone = Drone(dron_id, self.graph.path)
            drone.current_location = self.graph.start_zone
            drone.destination = self.graph.path[1]
            self.drones.append(drone)
        

    def is_finished(self) -> bool:

        for drone in self.drones:
            if drone.current_location != self.graph.end_zone:
                return False
        return True

    def is_move_valid(self, drone: Drone, target) -> bool:
            return True

    def tick(self) -> None:
        # turn_moves = []

        for drone in self.drones:
            if drone.current_location == self.graph.end_zone:
                continue

            next_target = drone.get_next_target_from_path() 

            if self.is_move_valid(drone, next_target):
                
                drone.move_to(next_target)
                drone.advance_path()
                
                # turn_moves.append(f"{drone.drone_id}-{next_target.name}")
            else:
                pass

        # if turn_moves:
        #     print(" ".join(turn_moves))
        
        self.turn_count += 1

    
    
    def run(self) -> None:
        while not self.is_finished():
            self.tick()
        
        print(f"Simulation finished in {self.turn_count} turns.")