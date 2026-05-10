from graph import Graph
from drower import Drower
from parser import MapParser
import sys

class ClassError(Exception):
    pass

def main() -> None:
    if len(sys.argv) != 2:
        raise ClassError("You need to run it like this: python main.py mapfile.txt")

    filemap = sys.argv[1]

    parser= MapParser()
    drower = Drower()
    graph: Graph = parser.parse(filemap)
    drower.drow(graph)
    

main()