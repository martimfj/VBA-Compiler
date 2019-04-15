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
        if self.value == "-":
            return self.children[0].evaluate(st) - self.children[1].evaluate(st)
        elif self.value == "+":
            return self.children[0].evaluate(st) + self.children[1].evaluate(st)
        elif self.value == "*":
            return self.children[0].evaluate(st) * self.children[1].evaluate(st)
        elif self.value == "/":
            return self.children[0].evaluate(st) // self.children[1].evaluate(st)
        elif self.value == ">":
            return self.children[0].evaluate(st) > self.children[1].evaluate(st)
        elif self.value == "<":
            return self.children[0].evaluate(st) < self.children[1].evaluate(st)
        elif self.value == "=":
            return self.children[0].evaluate(st) == self.children[1].evaluate(st)
        elif self.value == "OR":
            return self.children[0].evaluate(st) or self.children[1].evaluate(st)
        elif self.value == "AND":
            return self.children[0].evaluate(st) and self.children[1].evaluate(st)

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        if self.value == "-":
            return - self.children[0].evaluate(st)
        elif self.value == "+":
            return self.children[0].evaluate(st)
        elif self.value == "NOT":
            return not self.children[0].evaluate(st)

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, st):
        return self.value

class Indentifier(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, st):
        return st.getter(self.value)

class Assigment(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        st.setter(self.children[0].value, self.children[1].evaluate(st))

class Statements(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        for child in self.children: #for statement in statements
            child.evaluate(st)

class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        print(self.children[0].evaluate(st))

class While(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        while self.children[0].evaluate(st):
            self.children[1].evaluate(st)

class If(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        if self.children[0].evaluate(st):
            self.children[1].evaluate(st)
        else:
            if self.children[2] is not None:
                self.children[2].evaluate(st)

class Input(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, st):
        return int(input())

class NoOp(Node):
    def __init__(self):
        pass

    def evaluate(self, st):
        pass