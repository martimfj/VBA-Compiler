# Roteiro Zero 0 - Simple Calculator v0.1
### Martim José
**Entrega:** 18/02/2019

## IR (Intermediate Representation) vs ML (Machine Language)

### 1. O que é uma Representação Intermediária e uma Linguagem de Máquina.
A representação intermediária é a representação de um programa entre o código fonte e a linguagem alvo. Já a linguagem de máquina é uma sequência de instruções a serem executadas pelo processador.

### 2. Quais são as principais vantages e desvantages entre Linguagem de Máquina e Representação Intermediária?

| Representação Intermediária | Linguagem de Máquina           |
|-----------------------------|--------------------------------|
| Multiplataforma             | Performance                    |
| Debugging (sem print)       | Tamanho                        |
| Language Interoperability   | Consegue fazer cross compiling |
| Precisa de runtime          |                                |


## Compilador

### 1. Qual é o principal propósito de um compilador?

Um compilador é um programa que recebe de entrada um programa em uma determinada linguagem de programação (código fonte) e o traduz para um programa em outra linguagem (código objeto). O compilador tem o importante papel de relatar quaisquer erros no programa fonte detectados no processo de tradução. Se este programa objeto for um programa em linguagem de máquina, poderá ser executado pelo usuário para processar entradas e produzir saídas.

### 2. Como funciona um compilador?
O compilador pode ser simplificado por meio de uma caixa preta, em que podemos ter:
- **Interpretador:** Código Fonte -> Black Box (Compilador) -> Assembly -> Código Objeto (Assembler) -> Executável (Linker)
- **Compilador:** Código Fonte -> Black Box (Compilador) -> Representação Intermediária -> Máquina Virtual
- **Tradutor:** Código Fonte -> Black Box (Compilador) -> Assembly -> Linker -> Código Máquina Alvo

### 3. Como funciona o Blackbox?

O funcionamento de um compilador pode ser dividido em algumas etapas:

Código Fonte -> Pré-Processamento -> Análise Léxica -> Análise Sintática -> Análise Semântica -> Geração do Código (Interpretação ou Executável)

### 4. Qual etapa seria melhor otimizar o código de saída?

Como as etapas não são necessariamente sequenciais, podendo realizar várias passagens no código, é possível otimizar o código fonte em todas as etapas da compilação. Mas geralmente esta é feita na Geração do Código.

### 5. Qual é o papel de cada etapa do compilador?

- O **Pré-Processamento** resolve macros e diretivas de compilação (constantes), limpa arquivo fonte de comentários e Linefeed.
- A **Análise Léxica** divide o código fonte em um conjunto de *tokens*.
- A **Análise Sintática** verifica se o conteúdo do código fonte está aderente à especificação da linguagem de programação.
- A **Análise Semântica** verifica se o programa, a pesar de correto sintaticamente, faz sentido (não é análise de algoritmo). Por exemplo:
    - Duplicidade ou ausência de declaração de variáveis.
    - Operações, funções e atribuições com tipos incompatíveis.
    - Etc...

## Atividade

### Construa um programa que lê uma entrada do usuário com uma cadeia de somas e subtrações de números inteiros de múltiplos dígitos. Ao final deve interpretar e realizar a operação, exibindo o resultado final.

**Base de testes:**

    >> 1+2
    >> 3-2
    >> 1+2-3
    >> 11+22-33
    >> 789 +345 - 123


### 1. Explique como foi feito para reconhecer múltiplos dígitos e realizar múltiplas operações.

Para reconhecer diversos dígitos, foi utilizado a expressão regular *(\W)*, que combina qualquer caracter que não é uma palavra de caracteres (alphanumérico e underscore). Passando essa expressão na função *split()*, obteve-se uma lista com os números e operações.

### 2. Pense na estrutura de alguma linguagem procedural (C por exemplo), indique com detalhes como você expandiria o seu programa para compilar um programa nessa linguagem.

Para compilar um programa em C, o programa deve detectar os tokens principais da linguagem como a função main e logo após as operações. Mas isso não seria suficiente, teria também que validar o código sintáticamente e semânticamente.
