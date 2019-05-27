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
        if self.position == len(self.code):
            self.actual = Token("EOF", "EOF")
            return

        while self.code[self.position] == " ":
            self.position += 1

        if self.code[self.position] == "-":
            self.actual = Token("ARITH_UNARY_OP", "-")
            self.position += 1

        elif self.code[self.position] == "+":
            self.actual = Token("ARITH_UNARY_OP", "+")
            self.position += 1

        elif self.code[self.position] == "/":
            self.actual = Token("ARITH_BINARY_OP", "/")
            self.position += 1

        elif self.code[self.position] == "*":
            self.actual = Token("ARITH_BINARY_OP", "*")
            self.position += 1

        elif self.code[self.position] == ">":
            self.actual = Token("COMP_BINARY_OP", ">")
            self.position += 1

        elif self.code[self.position] == "<":
            self.actual = Token("COMP_BINARY_OP", "<")
            self.position += 1

        elif self.code[self.position] == "(":
            self.actual = Token("BRACKETS", "(")
            self.position += 1

        elif self.code[self.position] == ")":
            self.actual = Token("BRACKETS", ")")
            self.position += 1

        elif self.code[self.position] == ",":
            self.actual = Token("COMMA", ",")
            self.position += 1

        elif self.code[self.position] == "=":
            self.actual = Token("EQUAL", "=")
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
            while self.position < len(self.code) and (self.code[self.position].isalnum() or self.code[self.position] == "_"):
                identifier_token += str(self.code[self.position]).upper()
                self.position += 1

            reserved_words = ["PRINT", "END", "WHILE", "WEND", "IF", "ELSE", "THEN", "INPUT", "SUB", "MAIN", "DIM", "AS", "TRUE", "FALSE", "AND", "OR", "NOT", "INTEGER", "BOOLEAN", "FUNCTION"]
            if identifier_token in reserved_words:
                self.actual = Token(identifier_token, identifier_token)
            else:
                self.actual = Token("IDENTIFIER", identifier_token)
        else:
            raise ValueError("Tokenizer Error: Token {} is invalid".format(repr(self.code[self.position])))