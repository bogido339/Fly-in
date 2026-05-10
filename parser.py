from graph import Graph
from dron import Dron
from zone import Zone
from connections import Connection

class MapParserError(Exception):
    pass

class MapParser:
    def parse_drones(self, line, graph):
        try:
            number = int(line.split(":")[1])
            # if number < 0:
            #     raise ValueError()
            graph.nb_drones = number
        except ValueError:
            raise MapParserError("Invalid 'nb_drones' value: expected an integer after ':'")

    def parse_start(self, line, graph):
        data = line.split(":")[1]

        # if not data:
        #     raise MapParserError(
        #         "Empty 'start_hub' line: expected 'start_hub: start x y metadata'"
        #     )

        parts = data.split()

        if len(parts) != 4:
            raise MapParserError(
                "Invalid 'start_hub' format: expected 4 values "
                "(name x y metadata)"
            )

        zone_name = parts[0]

        if zone_name != "start":
            raise MapParserError(
                "Invalid start hub name: expected 'start'"
            )

        try:
            x = int(parts[1])
            y = int(parts[2])
        except ValueError:
            raise MapParserError(
                "Invalid coordinates for 'start_hub': x and y must be integers"
            )

        zone = Zone()
        zone.name = zone_name
        zone.location = (x, y)

        graph.add_zone(zone)

    def parse_end(self, line, graph):
        data = line.split(":")[1].strip()

        # if not data:
        #     raise MapParserError(
        #         "Empty 'end_hub' line: expected 'end_hub: end x y metadata'"
        #     )

        parts = data.split()

        if len(parts) != 4:
            raise MapParserError(
                "Invalid 'end_hub' format: expected 4 values "
                "(name x y metadata)"
            )

        zone_name = parts[0]

        if zone_name != "goal":
            raise MapParserError(
                "Invalid end hub name: expected 'goal'"
            )

        try:
            x = int(parts[1])
            y = int(parts[2])
        except ValueError:
            raise MapParserError(
                "Invalid coordinates for 'end_hub': x and y must be integers"
            )

        zone = Zone()
        zone.name = zone_name
        zone.location = (x, y)

        graph.add_zone(zone)

    def parse_zone(self, line, graph):
        data = line.split(":")[1]

        # if not data:
        #     raise MapParserError(
        #         "Empty 'hub' line: expected 'hub: hub_name x y metadata'"
        #     )

        parts = data.split()

        if len(parts) != 4:
            raise MapParserError(
                "Invalid 'hub' format: expected 4 values "
                "(name x y metadata)"
            )

        zone_name = parts[0]

        try:
            x = int(parts[1])
            y = int(parts[2])
        except ValueError:
            raise MapParserError(
                "Invalid coordinates for 'hub': x and y must be integers"
            )

        zone = Zone()
        zone.name = zone_name
        zone.location = (x, y)

        graph.add_zone(zone)

    def parse_connection(self, line, graph):
        
        data = line.split(":")[1]
        parts = data.split("-")
        if len(parts) != 2:
            raise MapParserError("you need 2 item")

        a = graph.get_zone(parts[0].strip())
        b = graph.get_zone(parts[1].strip())

        graph.add_connections(a, b)

    def parse(self, file_path: str) -> Graph:
        graph = Graph()
    
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if line.startswith("nb_drones:"):
                    self.parse_drones(line, graph)
                elif line.startswith("start_hub:"):
                    self.parse_start(line, graph)
                elif line.startswith("end_hub:"):
                    self.parse_end(line, graph)
                elif line.startswith("hub:"):
                    self.parse_zone(line, graph)
                elif line.startswith("connection:"):
                    self.parse_connection(line, graph)
        return graph
