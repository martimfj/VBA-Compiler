class SymbolTable():
    def __init__(self, ancestor):
        self.table = {}
        self.ancestor = ancestor

    def declare(self, variable_name, variable_type):
        if variable_name not in self.table.keys():
            self.table[variable_name] = [None, variable_type]
        else:
            raise ValueError("Symbol Table Error: Variable {} already declared".format(variable_name))

    def getter(self, variable_name):
        if variable_name in self.table.keys():
            return tuple(self.table[variable_name])
        elif self.ancestor != None:
            return self.ancestor.getter(variable_name)
        else:
            raise ValueError("Symbol Table Error: Variable {} does not exist".format(variable_name))

    def setter(self, variable_name, variable_value):
        if variable_name in self.table.keys():
            self.table[variable_name][0] = variable_value
        else:
            raise ValueError("Symbol Table Error: Variable {} not declared".format(variable_name))