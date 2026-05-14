from graph import Graph
from drawer import Drawer
from parser import MapParser
from pathfinding import PathFider
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
    drawer = Drawer()

    
    
    drawer.draw(graph)
        
    
main()
