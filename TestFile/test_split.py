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


def parse_metadata(self, metadata, connection):

    if not metadata.startswith("[") or not metadata.endswith("]"):
        raise MapParserError("invalid metadata")

    key, value = metadata.strip("[]").split("=")

    if key != "max_link_capacity":
        raise MapParserError("unknown metadata")

    try:
        connection.capacity = int(value)
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

        self.parse_metadata(parts[3], zone)

        graph.add_zone(zone)