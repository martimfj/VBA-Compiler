SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

segment .bss
  res RESB 1

section .text
  global _start

print:
  PUSH EBP
  MOV EBP, ESP
  MOV EAX, [EBP+8]
  XOR ESI, ESI
print_dec:
  MOV EDX, 0
  MOV EBX, 0x000A
  DIV EBX
  ADD EDX, '0'
  PUSH EDX
  INC ESI
  CMP EAX, 0
  JZ print_next
  JMP print_dec
print_next:
  CMP ESI, 0
  JZ print_exit
  DEC ESI
  MOV EAX, SYS_WRITE
  MOV EBX, STDOUT
  POP ECX
  MOV [res], ECX
  MOV ECX, res
  MOV EDX, 1
  INT 0x80
  JMP print_next
print_exit:
  POP EBP
  RET

binop_je:
  JE binop_true
  JMP binop_false
binop_jg:
  JG binop_true
  JMP binop_false
binop_jl:
  JL binop_true
  JMP binop_false
binop_false:
  MOV EBX, False
  JMP binop_exit
binop_true:
  MOV EBX, True
binop_exit:
  RET

_start:
  PUSH EBP
  MOV EBP, ESP
  PUSH DWORD 0      ; Dim BT as BOOLEAN - [EBP−4]
  PUSH DWORD 0      ; Dim BF as BOOLEAN - [EBP−8]

  MOV EBX, True
  MOV [EBP-4], EBX  ; BT = True 
  MOV EBX, False
  MOV [EBP-8], EBX  ; BF = False 
  MOV EBX, [EBP-8]
  PUSH EBX
  MOV EBX, [EBP-4]
  POP EAX

  AND EAX, EBX      ; And: False & True
  MOV EBX, EAX

  PUSH EBX
  CALL print
  POP EBX

  MOV EBX, [EBP-8]
  PUSH EBX
  MOV EBX, [EBP-4]
  POP EAX

  OR EAX, EBX       ; Or: False | True
  MOV EBX, EAX

  PUSH EBX
  CALL print
  POP EBX

  MOV EBX, [EBP-8]
  MOV EBX, True     ; Negation: !False
  MOV EBX, False    ; Negation: !True
  PUSH EBX
  CALL print
  POP EBX

  MOV EBX, [EBP-4]
  PUSH EBX
  MOV EBX, [EBP-8]
  POP EAX

  AND EAX, EBX      ; And: True & False
  MOV EBX, EAX

  PUSH EBX
  MOV EBX, [EBP-8]
  POP EAX

  OR EAX, EBX       ; Or: False | False
  MOV EBX, EAX

  MOV EBX, True     ; Negation: !False
  PUSH EBX
  CALL print
  POP EBX


  POP EBP
  MOV EAX, 1
  INT 0x80

