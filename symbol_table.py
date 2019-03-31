class SymbolTable():
    def __init__(self):
        self.table = {}

    def getter(self, variable):
        if variable in self.table.keys():
            return self.table[variable]
        else:
            raise ValueError("SymbolTable Error: Variable {} does not exist".format(variable))

    def setter(self, variable, value):
        self.table[variable] = value