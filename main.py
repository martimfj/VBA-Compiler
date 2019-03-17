__author__ = "Martim Ferreira José"
__version__ = "1.2.1"
__license__ = "MIT"

import re


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

class Tokenizer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.actual = None

    def selectNext(self):
        if self.position == len(self.code):
            self.actual = Token("EOF", "EOF")
            return

        while self.code[self.position] == " ":
            self.position += 1

        if self.code[self.position] == "-":
            self.actual = Token("UNARY_OP", "-")
            self.position += 1

        elif self.code[self.position] == "+":
            self.actual = Token("UNARY_OP", "+")
            self.position += 1

        elif self.code[self.position] == "/":
            self.actual = Token("BINARY_OP", "/")
            self.position += 1

        elif self.code[self.position] == "*":
            self.actual = Token("BINARY_OP", "*")
            self.position += 1

        elif self.code[self.position] == "(":
            self.actual = Token("BRACKETS", "(")
            self.position += 1

        elif self.code[self.position] == ")":
            self.actual = Token("BRACKETS", ")")
            self.position += 1
            
        elif self.code[self.position].isdigit():
            int_token = ""
            while self.position < len(self.code) and self.code[self.position].isdigit():
                int_token += str(self.code[self.position])
                self.position += 1
            self.actual = Token("INT", int(int_token))
        
        else:
            raise ValueError("Token {} inválido".format(repr(self.code[self.position])))

class Parser:

    @staticmethod
    def parseExpression():
        output = Parser.parseTerm()

        while Parser.tokens.actual.type == "UNARY_OP":
            if Parser.tokens.actual.value == "+":
                output += Parser.parseTerm()

            elif Parser.tokens.actual.value == "-":
                output -= Parser.parseTerm()
        return output

    @staticmethod
    def parseTerm():
        output = Parser.parseFactor()

        while Parser.tokens.actual.type == "BINARY_OP":
            if Parser.tokens.actual.value == "*":
                output *= Parser.parseFactor()

            elif Parser.tokens.actual.value == "/":
                output //= Parser.parseFactor()
        return output

    @staticmethod
    def parseFactor():
        output = 0
        
        Parser.tokens.selectNext()
        
        if Parser.tokens.actual.type == "INT":
            output += Parser.tokens.actual.value
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.type == "BRACKETS":
            if Parser.tokens.actual.value == "(":
                output = Parser.parseExpression()
                
                if Parser.tokens.actual.value == ")":
                    Parser.tokens.selectNext()
                
                else:
                    raise ValueError("Não fechou parênteses")
            else:
                raise ValueError("Começou com parênteses errado")

        elif Parser.tokens.actual.type == "UNARY_OP":
            if Parser.tokens.actual.value == "+":
                output += Parser.parseFactor()

            elif Parser.tokens.actual.value == "-":
                output -= Parser.parseFactor()

        else:
            raise ValueError("Após operador deve haver um número")
        return output

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(PrePro.filtra(code).rstrip())
        res = Parser.parseExpression()
        Parser.tokens.selectNext()

        if Parser.tokens.actual.value != "EOF":
            raise ValueError("Erro sintático. Último token não é o EOP.")
        return res

class PrePro:
    @staticmethod
    def filtra(code):
        return re.sub("'.*\n", "", code.replace("\\n", "\n"))

def main():
    code = input() + "\n"
    print(Parser.run(code))

if __name__ == "__main__":
    main()