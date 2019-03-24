_author__ = "Martim Ferreira José"
__version__ = "2.0.1"
__license__ = "MIT"

class Node():
    def __init__(self):
        self.value = None
        self.children = []

    def evaluate(self):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self):
        if self.value == "-":
            return self.children[0].evaluate() - self.children[1].evaluate()
        elif self.value == "+":
            return self.children[0].evaluate() + self.children[1].evaluate()
        elif self.value == "*":
            return self.children[0].evaluate() * self.children[1].evaluate()
        elif self.value == "/":
            return self.children[0].evaluate() // self.children[1].evaluate()
        
class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self):
        if self.value == "-":
            return - self.children[0].evaluate()
        elif self.value == "+":
            return self.children[0].evaluate()

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

class NoOp(Node):
    def __init__(self):
        pass

    def evaluate(self):
        pass 