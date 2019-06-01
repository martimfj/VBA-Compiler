from symbol_table import SymbolTable

class Node():
    def __init__(self, value = None, children = None):
        self.value = value
        self.children = children

    def evaluate(self, st):
        pass

class BinOp(Node):
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
    def evaluate(self, st):
        return (self.value, "INT")

class Identifier(Node):
    def evaluate(self, st):
        return st.getter(self.value)

class Assigment(Node):
    def evaluate(self, st):
        declared_type = st.getter(self.children[0].value)[1]
        child_value, child_type = self.children[1].evaluate(st)

        if declared_type == child_type:
            st.setter(self.children[0].value, child_value)
        else:
            raise ValueError("AST Error (Assingment): Type mismatch: {}({}) = {}({}) ".format(self.children[0].value, declared_type, child_value, child_type))

class Program(Node):
    def evaluate(self, st):
        for child in self.children:
            child.evaluate(st)

class Print(Node):
    def evaluate(self, st):
        print(self.children[0].evaluate(st)[0])

class While(Node):
    def evaluate(self, st):
        _, relexp_type = self.children[0].evaluate(st)
        if relexp_type == "BOOLEAN":
            while self.children[0].evaluate(st)[0]: #Cannot use relexp_value
                for child in self.children[1]:
                    child.evaluate(st)
        else:
            raise ValueError("AST Error (While): {} is not a valid relational expression type".format(relexp_type))

class If(Node):
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
    def evaluate(self, st):
        try:
            return (int(input("Input: ")), "INT")
        except:
            raise ValueError("AST Error (Input): Only INT is a valid input type")

class BoolValue(Node):
    def evaluate(self, st):
        if self.value == "TRUE":
            return (True, "BOOLEAN")
        else:
            return (False, "BOOLEAN")

class VarDec(Node):
    def evaluate(self, st):
        st.declare(self.children[0].value, self.children[1].evaluate(st))

class Type(Node):
    def evaluate(self, st):
        return self.value

class FuncDec(Node):
    def evaluate(self, st):
        st.declare(self.value, "FUNCTION")
        st.setter(self.value, self)

class SubDec(Node):
    def evaluate(self, st):
        st.declare(self.value, "SUB")
        st.setter(self.value, self)

class FuncCall(Node):
    def evaluate(self, st):
        st = SymbolTable(st)
        decFunc, decFunc_type = st.getter(self.value)

        if decFunc_type == "SUB":
            if len(decFunc.children[:-1]) == len(self.children):
                for decVar, callVar in zip(decFunc.children[:-1], self.children):
                    decVar.evaluate(st)
                    st.setter(decVar.children[0].value, callVar.evaluate(st)[0])
            else:
                raise ValueError("AST Error (FuncCall): Expected {} arguments. got {}".format(len(decFunc.children[:-1]), len(self.children)))

            for statement in decFunc.children[-1]:
                statement.evaluate(st)

        elif decFunc_type == "FUNCTION":
            if len(decFunc.children[1:-1]) == len(self.children):
                decFunc.children[0].evaluate(st)
                for decVar, callVar in zip(decFunc.children[1:-1], self.children):
                    decVar.evaluate(st)
                    st.setter(decVar.children[0].value, callVar.evaluate(st)[0])

            else:
                raise ValueError("AST Error (FuncCall): Expected {} arguments. got {}".format(len(decFunc.children[:-1]), len(self.children)))

            for statement in decFunc.children[-1]:
                statement.evaluate(st)
            
            return st.getter(decFunc.children[0].children[0].value)

class NoOp(Node):
    def evaluate(self, st):
        pass