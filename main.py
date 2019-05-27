__author__ = "Martim Ferreira José"
__version__ = "3.0.1"
__license__ = "MIT"

from parser import Parser
from assembler import Assembler
import sys
import os

def main():
    try:
        filename = sys.argv[1] #"test_file.vbs"
    except IndexError:
        print("This program needs an input .vbs file to continue. Exiting...")
        sys.exit(1)

    with open (filename, 'r') as file:
        code = file.read()
    Parser.run(code)
    Assembler.write_file()
    
    os.system("nasm -f elf32 -F dwarf -g program.asm ")
    os.system("ld -m elf_i386 -o program program.o")
    os.system("./program")

if __name__ == "__main__":
    main()