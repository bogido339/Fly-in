from graph import Graph
from drawer import Drawer
from parser import MapParser
import sys

class ClassError(Exception):
    pass

def main() -> None:
    if len(sys.argv) != 2:
        raise ClassError("You need to run it like this: python main.py mapfile.txt")

    filemap = sys.argv[1]

    parser= MapParser()
    drawer = Drawer()
    graph: Graph = parser.parse(filemap)
    drawer.draw(graph)
    

main()