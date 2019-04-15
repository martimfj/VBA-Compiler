from node import *
from symbol_table import SymbolTable
from prepro import PrePro
from lexer import Tokenizer

class Parser:
    @staticmethod
    def parseStatements():
        statements = []

        while Parser.tokens.actual.type not in ["EOF", "END", "WEND", "ELSE"]:
            statements.append(Parser.parseStatement())

            if Parser.tokens.actual.type == "LINEFEED":
                Parser.tokens.selectNext()

        return Statements('statements', statements)

    @staticmethod
    def parseStatement():
        if Parser.tokens.actual.type == "IDENTIFIER":
            identifier = Indentifier(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

            if Parser.tokens.actual.type == "EQUAL":
                Parser.tokens.selectNext()
                return Assigment("=", [identifier, Parser.parseExpression()])
            else:
                raise NameError("Parser Error (Statement): Name {} not defined".format(identifier.value))

        elif Parser.tokens.actual.type == "PRINT":
            Parser.tokens.selectNext()
            return Print('print', [Parser.parseExpression()])

        elif Parser.tokens.actual.type == "WHILE":
            Parser.tokens.selectNext()
            rel_exp = Parser.parseRelExpression()

            if Parser.tokens.actual.type == "LINEFEED":
                Parser.tokens.selectNext()
                statements = Parser.parseStatements()

                if Parser.tokens.actual.type == "WEND":
                    Parser.tokens.selectNext()
                    return While("WHILE", [rel_exp, statements])
                else:
                    raise ValueError("Parser Error (Statement): Expected WEND, got token {}".format(repr(Parser.tokens.actual.value)))
            else:
                raise ValueError("Parser Error (Statement): Expected '\n', got token {}".format(repr(Parser.tokens.actual.value)))

        elif Parser.tokens.actual.type == "IF":
            Parser.tokens.selectNext()
            rel_exp = Parser.parseRelExpression()
            statements_else = None

            if Parser.tokens.actual.type == "THEN":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "LINEFEED":
                    Parser.tokens.selectNext()

                    statements_if = Parser.parseStatements()
                    if Parser.tokens.actual.type == "ELSE":
                        Parser.tokens.selectNext()
                        statements_else = Parser.parseStatements()

                    if Parser.tokens.actual.type == "END":
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type == "IF":
                            Parser.tokens.selectNext()
                            return If("IF", [rel_exp, statements_if, statements_else])
                        else:
                            raise ValueError("Parser Error (Statement): Expected IF, got token {}".format(repr(Parser.tokens.actual.value)))
                    else:
                        raise ValueError("Parser Error (Statement): Expected END, got token {}".format(repr(Parser.tokens.actual.value)))
                else:
                    raise ValueError("Parser Error (Statement): Expected '\n', got token {}".format(repr(Parser.tokens.actual.value)))
            else:
                raise ValueError("Parser Error (Statement): Expected THEN, got token {}".format(repr(Parser.tokens.actual.value)))
        else:
            return NoOp()

    @staticmethod
    def parseExpression():
        output = Parser.parseTerm()

        while Parser.tokens.actual.value in ["+", "-", "OR"]:
            if Parser.tokens.actual.value == "+":
                Parser.tokens.selectNext()
                output = BinOp("+", [output, Parser.parseTerm()])

            elif Parser.tokens.actual.value == "-":
                Parser.tokens.selectNext()
                output = BinOp("-", [output, Parser.parseTerm()])

            elif Parser.tokens.actual.value == "OR":
                Parser.tokens.selectNext()
                output = BinOp("OR", [output, Parser.parseTerm()])
        return output

    @staticmethod
    def parseTerm():
        output = Parser.parseFactor()

        while Parser.tokens.actual.value in ["*", "/", "AND"]:
            if Parser.tokens.actual.value == "*":
                Parser.tokens.selectNext()
                output = BinOp("*", [output, Parser.parseFactor()])

            elif Parser.tokens.actual.value == "/":
                Parser.tokens.selectNext()
                output = BinOp("/", [output, Parser.parseFactor()])

            elif Parser.tokens.actual.value == "AND":
                Parser.tokens.selectNext()
                output = BinOp("AND", [output, Parser.parseFactor()])
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

        elif Parser.tokens.actual.type == "INPUT":
            output = Input("Input")
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

        elif Parser.tokens.actual.value in ["+", "-", "NOT"]:
            if Parser.tokens.actual.value == "+":
                Parser.tokens.selectNext()
                output = UnOp("+", [Parser.parseFactor()])

            elif Parser.tokens.actual.value == "-":
                Parser.tokens.selectNext()
                output = UnOp("-", [Parser.parseFactor()])

            elif Parser.tokens.actual.value == "NOT":
                Parser.tokens.selectNext()
                output = UnOp("NOT", [Parser.parseFactor()])
        else:
            raise ValueError("Parser Error (Factor): Token {} is invalid".format(repr(Parser.tokens.actual.value)))
        return output

    @staticmethod
    def parseRelExpression():
        output = Parser.parseExpression()

        while Parser.tokens.actual.value in ["=", ">", "<"]:
            if Parser.tokens.actual.value == "=":
                Parser.tokens.selectNext()
                output = BinOp("=", [output, Parser.parseExpression()])

            elif Parser.tokens.actual.value == ">":
                Parser.tokens.selectNext()
                output = BinOp(">", [output, Parser.parseExpression()])

            elif Parser.tokens.actual.value == "<":
                Parser.tokens.selectNext()
                output = BinOp("<", [output, Parser.parseExpression()])

        return output

    @staticmethod
    def run(code):
        st = SymbolTable()
        print(repr(PrePro.filtra(code)))
        Parser.tokens = Tokenizer(PrePro.filtra(code))
        Parser.tokens.selectNext()
        res = Parser.parseStatements()

        Parser.tokens.selectNext()
        if Parser.tokens.actual.value != "EOF":
            raise ValueError("Run (EOF Check): Expected EOF, got token {}: {}".format(repr(Parser.tokens.actual.value), Parser.tokens.position))

        res.evaluate(st)