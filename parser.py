from node import *
from symbol_table import SymbolTable
from prepro import PrePro
from lexer import Tokenizer

class Parser:
    @staticmethod
    def parseSubDec():
        subStatements = []
        subArguments = []

        if Parser.tokens.actual.type == "SUB":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "IDENTIFIER":
                subIdentifier = Parser.tokens.actual.value
                Parser.tokens.selectNext()
                if Parser.tokens.actual.value == "(":
                    Parser.tokens.selectNext()

                    while Parser.tokens.actual.value != ")":
                        if Parser.tokens.actual.type == "IDENTIFIER":
                            subArgName = Parser.tokens.actual.value
                            Parser.tokens.selectNext()
                            if Parser.tokens.actual.type == "AS":
                                Parser.tokens.selectNext()
                                subArguments.append(VarDec("subArgDec", [Identifier(subArgName), Parser.parseType()]))
                                if Parser.tokens.actual.type == "COMMA":
                                    Parser.tokens.selectNext()
                                    if Parser.tokens.actual.type != "IDENTIFIER":
                                        raise ValueError("Parser Error (funcDeclaration): Expected an identifier, got token {}".format(repr(Parser.tokens.actual.value)))
                            else:
                                raise ValueError("Parser Error (subDeclaration): Expected AS, got token {}".format(repr(Parser.tokens.actual.value)))

                    if Parser.tokens.actual.value == ")":
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type == "LINEFEED":
                            Parser.tokens.selectNext()

                            while Parser.tokens.actual.type != "END":
                                subStatements.append(Parser.parseStatement())

                                if Parser.tokens.actual.type == "LINEFEED":
                                    Parser.tokens.selectNext()
                            
                            if Parser.tokens.actual.type == "END":
                                Parser.tokens.selectNext()

                                if Parser.tokens.actual.type == "SUB":
                                    Parser.tokens.selectNext()
                                else:
                                    raise ValueError("Parser Error (subDeclaration): Expected SUB, got token {}".format(repr(Parser.tokens.actual.value)))
                            else:
                                raise ValueError("Parser Error (subDeclaration): Expected END, got token {}".format(repr(Parser.tokens.actual.value)))
                        else:
                            raise ValueError("Parser Error (subDeclaration): Expected '\n', got token {}".format(repr(Parser.tokens.actual.value)))
                    else:
                        raise ValueError("Parser Error (subDeclaration): Expected ), got token {}".format(repr(Parser.tokens.actual.value)))
                else:
                    raise ValueError("Parser Error (subDeclaration): Expected (, got token {}".format(repr(Parser.tokens.actual.value)))
            else:
                raise ValueError("Parser Error (subDeclaration): Expected an identifier, got token {}".format(repr(Parser.tokens.actual.value)))
        else:
            raise ValueError("Parser Error (subDeclaration): Expected SUB, got token {}".format(repr(Parser.tokens.actual.value)))
        
        return SubDec(subIdentifier, subArguments + [subStatements])

    @staticmethod
    def parseFuncDec():
        funcStatements = []
        funcArguments = []

        if Parser.tokens.actual.type == "FUNCTION":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "IDENTIFIER":
                funcIdentifier = Parser.tokens.actual.value
                Parser.tokens.selectNext()
                if Parser.tokens.actual.value == "(":
                    Parser.tokens.selectNext()

                    while Parser.tokens.actual.value != ")":
                        if Parser.tokens.actual.type == "IDENTIFIER":
                            funcArgName = Parser.tokens.actual.value
                            Parser.tokens.selectNext()
                            if Parser.tokens.actual.type == "AS":
                                Parser.tokens.selectNext()
                                funcArguments.append(VarDec("funcArgDec", [Identifier(funcArgName), Parser.parseType()]))
                                if Parser.tokens.actual.type == "COMMA":
                                    Parser.tokens.selectNext()
                                    if Parser.tokens.actual.type != "IDENTIFIER":
                                        raise ValueError("Parser Error (funcDeclaration): Expected an identifier, got token {}".format(repr(Parser.tokens.actual.value)))
                            else:
                                raise ValueError("Parser Error (funcDeclaration): Expected AS, got token {}".format(repr(Parser.tokens.actual.value)))

                    if Parser.tokens.actual.value == ")":
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type == "AS":
                            Parser.tokens.selectNext()
                            funcType = [VarDec("funcType", [Identifier(funcIdentifier), Parser.parseType()])]

                            if Parser.tokens.actual.type == "LINEFEED":
                                Parser.tokens.selectNext()

                                while Parser.tokens.actual.type != "END":
                                    funcStatements.append(Parser.parseStatement())

                                    if Parser.tokens.actual.type == "LINEFEED":
                                        Parser.tokens.selectNext()
                                
                                if Parser.tokens.actual.type == "END":
                                    Parser.tokens.selectNext()

                                    if Parser.tokens.actual.type == "FUNCTION":
                                        Parser.tokens.selectNext()
                                    else:
                                        raise ValueError("Parser Error (functionDeclaration): Expected FUNCTION, got token {}".format(repr(Parser.tokens.actual.value)))
                                else:
                                    raise ValueError("Parser Error (functionDeclaration): Expected END, got token {}".format(repr(Parser.tokens.actual.value)))
                            else:
                                raise ValueError("Parser Error (functionDeclaration): Expected '\n', got token {}".format(repr(Parser.tokens.actual.value)))
                        else:
                            raise ValueError("Parser Error (functionDeclaration): Expected AS, got token {}".format(repr(Parser.tokens.actual.value)))
                    else:
                        raise ValueError("Parser Error (functionDeclaration): Expected ), got token {}".format(repr(Parser.tokens.actual.value)))
                else:
                    raise ValueError("Parser Error (functionDeclaration): Expected (, got token {}".format(repr(Parser.tokens.actual.value)))
            else:
                raise ValueError("Parser Error (functionDeclaration): Expected an identifier, got token {}".format(repr(Parser.tokens.actual.value)))
        else:
            raise ValueError("Parser Error (functionDeclaration): Expected FUNCTION, got token {}".format(repr(Parser.tokens.actual.value)))
        
        return FuncDec(funcIdentifier, funcType + funcArguments + [funcStatements])

    @staticmethod
    def parseStatement():
        if Parser.tokens.actual.type == "IDENTIFIER":
            identifier = Identifier(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

            if Parser.tokens.actual.type == "EQUAL":
                Parser.tokens.selectNext()
                return Assigment("=", [identifier, Parser.parseRelExpression()])
            else:
                raise NameError("Parser Error (Statement): Name {} not defined".format(repr(identifier.value)))

        elif Parser.tokens.actual.type == "PRINT":
            Parser.tokens.selectNext()
            return Print('print', [Parser.parseRelExpression()])

        elif Parser.tokens.actual.type == "WHILE":
            Parser.tokens.selectNext()
            rel_exp = Parser.parseRelExpression()

            if Parser.tokens.actual.type == "LINEFEED":
                Parser.tokens.selectNext()
                statements = []
                while Parser.tokens.actual.type != "WEND":
                    statements.append(Parser.parseStatement())

                    if Parser.tokens.actual.type == "LINEFEED":
                        Parser.tokens.selectNext()
                    else:
                        raise ValueError("Parser Error (Statement): Expected '\n', got token {}".format(repr(Parser.tokens.actual.value)))
                
                if Parser.tokens.actual.type == "WEND": #Just an excuse to consume the token and SelectNext
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
                    
                    statements_if = []
                    while Parser.tokens.actual.type not in ["ELSE", "END"]:
                        statements_if.append(Parser.parseStatement())

                        if Parser.tokens.actual.type == "LINEFEED":
                            Parser.tokens.selectNext()
                        else:
                            raise ValueError("Parser Error (Statement): Expected '\n', got token {}".format(repr(Parser.tokens.actual.value)))
                    
                    if Parser.tokens.actual.type == "ELSE":
                        Parser.tokens.selectNext()

                        if Parser.tokens.actual.type == "LINEFEED":
                            Parser.tokens.selectNext()

                            statements_else = []
                            while Parser.tokens.actual.type != "END":
                                statements_else.append(Parser.parseStatement())

                                if Parser.tokens.actual.type == "LINEFEED":
                                    Parser.tokens.selectNext()
                                else:
                                    raise ValueError("Parser Error (Statement): Expected '\n', got token {}".format(repr(Parser.tokens.actual.value)))
                        else:
                            raise ValueError("Parser Error (Statement): Expected '\n', got token {}".format(repr(Parser.tokens.actual.value)))

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
        
        elif Parser.tokens.actual.type == "DIM":
            Parser.tokens.selectNext()

            if Parser.tokens.actual.type == "IDENTIFIER":
                identifier = Identifier(Parser.tokens.actual.value)
                Parser.tokens.selectNext()

                if Parser.tokens.actual.type == "AS":
                    Parser.tokens.selectNext()
                    return VarDec("VarDec", [identifier, Parser.parseType()])
                else:
                    raise ValueError("Parser Error (Statement): Expected AS, got token {}".format(repr(Parser.tokens.actual.value)))
            else:
                raise ValueError("Parser Error (Statement): Expected an IDENTIFIER, got token {}".format(repr(Parser.tokens.actual.value)))

        elif Parser.tokens.actual.type == "CALL":
            Parser.tokens.selectNext()

            callArguments = []

            if Parser.tokens.actual.type == "IDENTIFIER":
                callIdentifier = Parser.tokens.actual.value
                Parser.tokens.selectNext()
                if Parser.tokens.actual.value == "(":
                    Parser.tokens.selectNext()

                    while Parser.tokens.actual.value != ")":
                        callArguments.append(Parser.parseRelExpression())

                        if Parser.tokens.actual.type == "COMMA":
                            Parser.tokens.selectNext()
                        
                    if Parser.tokens.actual.value == ")":
                        Parser.tokens.selectNext()
                        return FuncCall(callIdentifier, callArguments)
                    else:
                        raise ValueError("Parser Error (Statement): Expected ), got token {}".format(repr(Parser.tokens.actual.value)))
                else:
                    raise ValueError("Parser Error (Statement): Expected (, got token {}".format(repr(Parser.tokens.actual.value)))
            else:
                raise ValueError("Parser Error (Statement): Expected an IDENTIFIER, got token {}".format(repr(Parser.tokens.actual.value)))

        else:
            return NoOp()

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
            identifier = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if Parser.tokens.actual.value == "(":
                Parser.tokens.selectNext()
                callArguments = []

                while Parser.tokens.actual.value != ")":
                    callArguments.append(Parser.parseRelExpression())
                    
                    if Parser.tokens.actual.type == "COMMA":
                        Parser.tokens.selectNext()

                if Parser.tokens.actual.value == ")":
                    Parser.tokens.selectNext()
                    output = FuncCall(identifier, callArguments)
                else:
                    raise ValueError("Parser Error (subDeclaration): Expected ), got token {}".format(repr(Parser.tokens.actual.value)))
            else:
                output = Identifier(identifier)

        elif Parser.tokens.actual.type == "INPUT":
            output = Input("Input")
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.type == "BRACKETS":
            if Parser.tokens.actual.value == "(":
                Parser.tokens.selectNext()
                output = Parser.parseRelExpression()

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

        elif Parser.tokens.actual.value in ["TRUE", "FALSE"]:
            output = BoolValue(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        else:
            raise ValueError("Parser Error (Factor): Token {} is invalid".format(repr(Parser.tokens.actual.value)))
        return output

    @staticmethod
    def parseType():
        if Parser.tokens.actual.type == "INTEGER":
            Parser.tokens.selectNext()
            return Type("INT")

        elif Parser.tokens.actual.type == "BOOLEAN":
            Parser.tokens.selectNext() 
            return Type("BOOLEAN")
            
        else:
            raise ValueError("Parser Error (Type): Token {} type is not supported".format(repr(Parser.tokens.actual.type)))

    @staticmethod
    def parseProgram():
        statements = []
        while Parser.tokens.actual.type != "EOF":
            if Parser.tokens.actual.type == "SUB":
                statements.append(Parser.parseSubDec())

            elif Parser.tokens.actual.type == "FUNCTION":
                statements.append(Parser.parseFuncDec())

            elif Parser.tokens.actual.type == "LINEFEED":
                Parser.tokens.selectNext()
                
            else:
                raise ValueError("Parser Error (program): Expected a SUB, FUNCTION or EOF, got token {}".format(repr(Parser.tokens.actual.value)))
        
        statements.append(FuncCall("MAIN", []))
        return Program("Program", statements)

    @staticmethod
    def run(code):
        st = SymbolTable(None)
        Parser.tokens = Tokenizer(PrePro.filtra(code))
        Parser.tokens.selectNext()
        res = Parser.parseProgram()

        Parser.tokens.selectNext()
        if Parser.tokens.actual.value != "EOF":
            raise ValueError("Run (EOF Check): Expected EOF, got token {}: {}".format(repr(Parser.tokens.actual.value), Parser.tokens.position))

        res.evaluate(st)
