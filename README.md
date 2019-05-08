# VBA Compiler

## Diagrama Sintático
![Diagrama Sintático](diagrama_sintatico.png)

## EBNF
- program: "sub", "main", "(", ")", {statement, "\n"}, "end", "sub";
- statement: (assingment | print | declare | while | if_else);
- assingment: identifier, "=", expression;
- print: "print", expression;
- declare: "dim", identifier, "as", type;
- while: "while", rel_expression, {statement, "\n"}, "wend";
- if_else: "if", rel_expression, "then", {statement, "\n"}, ["else", "\n", {statement, "\n"}], "end", "if";

- rel_expression: expression, (("=" | ">" | "<"), expression);
- expression: term, {("+" | "-" | "or"), term};
- term: factor, {("*" | "/" | "and"), factor};
- factor: number, ("True" | "False"), (“+” | “-” | "not"), identifier | "(", expression, ")" | "input");
- type: "integer" | "boolean"

- identifier = letter, { letter | digit | “_” } ;
- number = digit, { digit } ;
- letter = "A" | "B" | "C" | "D" | "E" | "F" | "G"
       | "H" | "I" | "J" | "K" | "L" | "M" | "N"
       | "O" | "P" | "Q" | "R" | "S" | "T" | "U"
       | "V" | "W" | "X" | "Y" | "Z" ;
- digit = ( "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ) ;

## Como utilizar
Para utilizar o compilador, rode o arquivo `main.py`, passando como argumento o arquivo **.vbs* a ser compilado. Para testar com o arquivo de teste:
```bash
$ python main.py test_file.vbs
```
