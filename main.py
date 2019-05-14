__author__ = "Martim Ferreira José"
__version__ = "2.3.1"
__license__ = "MIT"

from parser import Parser
from assembler import Assembler
import sys

def main():
    try:
        filename = "test_file.vbs" #sys.argv[1]
    except IndexError:
        print("This program needs an input .vbs file to continue. Exiting...")
        sys.exit(1)

    with open (filename, 'r') as file:
        code = file.read()
    Parser.run(code)
    Assembler.write_file()

if __name__ == "__main__":
    main()