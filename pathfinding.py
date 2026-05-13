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

        heapq.heappush(pq, (0, self.start_zone))

        while pq:

            zone_cost, zone = heapq.heappop(pq)

            if zone_cost > dist[zone]:
                continue

            for neighbor in zone.neighbors:
                if neighbor.cost + zone_cost < dist[neighbor]:
                    dist[neighbor] = neighbor.cost + zone_cost
                    heapq.heappush(pq, (dist[neighbor], neighbor))
                    path[neighbor] = zone

        zone = self.end_zone
        path_list = []
        while path[zone]:
            path_list.append(path[zone])
            zone = path[zone]
            


        return path_list