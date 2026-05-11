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