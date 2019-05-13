class Node():
    def __init__(self):
        self.value = None
        self.children = []

    def evaluate(self, st):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        children = [child.evaluate(st) for child in self.children]
        child_value = [child[0] for child in children]
        child_type = [child[1] for child in children]

        if child_type[0] == "INT" and child_type[1] == "INT":
            if self.value == "-":
                return (child_value[0] - child_value[1], "INT")
            elif self.value == "+":
                return (child_value[0] + child_value[1], "INT")
            elif self.value == "*":
                return (child_value[0] * child_value[1], "INT")
            elif self.value == "/":
                return (child_value[0] // child_value[1], "INT")
            elif self.value == ">":
                return (child_value[0] > child_value[1], "BOOLEAN")
            elif self.value == "<":
                return (child_value[0] < child_value[1], "BOOLEAN")
            elif self.value == "=":
                return (child_value[0] == child_value[1], "BOOLEAN")

        elif child_type[0] == "BOOLEAN" and child_type[1] == "BOOLEAN":
            if self.value == "=":
                return (child_value[0] == child_value[1], "BOOLEAN")
            elif self.value == "OR":
                return (child_value[0] or child_value[1], "BOOLEAN")
            elif self.value == "AND":
                return (child_value[0] and child_value[1], "BOOLEAN")
        else:
            raise ValueError("AST Error (BinOp): Operation can not be performed: {} {} {} ".format(child_value[0], self.value, child_value[1]))

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        child_value, child_type = self.children[0].evaluate(st)

        if child_type == "INT" and self.value == "-":
            return (-child_value, "INT")
        elif child_type == "INT" and self.value == "+":
            return (child_value, "INT")
        elif child_type == "BOOLEAN" and self.value == "NOT":
            return (not child_value, "BOOLEAN")
        else:
            raise ValueError("AST Error (UnOp): Operation can not be performed: {} {} ".format(self.value, child_value))

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, st):
        return (self.value, "INT")

class Indentifier(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, st):
        return st.getter(self.value)

class Assigment(Node):
    """
    Value: "="
    Children: [Identifier (String), Value (Boolean or Int)]

    Usage: Assigment("=", [identifier, Parser.parseRelExpression()])
    """

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        declared_type = st.getter(self.children[0].value)[1]
        child_value, child_type = self.children[1].evaluate(st)

        if declared_type == child_type:
            st.setter(self.children[0].value, child_value)
        else:
            raise ValueError("AST Error (Assingment): Type mismatch: {}({}) = {}({}) ".format(self.children[0].value, declared_type, child_value, child_type))

class Program(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        for child in self.children:
            child.evaluate(st)

class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        print(self.children[0].evaluate(st)[0])

class While(Node):
    """
    Value: "WHILE"
    Children: [BinOp (Boolean), Statements]

    Usage: While("WHILE", [rel_exp, statements]) 
    """
    
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        _, relexp_type = self.children[0].evaluate(st)
        if relexp_type == "BOOLEAN":
            while self.children[0].evaluate(st)[0]: #Cannot use relexp_value
                for child in self.children[1]:
                    child.evaluate(st)
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

    def evaluate(self, st):
        relexp_value, relexp_type = self.children[0].evaluate(st)

        if relexp_type == "BOOLEAN":
            if relexp_value:
                for child in self.children[1]:
                    child.evaluate(st)
            else:
                if self.children[2] is not None:
                    for child in self.children[2]:
                        child.evaluate(st)

        else:
            raise ValueError("AST Error (If): {} is not a valid relational expression type".format(relexp_type))

class Input(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, st):
        try:
            return (int(input("Input: ")), "INT")
        except:
            raise ValueError("AST Error (Input): Only INT is a valid input type")

class BoolValue(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, st):
        if self.value == "TRUE":
            return (True, "BOOLEAN")
        else:
            return (False, "BOOLEAN")

class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        st.declare(self.children[0].value, self.children[1].evaluate(st))

class Type(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, st):
        return self.value

class NoOp(Node):
    def __init__(self):
        pass

    def evaluate(self, st):
        pass