class Node:
    def __init__(self, name: str):
        self.name = name
        # A list to store references to other connected Node objects
        self.neighbors: list['Node'] = []

    def add_neighbor(self, neighbor: 'Node') -> None:
        """Connects this node to another node."""
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def __repr__(self) -> str:
        return self.name
    
class Graph:
    def __init__(self):
        # A dictionary mapping a string name to the actual Node object
        self.nodes: dict[str, Node] = {}

    def add_node(self, name: str) -> Node:
        """Adds a new node to the graph if it doesn't exist."""
        if name not in self.nodes:
            self.nodes[name] = Node(name)
        return self.nodes[name]

    def add_edge(self, from_name: str, to_name: str, bidirectional: bool = True) -> None:
        """Creates a link between two nodes."""
        # Ensure both nodes exist in the graph
        node_a = self.add_node(from_name)
        node_b = self.add_node(to_name)

        # Connect them
        node_a.add_neighbor(node_b)
        
        # If it's a two-way street, connect B back to A
        if bidirectional:
            node_b.add_neighbor(node_a)

    def display(self) -> None:
        """Prints the graph's connections."""
        for name, node in self.nodes.items():
            neighbor_names = [n.name for n in node.neighbors]
            print(f"{name} is connected to: {neighbor_names}")

# 1. Initialize the network manager
my_network = Graph()

# 2. Add edges (this automatically creates the nodes if they don't exist)
my_network.add_edge("Start_Hub", "Zone_A")
my_network.add_edge("Zone_A", "Zone_B")
my_network.add_edge("Zone_B", "End_Hub")

# You can also add intersecting paths
my_network.add_edge("Start_Hub", "Zone_B")

# 3. View the structure
my_network.display()