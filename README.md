# VBA-Compiler
### Martim Ferreira José - Engenharia de Computação Insper

## Gramática
G = ({E, T, F, +, -, *, /, (, ), n}, {+, -, *, /, (, ), n}, P, E)

## Diagrama Sintático
![Diagrama Sintático](diagrama_sintatico.png)

## EBNF

- expressão = termo, { (“+” | “-”), termo } ;
- termo = fator, { (“*” | “/”), fator } ;
- fator = (“+” | “-”) fator, número, “(” expressão “)” ;
- número = “-2^63” | ... | “2^63” ;


