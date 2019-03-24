# VBA-Compiler
### Martim Ferreira José - Engenharia de Computação Insper

## Gramática
G = ({E, T, F, +, -, *, /, (, ), n}, {+, -, *, /, (, ), n}, P, E)

## Diagrama Sintático
![Diagrama Sintático](diagrama_sintatico.png)

## EBNF

- expressão = termo, { (“+” | “-”), termo } ;
- termo = fator, { (“*” | “/”), fator } ;
- fator = (“+” | “-”) fator | número, “(” expressão “)” ;
- número = “-2^63” | ... | “2^63” ;

## Como utilizar
Para utilizar o compilador nesta fase inicial, rode o arquivo `main.py`. Para alterar a equação que será executada, modifique o arquivo *test_file.vbs*.

## Testes
Para relizar os testes do compilador, execute o arquivo `test.py`.