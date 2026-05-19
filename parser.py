from graph import Graph
from zone import Zone
import sys


class MapParserError(Exception):
    pass


class MapParser:
    def __init__(self):
        self.locations = set()
        self.zones_name = []

    def parse_drones(self, line, graph, nb_line):
        try:
            number = int(line.split(":")[1].strip())
            if number < 0:
                raise ValueError()
            graph.nb_drones = number

        except ValueError:
            raise MapParserError(f"Line {nb_line}: Invalid 'nb_drones' value: expected a positive integer after ':'")

    def parse_metadata(self, meta_part, obj, nb_line):
        if not meta_part:
            return

        parts = meta_part.split()
        for part in parts:
            if "=" not in part:
                raise MapParserError(f"Line {nb_line}: Invalid metadata format '{part}'. Expected key=value.")
                
            key, value = part.split("=", 1)

            if isinstance(obj, Zone):
                if key.strip() == "color":
                    obj.color = value.strip()
                elif key.strip() == "max_drones":
                    try:
                        obj.capacity = int(value)
                    except ValueError:
                        raise MapParserError(f"Line {nb_line}: Invalid zone capacity")
                elif key.strip() == "zone":
                    obj.type = value.strip()

                    if obj.type == "restricted":
                        obj.cost = 2
                    elif obj.type == "priority":
                        obj.cost = 0.99
                    elif obj.type == "blocked":
                        obj.cost = sys.maxsize
                    else:
                        raise MapParserError(f"Line: {nb_line}: uknown type zone")
                else:
                    raise MapParserError(f"Line {nb_line}: Invalid item '{key}' in zone metadata")
            else:
                if key.strip() == "max_link_capacity":
                    try:
                        obj.capacity = int(value)
                    except ValueError:
                        raise MapParserError(f"Line {nb_line}: Invalid connection capacity")
                else:
                    raise MapParserError(f"Line {nb_line}: Invalid item '{key}' in connection metadata")

    def parse_start(self, line, graph, nb_line):
        if "[" in line:
            main_part, meta_part = line.split("[", 1)
            meta_part = meta_part.strip("]")
        else:
            main_part = line
            meta_part = ""
        
        data = main_part.split(":", 1)[1].strip()
        parts = data.split()

        if len(parts) < 3:
            raise MapParserError(f"Line {nb_line}: Invalid start_hub syntax. Expected 'name x y'")

        try:
            x = int(parts[1])
            y = int(parts[2])
            if (x, y) not in self.locations:
                self.locations.add((x, y))
            else:
                raise MapParserError(f"Line {nb_line}: Location ({x}, {y}) is already in the map")
        except ValueError:
            raise MapParserError(f"Line {nb_line}: Invalid coordinates for 'start_hub'")

        zone = Zone()
        zone.name = parts[0].strip()
        zone.location = (x, y)

        if meta_part:
            self.parse_metadata(meta_part, zone, nb_line)

        graph.add_zone(zone)
        graph.start_zone = zone
        graph.start_zone.current_drones = graph.nb_drones
        graph.start_zone.capacity = graph.nb_drones

    def parse_end(self, line, graph, nb_line):
        if "[" in line:
            main_part, meta_part = line.split("[", 1)
            meta_part = meta_part.strip("]")
        else:
            main_part = line
            meta_part = ""

        data = main_part.split(":", 1)[1].strip()
        parts = data.split()

        if len(parts) < 3:
            raise MapParserError(f"Line {nb_line}: Invalid 'end_hub' syntax. Expected 'name x y'")

        zone_name = parts[0].strip()

        try:
            x = int(parts[1])
            y = int(parts[2])
            if (x, y) not in self.locations:
                self.locations.add((x, y))
            else:
                raise MapParserError(f"Line {nb_line}: Location ({x}, {y}) is already in the map")
        except ValueError:
            raise MapParserError(f"Line {nb_line}: Invalid coordinates for 'end_hub': x and y must be integers")

        zone = Zone()
        zone.name = zone_name
        zone.location = (x, y)
        
        if meta_part:
            self.parse_metadata(meta_part, zone, nb_line)
            
        graph.add_zone(zone)
        graph.end_zone = zone
        graph.end_zone.capacity = graph.nb_drones

    def parse_zone(self, line, graph, nb_line):
        if "[" in line:
            main_part, meta_part = line.split("[", 1)
            meta_part = meta_part.strip("]")
        else:
            main_part = line
            meta_part = ""
    
        data = main_part.split(":", 1)[1].strip()
        parts = data.split()

        if len(parts) < 3:
            raise MapParserError(f"Line {nb_line}: Invalid 'hub' format: expected at least 3 values (name x y)")

        zone_name = parts[0].strip()

        try:
            x = int(parts[1])
            y = int(parts[2])
            if (x, y) not in self.locations:
                self.locations.add((x, y))
            else:
                raise MapParserError(f"Line {nb_line}: Location ({x}, {y}) is already in the map")
        except ValueError:
            raise MapParserError(f"Line {nb_line}: Invalid coordinates for 'hub': x and y must be integers")

        zone = Zone()
        zone.name = zone_name
        zone.location = (x, y)
        
        if meta_part:
            self.parse_metadata(meta_part, zone, nb_line)
            
        graph.add_zone(zone)

    def parse_connection(self, line, graph, nb_line):
        if "[" in line:
            main_part, meta_part = line.split("[", 1)
            meta_part = meta_part.strip("]")
        else:
            main_part = line
            meta_part = ""

        payload = main_part.split(":", 1)[1].strip()
        parts = payload.split()

        if not parts:
            raise MapParserError(f"Line {nb_line}: Invalid connection syntax")

        zone_part = parts[0]
        names = zone_part.split("-")

        if len(names) != 2:
            raise MapParserError(f"Line {nb_line}: Invalid zone format. Expected 'hubA-hubB'")

        a = graph.get_zone(names[0].strip())
        b = graph.get_zone(names[1].strip())

        if not a or not b:
            raise MapParserError(f"Line {nb_line}: Zone not found for connection {zone_part}")

        connection = graph.add_connections(a, b)
        
        if meta_part:
            self.parse_metadata(meta_part, connection, nb_line)

    def parse(self, file_path: str) -> Graph:
        graph = Graph()
    
        with open(file_path, 'r') as file:
            for nb_line, line in enumerate(file, start=1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if line.startswith("nb_drones:"):
                    self.parse_drones(line, graph, nb_line)
                elif line.startswith("start_hub:"):
                    self.parse_start(line, graph, nb_line)
                elif line.startswith("end_hub:"):
                    self.parse_end(line, graph, nb_line)
                elif line.startswith("hub:"):
                    self.parse_zone(line, graph, nb_line)
                elif line.startswith("connection:"):
                    self.parse_connection(line, graph, nb_line)
                else:
                    raise MapParserError(f"Line {nb_line}: Unknown command or invalid syntax")
                    
        return graph
