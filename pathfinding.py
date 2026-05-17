import heapq
import sys


class PathfinderError(Exception):
    pass


class PathFider():
    def __init__(self, graph):
        self.graph = graph
        self.start_zone = graph.start_zone
        self.end_zone = graph.end_zone

    def find_shortest_path(self):
        pq = []

        path = {zone: None for zone in self.graph.zones.values()}
        dist = {zone: sys.maxsize for zone in self.graph.zones.values()}

        dist[self.start_zone] = 0

        heapq.heappush(pq, (0, id(self.start_zone), self.start_zone))

        while pq:
            zone_cost, _, zone = heapq.heappop(pq)

            if zone_cost > dist[zone]:
                continue

            if zone == self.end_zone:
                break

            for neighbor in zone.neighbors:
                new_cost = zone_cost + neighbor.cost
                
                if new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    path[neighbor] = zone
                    heapq.heappush(pq, (new_cost, id(neighbor), neighbor))

        zone = self.end_zone
        path_list = []
        
        if path.get(zone) is None and zone != self.start_zone:
            raise PathfinderError("The route to the final point could not be found.")

        while zone:
            path_list.append(zone)
            zone = path.get(zone)
            
        path_list.reverse()

        return path_list