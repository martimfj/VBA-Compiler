class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

class Tokenizer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.actual = Token("None", "None")

    def selectNext(self):
        #print(repr(self.actual.value))
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

        elif self.code[self.position] == "=":
            self.actual = Token("ASSIGNMENT", "=")
            self.position += 1

        elif self.code[self.position] == "\n":
            self.actual = Token("LINEFEED", "\n")
            self.position += 1

        elif self.code[self.position].isdigit():
            int_token = ""
            while self.position < len(self.code) and self.code[self.position].isdigit():
                int_token += str(self.code[self.position])
                self.position += 1
            self.actual = Token("INT", int(int_token))
        
        elif self.code[self.position].isalpha():
            identifier_token = ""
            while self.position < len(self.code) and self.code[self.position].isidentifier():
                identifier_token += str(self.code[self.position]).upper()
                self.position += 1

            reserved_words = ["PRINT", "BEGIN", "END"]
            if identifier_token in reserved_words:
                self.actual = Token(identifier_token, identifier_token)
            else:
                self.actual = Token("IDENTIFIER", identifier_token)

        else:
            raise ValueError("Tokenizer Error: Token > {} < is invalid".format(repr(self.code[self.position])))