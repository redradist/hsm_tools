class Expression:
    def __init__(self, *items):
        self._items = list(*items)

    def append(self, value):
        self._items.append(value)

    def remove(self, value):
        self._items.remove(value)

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item):
        return item in self._items

    def __setitem__(self, key, value):
        if key >= len(self._items):
            raise ValueError('key index is bigger than items in Expression')

        self._items[key] = value

    def __getitem__(self, key):
        if key >= len(self._items):
            raise ValueError('key index is bigger than items in Expression')

        return self._items[key]

    def __len__(self):
        return len(self._items)

    def __str__(self):
        result = ""
        for item in self._items:
            if len(result) > 0:
                result += ' '
            result += str(item)
        return result


class Sequence(Expression):
    def __init__(self, complete=False):
        Expression.__init__(self)
        self.complete = complete

    def __str__(self):
        result = '(' + ', '.join(str(item) for item in self._items) + ')'
        return result


class Symbol:
    def __init__(self, name, object=None, *symbols):
        self.object = object
        self.name = name
        self.symbols = list(symbols)
        self.attr_type = None

    def is_complex(self):
        return self.symbols is not None and len(self.symbols) > 0

    def get_import_modules_for(self, language):
        if language == 'c' or language == 'C':
            if self.attr_type == 'String':
                return '#include <string.h>'
        elif language == 'cxx' or \
             language == 'cpp' or \
             language == 'Cxx' or \
             language == 'Cpp' or \
             language == 'c++' or \
             language == 'C++':
                return '#include <string>'

    def get_type_for(self, language):
        if language == 'c' or language == 'C':
            if self.attr_type == 'String':
                return 'const char *'
            else:
                return self.attr_type
        elif language == 'cxx' or \
             language == 'cpp' or \
             language == 'Cxx' or \
             language == 'Cpp' or \
             language == 'c++' or \
             language == 'C++':
            if self.attr_type == 'String':
                return 'std::string'
            elif self.attr_type == 'Boolean':
                return 'bool'
            elif self.attr_type == 'Number':
                return 'double'
            elif self.attr_type == 'Integer':
                return 'int'
            elif self.attr_type == 'Float':
                return 'float'
            elif self.attr_type == 'Double':
                return 'double'
            else:
                return self.attr_type
        else:
            return 'Unknown'

    def __str__(self):
        result = ''
        if self.object:
            result += str(self.object) + '.'
        result += str(self.name)
        result += '{'
        if self.symbols:
            symbol_str = ''
            for symbol in self.symbols:
                if len(symbol_str) != 0:
                    symbol_str += ', '
                    symbol_str += str(symbol)
            result += symbol_str
        result += '}'
        return result


class Object:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)


class FunctionCall:
    """
    Object that responsible for storing event information:
        State owner
    """
    def __init__(self, name, *args):
        self.name = name
        self.args = args

    def __str__(self):
        result = str(self.name)
        result += '('
        arg_str = ''
        for arg in self.args:
            if len(arg_str) != 0:
                arg_str += ', '
            arg_str += str(arg)
        result += arg_str
        result += ')'
        return result


class MethodCall(FunctionCall):
    """
    Object that responsible for storing event information:
        State owner
    """
    def __init__(self, name, object=None, *args):
        FunctionCall.__init__(self, name, *args)
        self.object = object

    def __str__(self):
        result = ''
        if self.object:
            result += str(self.object) + '.'
        result += FunctionCall.__str__(self)
        return result


class Function:
    def __init__(self, name, *params, body=None, return_value=None):
        self.name = name
        self.params = params
        self.return_value = return_value
        self.body = body
        self.lang = None

    def __str__(self):
        result = str(self.name)
        result += '('
        params_str = ''
        for param in self.params:
            if len(params_str) != 0:
                params_str += ', '
                params_str += str(param)
        result += params_str
        result += ')'
        if self.return_value:
            result += ' -> ' + self.return_value + ' '
        if self.body:
            result += '{' + self.body + '}'
        return result


class Method(Function):
    def __init__(self, name, object=None, *params, body=None, return_value=None):
        Function.__init__(self, name, *params, body, return_value)
        self.object = object

    def __str__(self):
        result = ''
        if self.object:
            result += str(self.object) + '.'
        result += Function.__str__(self)
        return result


class Lambda(Function):
    """
    Object that representing anonymous Function
    """
    def __init__(self, *args, body=None, return_value=None):
        super().__init__(None,
                         None,
                         *args,
                         body=body,
                         return_value=return_value)


class String:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)


class Indexer:
    def __init__(self, attribute):
        self.attribute = attribute
        self.expression = []


class Operator:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)


class Value:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Condition(Expression):
    def __init__(self, statement, exp_parts, owner=None):
        Expression.__init__(self, *exp_parts)
        self.statement = statement
        self.owner = owner

    def __str__(self):
        result = ""
        if self.owner is not None:
            result += str(self.owner) + '.'
        result += self.statement
        return result
