__author__ = "Martim Ferreira José"
__version__ = "2.4.1"
__license__ = "MIT"

from parser import Parser
import sys

def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        print("This program accepts a .vbs file as input. Running test_file.vbs...")
        filename = "test_file.vbs"

    with open (filename, 'r') as file:
        code = file.read()
    Parser.run(code)

if __name__ == "__main__":
    main()