__author__ = "Martim Ferreira José"
__version__ = "2.1.1"
__license__ = "MIT"

from parser import Parser

def main():
    with open ('test_file.vbs', 'r') as file:
        code = file.read()
    Parser.run(code)

if __name__ == "__main__":
    main()