from node import *
from symbol_table import SymbolTable
from prepro import PrePro
from lexer import Tokenizer

class Parser:
    @staticmethod
    def parseStatements():
        statements = []

        while True:
            statements.append(Parser.parseStatement())
            
            if Parser.tokens.actual.type == "LINEFEED":
                Parser.tokens.selectNext()
            elif Parser.tokens.actual.type in ["EOF", "END", "WEND"]:
                break

        return Statements('statements', statements)

    @staticmethod
    def parseStatement():
        if Parser.tokens.actual.type == "IDENTIFIER":
            identifier = Indentifier(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            
            if Parser.tokens.actual.type == "ASSIGNMENT":
                Parser.tokens.selectNext()
                return Assigment("=", [identifier, Parser.parseExpression()])
            else:
                raise NameError("Parser Error (Statement): Name {} not defined".format(identifier.value))

        elif Parser.tokens.actual.type == "PRINT":
            Parser.tokens.selectNext()
            return Print('print', [Parser.parseExpression()])

        elif Parser.tokens.actual.type == "BEGIN":
            return Parser.parseStatements()

        else:
            return NoOp()

    @staticmethod
    def parseExpression():
        output = Parser.parseTerm()

        while Parser.tokens.actual.type == "UNARY_OP":
            if Parser.tokens.actual.value == "+":
                Parser.tokens.selectNext()
                output = BinOp("+", [output, Parser.parseTerm()])

            elif Parser.tokens.actual.value == "-":
                Parser.tokens.selectNext()
                output = BinOp("-", [output, Parser.parseTerm()])
        return output

    @staticmethod
    def parseTerm():
        output = Parser.parseFactor()

        while Parser.tokens.actual.type == "BINARY_OP":
            if Parser.tokens.actual.value == "*":
                Parser.tokens.selectNext()
                output = BinOp("*", [output, Parser.parseFactor()])

            elif Parser.tokens.actual.value == "/":
                Parser.tokens.selectNext()
                output = BinOp("/", [output, Parser.parseFactor()])
        return output

    @staticmethod
    def parseFactor():
        output = 0

        if Parser.tokens.actual.type == "INT":
            output = IntVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.type == "IDENTIFIER":
            output = Indentifier(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.type == "BRACKETS":
            if Parser.tokens.actual.value == "(":
                Parser.tokens.selectNext()
                output = Parser.parseExpression()
                
                if Parser.tokens.actual.value == ")":
                    Parser.tokens.selectNext()

                else:
                    raise ValueError("Parser Error (Factor): Expected ), got token {}".format(repr(Parser.tokens.actual.value)))
            else:
                raise ValueError("Parser Error (Factor): Expected (, got token {}".format(repr(Parser.tokens.actual.value)))

        elif Parser.tokens.actual.type == "UNARY_OP":
            if Parser.tokens.actual.value == "+":
                Parser.tokens.selectNext()
                output = UnOp("+", [Parser.parseFactor()])

            elif Parser.tokens.actual.value == "-":
                Parser.tokens.selectNext()
                output = UnOp("-", [Parser.parseFactor()])

        else:
            raise ValueError("Parser Error (Factor): Expected a number, got token {}".format(repr(Parser.tokens.actual.value)))
        return output

    @staticmethod
    def run(code):
        st = SymbolTable()
        # print(repr(PrePro.filtra(code)))
        Parser.tokens = Tokenizer(PrePro.filtra(code))
        Parser.tokens.selectNext()
        res = Parser.parseStatements()

        Parser.tokens.selectNext()
        if Parser.tokens.actual.value != "EOF":
            raise ValueError("Run (EOF Check): Expected EOF, got token {}: {}".format(repr(Parser.tokens.actual.value), Parser.tokens.position))
            
        res.evaluate(st)