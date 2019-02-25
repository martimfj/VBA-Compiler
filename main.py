__author__ = "Martim Ferreira José"
__version__ = "1.0.1"
__license__ = "MIT"

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

class Tokenizer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.actual = self.selectNext()

    def selectNext(self):
        if self.position == len(self.code):
            return Token("EOF", "EOF")

        elif self.code[self.position] == " ":
            self.position += 1
            return self.selectNext()

        elif self.code[self.position] == "-":
            self.position += 1
            return Token("MINUS", "-")

        elif self.code[self.position] == "+":
            self.position += 1
            return Token("PLUS", "+")
        
        elif self.code[self.position].isdigit():
            int_token = ""
            while self.position < len(self.code) and self.code[self.position].isdigit():
                int_token += str(self.code[self.position])
                self.position += 1
            return Token("INT", int(int_token))
        
        else:
            raise ValueError("Token {} inválido".format(self.code[self.position]))

class Parser:

    @staticmethod
    def parseExpression():
        output = 0

        if Parser.tokens.actual.type == "INT":
            output += Parser.tokens.actual.value
            actual_token = Parser.tokens.selectNext()
            
            while actual_token.type == "PLUS" or actual_token.type == "MINUS":
                if actual_token.type == "PLUS":
                    actual_token = Parser.tokens.selectNext()
                    if actual_token.type == "INT":
                        output += actual_token.value
                    else:
                        raise ValueError("Um número é necessário após o operador +")
                        
                elif actual_token.type == "MINUS":
                    actual_token = Parser.tokens.selectNext()
                    if actual_token.type == "INT":
                        output -= actual_token.value
                    else:
                        raise ValueError("Um número é necessário após o operador -")
                actual_token = Parser.tokens.selectNext()
        else:
            raise ValueError("A operação deve começar com um número")

        return output
        
    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        return Parser.parseExpression()

def main():
    code = input()
    print(Parser.run(code))

if __name__ == "__main__":
    main()