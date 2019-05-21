class SymbolTable():
    """Data structure to store information about variable names, values and types.

    table =	{ "variable_name": [variable_value, variable_type] }
    """

    def __init__(self):
        self.table = {}
        self.size = 0

    def declare(self, variable_name, variable_type):
        """Define the variable name, type and offset in the table.

        Arguments:
            variable_name {string}
            variable_type {string} -- "BOOLEAN" or "INT"

        Raises:
            ValueError: If variable_name already in dictionary.
        """

        if variable_name not in self.table.keys():
            self.size += 1
            self.table[variable_name] = [None, variable_type, self.size * 4]
        else:
            raise ValueError("Symbol Table Error: Variable {} already declared".format(variable_name))

    def getter(self, variable_name):
        """Return tuple with variable value, type and offset.

        Arguments:
            variable_name {string}

        Raises:
            ValueError: If variable_name does not exist in dictionary.
        """

        if variable_name in self.table.keys():
            return tuple(self.table[variable_name])
        else:
            raise ValueError("Symbol Table Error: Variable {} does not exist".format(variable_name))

    def setter(self, variable_name, variable_value, variable_type):
        """Initialize a value for the variable.

        Arguments:
            variable_name {string}
            variable_value {int, boolean}

        Raises:
            ValueError: If variable_name does not exist in dictionary.
        """

        if variable_name in self.table.keys():
            if self.table[variable_name][1] == variable_type:
                self.table[variable_name][0] = variable_value
            else:
                raise ValueError("Symbol Table Error (Setter): Type mismatch: {}({}) = {}({}) ".format(variable_name, self.table[variable_name][2], variable_value, variable_type))
        else:
            raise ValueError("Symbol Table Error (Setter): Variable {} not declared".format(variable_name))