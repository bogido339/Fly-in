from graph import Graph
from zone import Zone
from connections import Connection

class MapParserError(Exception):
    pass

class MapParser:
    def __init__(self):
        self.locations = []
        self.zones_name = []

    def parse_drones(self, line, graph):
        try:
            number = int(line.split(":")[1])
            if number < 0:
                raise ValueError()

            graph.nb_drones = number
        except ValueError:
            raise MapParserError("Invalid 'nb_drones' value: expected an integer after ':'")

    def parse_metadata(self, metadata, obj):

        if not metadata.startswith("[") or not metadata.endswith("]"):
            raise MapParserError("invalid metadata")
        
        parts = metadata.strip("[]").split()
        for part in parts:
            key, value = part.split("=")

            # if key.strip() != "max_link_capacity":
            #     raise MapParserError("unknown metadata")

            try:
                obj.capacity = int(value)
            except ValueError:
                raise MapParserError("invalid capacity")

    def parse_start(self, line, graph):
        
        data = line.split(":", 1)[1].strip()
        parts = data.split()

        if len(parts) == 0 or len(parts) != 4:
            raise MapParserError("invalid start_hub sysntax")

        if parts[0].strip() != "start":
            raise MapParserError("Invalid start hub name: expected 'start'")

        try:
            x = int(parts[1])
            y = int(parts[2])
            if (x, y) not in self.locations:
                self.locations.append((x, y))
            else:
                raise MapParserError("this location is alrydy in map not fawnd")
        except ValueError:
            raise MapParserError("Invalid coordinates for 'start_hub'")

        zone = Zone()
        zone.name = data[0].strip()
        zone.location = (x, y)

        self.parse_metadata(parts[4], zone)

        graph.add_zone(zone)

    def parse_end(self, line, graph):

        data = line.split(":", 1)[1].strip()
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

        payload = line.split(":", 1)[1].strip()
        parts = payload.split()

        if len(parts) == 0 or len(parts) > 2:
            raise MapParserError("invalid connection syntax")

        zone_part = parts[0]
        names = zone_part.split("-")

        if len(names) != 2:
            raise MapParserError("invalid zone format")

        a = graph.get_zone(names[0])
        b = graph.get_zone(names[1])

        if not a or not b:
            raise MapParserError("zone not found")

        connection = graph.add_connections(a, b)

        if len(parts) == 2:
            self.parse_metadata(parts[1], connection)

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
