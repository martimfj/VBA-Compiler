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


## Como utilizar
Para utilizar o compilador nesta fase inicial, rode o arquivo `main.py` e inpute uma expressão que a gramática suporte, como por exemplo: *(9-7)*3+(4+6)/5*

## Testes
Para relizar os testes do compilador, execute o arquivo `test.py`.