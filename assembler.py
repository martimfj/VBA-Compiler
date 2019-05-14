CONSTANTS = [
"SYS_EXIT equ 1",
"SYS_READ equ 3",
"SYS_WRITE equ 4",
"STDIN equ 0",
"STDOUT equ 1",
"True equ 1",
"False equ 0"
]

DATA_SEG = [
"segment .data"
]

TEXT_SEG =[
"section .text",
"  global _start"
]

PRINT_SUBROUTINE = [
"print:",
  "  PUSH EBP",
  "  MOV EBP, ESP",
  "  MOV EAX, [EBP+8]",
  "  XOR ESI, ESI",

"print_dec:",
  "  MOV EDX, 0",
  "  MOV EBX, 0x000A",
  "  DIV EBX",
  "  ADD EDX, '0'",
  "  PUSH EDX",
  "  INC ESI",
  "  CMP EAX, 0",
  "  JZ print_next",
  "  JMP print_dec",

"print_next:",
  "  CMP ESI, 0",
  "  JZ print_exit",
  "  DEC ESI",
  "  MOV EAX, SYS_WRITE",
  "  MOV EBX, STDOUT",
  "  POP ECX",
  "  MOV [res], ECX",
  "  MOV ECX, res",
  "  MOV EDX, 1",
  "  INT 0x80",
  "  JMP print_next",

"print_exit:",
  "  POP EBP",
  "  RET"
]

IF_WHILE_SUBROUTINE = [
"binop_je:",
  "  JE binop_true",
  "  JMP binop_false",

"binop_jg:",
  "  JG binop_true",
  "  JMP binop_false",

"binop_jl:",
  "  JL binop_true",
  "  JMP binop_false",

"binop_false:",
  "  MOV EBX, False",
  "  JMP binop_exit",

"binop_true:",
  "  MOV EBX, True",

"binop_exit:",
  "  RET"
]

INTERRUPT = [
"POP EBP",
"MOV EAX, 1",
"INT 0x80"
]

class Assembler:
    bss_segment = ["segment .bss", "  res RESB 1"]
    program = ["_start:"]

    @staticmethod
    def write_line(line):
        Assembler.program.append("  " + line)

    @staticmethod
    def write_bss(line):
        Assembly.bss_segment.append("  " + line)

    @staticmethod
    def write_file():
        code = []
        sections = [CONSTANTS, DATA_SEG, TEXT_SEG, PRINT_SUBROUTINE, IF_WHILE_SUBROUTINE, Assembler.program, INTERRUPT]
        for section in sections:
            code.extend(section)
            code.append("\r")

        with open("program.asm", "w") as myfile:
            for line in code:
                myfile.write(line + "\n")