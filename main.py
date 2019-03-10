__author__ = "Martim Ferreira José"
__version__ = "1.1.1"
__license__ = "MIT"

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

        while self.code[self.position] == " " and self.position < len(self.code):
            self.position += 1

        if self.code[self.position] == "-":
            self.actual = Token("MINUS", "-")
            self.position += 1

        elif self.code[self.position] == "+":
            self.actual = Token("PLUS", "+")
            self.position += 1

        elif self.code[self.position] == "/":
            self.actual = Token("DIV", "/")
            self.position += 1

        elif self.code[self.position] == "*":
            self.actual = Token("MULT", "*")
            self.position += 1
            
        elif self.code[self.position].isdigit():
            int_token = ""
            while self.position < len(self.code) and self.code[self.position].isdigit():
                int_token += str(self.code[self.position])
                self.position += 1
            self.actual = Token("INT", int(int_token))
        
        else:
            raise ValueError("Token {} inválido".format(self.code[self.position]))

class Parser:

    @staticmethod
    def parseExpression():
        output = Parser.parseTerm()

        while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
            if Parser.tokens.actual.type == "PLUS":
                output += Parser.parseTerm()

            elif Parser.tokens.actual.type == "MINUS":
                output -= Parser.parseTerm()
            Parser.tokens.selectNext()
        return output

    @staticmethod
    def parseTerm():
        output = 0
        Parser.tokens.selectNext()

        if Parser.tokens.actual.type == "INT":
            output += Parser.tokens.actual.value
            Parser.tokens.selectNext()
            
            while Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV":
                if Parser.tokens.actual.type == "MULT":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "INT":
                        output *= Parser.tokens.actual.value
                    else:
                        raise ValueError("Um número é necessário após um operador")
                        
                elif Parser.tokens.actual.type == "DIV":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "INT":
                        output //= Parser.tokens.actual.value
                    else:
                        raise ValueError("Um número é necessário após um operador")
                Parser.tokens.selectNext()
        else:
            raise ValueError("A operação deve começar com um número")

        return output
        
    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        res = Parser.parseExpression()
        Parser.tokens.selectNext()

        if Parser.tokens.actual.value != "EOF":
            raise ValueError("Erro sintático. Último token não é o EOP.")
        return res

def main():
    code = input()
    print(Parser.run(code))

if __name__ == "__main__":
    main()