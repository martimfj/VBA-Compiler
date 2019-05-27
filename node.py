from assembler import Assembler

class Node():
    i = 0
    def __init__(self):
        self.value = None
        self.children = []
        self.id = Node.newID()

    def evaluate(self, st):
        pass

    @staticmethod
    def newID():
        Node.i += 1
        return Node.i

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def evaluate(self, st):
        child_r = self.children[0].evaluate(st)
        Assembler.write_line("PUSH EBX")

        child_l = self.children[1].evaluate(st)
        Assembler.write_line("POP EAX")
        Assembler.clean_line()

        if child_r[1] == child_l[1]:
            if self.value == "-":
                Assembler.write_line("SUB EAX, EBX      ; Subtraction: {} - {}".format(child_r[0], child_l[0]))
                Assembler.write_line("MOV EBX, EAX")
                Assembler.clean_line()
                return (child_r[0] - child_l[0], "INT")

            elif self.value == "+":
                Assembler.write_line("ADD EAX, EBX      ; Addition: {} + {}".format(child_r[0], child_l[0]))
                Assembler.write_line("MOV EBX, EAX")
                Assembler.clean_line()
                return (child_r[0] + child_l[0], "INT")

            elif self.value == "*":
                Assembler.write_line("IMUL EBX          ; Multiplication: {} * {}".format(child_r[0], child_l[0]))
                Assembler.write_line("MOV EBX, EAX")
                Assembler.clean_line()
                return (child_r[0] * child_l[0], "INT")

            elif self.value == "/":
                Assembler.write_line("IDIV EBX          ; Division: {} / {}".format(child_r[0], child_l[0]))
                Assembler.write_line("MOV EBX, EAX")
                Assembler.clean_line()
                return (child_r[0] // child_l[0], "INT")

            elif self.value == ">":
                Assembler.write_line("CMP EAX, EBX      ; Greater-than: {} > {}".format(child_r[0], child_l[0]))
                Assembler.write_line("CALL binop_jg")
                Assembler.clean_line()
                return (child_r[0] > child_l[0], "BOOLEAN")

            elif self.value == "<":
                Assembler.write_line("CMP EAX, EBX      ; Less-than: {} < {}".format(child_r[0], child_l[0]))
                Assembler.write_line("CALL binop_jl")
                Assembler.clean_line()
                return (child_r[0] < child_l[0], "BOOLEAN")

            elif self.value == "=":
                Assembler.write_line("CMP EAX, EBX      ; Equal: {} == {}".format(child_r[0], child_l[0]))
                Assembler.write_line("CALL binop_je")
                Assembler.clean_line()
                return (child_r[0] == child_l[0], "BOOLEAN")

            elif self.value == "OR":
                Assembler.write_line("OR EAX, EBX       ; Or: {} | {}".format(child_r[0], child_l[0]))
                Assembler.write_line("MOV EBX, EAX")
                Assembler.clean_line()
                return (child_r[0] or child_l[0], "BOOLEAN")

            elif self.value == "AND":
                Assembler.write_line("AND EAX, EBX      ; And: {} & {}".format(child_r[0], child_l[0]))
                Assembler.write_line("MOV EBX, EAX")
                Assembler.clean_line()
                return (child_r[0] and child_l[0], "BOOLEAN")
        else:
            raise ValueError("AST Error (BinOp): Operation can not be performed: {} {} {} ".format(child_r[0], self.value, child_l[0]))

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def evaluate(self, st):
        child = self.children[0].evaluate(st)
        child_value = child[0]
        child_type = child[1]

        if child_type == "INT" and self.value == "-":
            # Assembler.write_line("NEG EAX           ; Negativize: -{}".format(child_value))
            return (-child_value, "INT")

        elif child_type == "INT" and self.value == "+":
            return (child_value, "INT")

        elif child_type == "BOOLEAN" and self.value == "NOT":
            if child_value == True:
                Assembler.write_line("MOV EBX, False    ; Negation: !{}".format(child_value))
                return (child_value, "BOOLEAN")
            else:
                Assembler.write_line("MOV EBX, True     ; Negation: !{}".format(child_value))
                return (not child_value, "BOOLEAN")
        else:
            raise ValueError("AST Error (UnOp): Operation can not be performed: {} {} ".format(self.value, child_value))

class IntVal(Node):
    def __init__(self, value):
        self.value = value
        self.id = Node.newID()

    def evaluate(self, st):
        Assembler.clean_line()
        Assembler.write_line("MOV EBX, {}".format(self.value))
        return (self.value, "INT")

class Identifier(Node):
    def __init__(self, value):
        self.value = value
        self.id = Node.newID()

    def evaluate(self, st):
        child_value, child_type, offset = st.getter(self.value)
        Assembler.write_line("MOV EBX, [EBP-{}]".format(offset))
        return child_value, child_type, offset

class Assigment(Node):
    """
    Value: "="
    Children: [Identifier (String), Value (Boolean or Int)]

    Usage: Assigment("=", [identifier, Parser.parseRelExpression()])
    """

    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def evaluate(self, st):
        _, declared_type, offset = st.getter(self.children[0].value)
        child_value, child_type = self.children[1].evaluate(st)
        st.setter(self.children[0].value, child_value, child_type)
        Assembler.write_line("MOV [EBP-{}], EBX  ; {} = {} ".format(offset, self.children[0].value, child_value))

class Program(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def evaluate(self, st):
        for child in self.children:
            child.evaluate(st)

class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def evaluate(self, st):
        self.children[0].evaluate(st)
        Assembler.write_line("PUSH EBX")
        Assembler.write_line("CALL print")
        Assembler.write_line("POP EBX")
        Assembler.clean_line()

class While(Node):
    """
    Value: "WHILE"
    Children: [BinOp (Boolean), Statements]

    Usage: While("WHILE", [rel_exp, statements]) 
    """
    
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def evaluate(self, st):
        # _, relexp_type = self.children[0].evaluate(st)
        Assembler.clean_line()
        Assembler.write_line("LOOP_{}:".format(self.id))
        _, relexp_type = self.children[0].evaluate(st)
        
        if relexp_type == "BOOLEAN":
            Assembler.write_line("CMP EBX, False")
            Assembler.write_line("JE EXIT_{}".format(self.id))
            for child in self.children[1]:
                child.evaluate(st)
            Assembler.write_line("JMP LOOP_{}".format(self.id))
            Assembler.write_line("EXIT_{}:".format(self.id))
            Assembler.clean_line()
        else:
            raise ValueError("AST Error (While): {} is not a valid relational expression type".format(relexp_type))
class If(Node):
    """
    Value: "IF"
    Children: [BinOp (Boolean), list(Statements)] or [BinOp (Boolean), list(Statements), list(Statements)]

    Usage: 
    1) If("IF", [rel_exp, statements_if, statements_else])
    2) If("IF", [rel_exp, statements_if])
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def evaluate(self, st):
        relexp_type = self.children[0].evaluate(st)[1]
        
        if relexp_type == "BOOLEAN":
            if self.children[2] is not None:
                Assembler.write_line("CMP EBX, False")
                Assembler.write_line("JE ELSE_{}".format(self.id))
                for child in self.children[1]:
                    child.evaluate(st)
                Assembler.write_line("JMP EXIT_{}".format(self.id))
                Assembler.write_line("ELSE_{}:".format(self.id))
                for child in self.children[2]:
                    child.evaluate(st)
                Assembler.write_line("EXIT_{}:".format(self.id))
            else:
                Assembler.write_line("CMP EBX, False")
                Assembler.write_line("JE EXIT_{}".format(self.id))
                for child in self.children[1]:
                    child.evaluate(st)
                Assembler.write_line("EXIT_{}:".format(self.id))
        else:
            raise ValueError("AST Error (If): {} is not a valid relational expression type".format(relexp_type))

class Input(Node):
    def __init__(self, value):
        self.value = value
        self.id = Node.newID()

    def evaluate(self, st):
        try:
            input_value = int(input("Input: "))
            Assembler.write_line("MOV EBX, {}".format(input_value))
            return (input_value, "INT")
        except:
            raise ValueError("AST Error (Input): Only INT is a valid input type")

class BoolValue(Node):
    def __init__(self, value):
        self.value = value
        self.id = Node.newID()

    def evaluate(self, st):
        if self.value == "TRUE":
            Assembler.clean_line()
            Assembler.write_line("MOV EBX, {}".format("True"))
            return (True, "BOOLEAN")
        else:
            Assembler.write_line("MOV EBX, {}".format("False"))
            return (False, "BOOLEAN")

class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def evaluate(self, st):
        ident = self.children[0].value

        st.declare(ident, self.children[1].evaluate(st))
        child_value, child_type, offset = st.getter(ident)
        Assembler.write_line("PUSH DWORD 0      ; Dim {} as {} - [EBP−{}]".format(ident, child_type, offset))

class Type(Node):
    def __init__(self, value):
        self.value = value
        self.id = Node.newID()

    def evaluate(self, st):
        return self.value

class NoOp(Node):
    def __init__(self):
        pass

    def evaluate(self, st):
        pass