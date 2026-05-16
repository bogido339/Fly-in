from graph import Graph
from drawer import Drawer
from parser import MapParser
from pathfinding import PathFider
from simulation import Simulator
from drone import Drone
import sys

class ClassError(Exception):
    pass

def main() -> None:
    if len(sys.argv) != 2:
        raise ClassError("You need to run it like this: python main.py mapfile.txt")

    filemap = sys.argv[1]

    parser= MapParser()
    graph: Graph = parser.parse(filemap)

    pathfider = PathFider(graph)
    path = pathfider.find_shortest_path()

    graph.path = path
    print("PATH:", [zone.name for zone in path])

    simulator = Simulator(graph)
    simulator.create_drons()
    # simulator.run()
    
    drawer = Drawer()
    drawer.draw_all(graph, simulator)

    
        
    
main()
