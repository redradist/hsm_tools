import regex as re

from fsm_tools.parsers.expression_ast import Value, Symbol, Operator, Indexer, Sequence, String, Object, Lambda, \
    FunctionCall, Function, Expression
from fsm_tools.exceptions import ValidationError


symbol_expr = r'(?P<symbol>[_A-Za-z][_A-Za-z0-9]*)'
symbol_regex = re.compile(symbol_expr)

value_expr = r'(?P<value>[^\s]+)'
value_regex = re.compile(value_expr)

group_expr = r'\((?P<group_body>(.|\s)*)\)'
group_regex = re.compile(group_expr)

object_construction_expr = symbol_expr + \
                           r'\{(?P<args>(.|\s)*)\}'
object_construction_regex = re.compile(object_construction_expr)

c_like_param_expr = symbol_expr + \
                  r'\s+' + \
                  symbol_expr
c_like_param_regex = re.compile(c_like_param_expr)

rust_like_param_expr = symbol_expr + \
                     r'\s*:\s*' + \
                     symbol_expr
rust_like_param_regex = re.compile(rust_like_param_expr)

function_call_expr = symbol_expr + \
                     r'\((?P<args>(.|\s)*)\)'
function_call_regex = re.compile(function_call_expr)

function_declaration_expr = symbol_expr + \
                            r'(\((?P<params>(.|\s)*)\)\s*(->\s*' + \
                            r'(?P<return_type>' + symbol_expr + r')?' \
                            r')?)?\s*?\{(?P<function_body>(.|\s)*)\}'
function_declaration_regex = re.compile(function_declaration_expr)

method_call_expr = symbol_expr + \
                   r'(\.|->)' + \
                   symbol_expr + \
                   r'\((?P<args>(.|\s)*)\)'
method_call_regex = re.compile(method_call_expr)

method_declaration_expr = r'([a-zA-Z$][a-zA-Z_$0-9]*(\.|->))?' + \
                          symbol_expr + \
                          r'(\((?P<args>(.|\s)*)\)\s*(->\s*' + \
                          r'(?P<return_type>' + symbol_expr + r')?' \
                          r')?)?\s*?\{(?P<function_body>(.|\s)*)\}'
method_declaration_regex = re.compile(method_declaration_expr)

lambda_declaration_expr = r'(\((?P<args>(.|\s)*)\)\s*(->\s*' + \
                          r'(?P<return_type>' + symbol_expr + r')?' \
                          r')?)?\s*?\{(?P<lambda_body>(.|\s)*)\}'
lambda_declaration_regex = re.compile(lambda_declaration_expr)


class ExpressionParser:
    class _ParserContext:
        def __init__(self, parser):
            self._parser = parser

        def __enter__(self):
            self._parser._contexts = []
            self._parser._parse_item = None
            self._parser._parse_buffer = []
            self._parser._num_of_open_braces = 0
            self._parser._num_of_open_parentheses = 0
            self._parser._num_of_open_square_bracket = 0

        def __exit__(self, exc_type, exc_val, exc_tb):
            del self._parser._parse_item
            del self._parser._parse_buffer
            del self._parser._num_of_open_braces
            del self._parser._num_of_open_parentheses
            del self._parser._num_of_open_square_bracket

    def __init__(self, statement):
        self._statement = statement
        self._expr = Sequence()

        with ExpressionParser._ParserContext(self) as context:
            for ch in self._statement:
                self._parse_expr(ch)
            # NOTE(redra): Currently workaround to finish parsing statement
            self._parse_expr(' ')
            self._expr = self.get_most_inner_expr(self._expr)

    @property
    def expression(self):
        return self._expr

    def get_ast(self):
        return self.expression

    def is_name(self, value):
        return not value[0].isdigit()

    def is_operator_char(self, ch):
        return any(ch in operator for operator in ExpressionParser._operators)

    def is_operator(self, ch):
        return ch in ['->', '=', '==', '===', '!=', '!==',
                      '>', '>=', '<', '<=', '&', '&&',
                      '|', '||', '^', '*', '**', '%',
                      '!', '~', '+', '++', '-', '--',
                      '+=', '-=', '|=', '&=', '/', '//']

    def is_group_operator(self, ch):
        return ch in ['(', ')']

    def is_function_body_operator(self, ch):
        return ch in ['{', '}']

    def is_index_operator(self, ch):
        return ch in ['[', ']']

    def is_string_operator(self, ch):
        return ch in ['\'', '\"']

    def is_first_name_letter(self, ch):
        return ch.isalpha() or ch == '_' or ch == ':'

    def is_name_letter(self, ch):
        return ch.isalnum() or ch == '_' or ch == ':'

    def parse_text(self, ch):
        if self.is_name_letter(ch):
            self._parse_buffer.append(ch)
        elif len(self._parse_buffer) > 0:
            if type(self._expr[-1]) == Expression:
                attrib = self._expr[-1][-1]
            else:
                attrib = self._expr[-1]
            attrib.name = ''.join(self._parse_buffer)
            self._parse_buffer = []
            self._parse_expr(ch)

    def parse_string(self, ch):
        self._parse_buffer.append(ch)
        if len(self._parse_buffer) > 1 and \
                ((self._parse_buffer[0] == '\'' and ch == '\'') or \
                 (self._parse_buffer[0] == '\"' and ch == '\"')):
            del self._parse_buffer[0]
            del self._parse_buffer[-1]
            self._expr.append(String(''.join(self._parse_buffer)))
            self._parse_buffer = []

    def parse_number(self, ch):
        if ch.isdigit():
            self._parse_buffer.append(ch)
        elif not ch.isalpha():
            self._expr.append(Value(''.join(self._parse_buffer)))
            self._parse_buffer = []
            self._parse_expr(ch)
        else:
            raise ValidationError()

    def parse_operator(self, ch):
        if self.is_operator_char(ch):
            self._parse_buffer.append(ch)
        elif self.is_operator(''.join(self._parse_buffer)):
            if self._parse_buffer[0] == '-' and self._parse_buffer[1] == '>':
                if len(self._expr) > 0 and isinstance(self._expr[-1], FunctionCall):
                    if self.is_name_letter(ch) or ch == ' ':
                        if not hasattr(self, 'return_value'):
                            self.return_value = ''
                        self.return_value += ch
                    else:
                        func = self._expr[-1]
                        func = Function(func.name, func.object, *func.args)
                        self._expr[-1] = func
                        return_value = self.return_value.strip()
                        if ' ' in return_value:
                            raise ValidationError()
                        if len(return_value) != 0:
                            func.return_value = return_value
                        self._parse_buffer = []
                        self._parse_expr(ch)
                elif len(self._expr) > 0 and isinstance(self._expr[-1], Expression):
                    if self.is_name_letter(ch) or ch == ' ':
                        if not hasattr(self, 'return_value'):
                            self.return_value = ''
                        self.return_value += ch
                    else:
                        group = self._expr[-1]
                        body = ''.join(self._parse_buffer)
                        anon_func = Lambda(*group._items, body=body)
                        return_value = self.return_value.strip()
                        if ' ' in return_value:
                            raise ValidationError()
                        if len(return_value) != 0:
                            anon_func.return_value = return_value
                        self._expr[-1] = anon_func
                        self._parse_buffer = []
                        self._parse_expr(ch)
                else:
                    raise ValidationError()
            else:
                self._expr.append(Operator(''.join(self._parse_buffer)))
                self._parse_buffer = []
                self._parse_expr(ch)
        else:
            raise ValidationError()

    def parse_indexer(self, ch):
        self._parse_buffer.append(ch)
        if ch == '[':
            self._num_of_open_square_bracket += 1
        elif ch == ']':
            self._num_of_open_square_bracket -= 1
            if self._num_of_open_square_bracket == 0:
                del self._parse_buffer[0]
                del self._parse_buffer[-1]
                indexer = self._expr[-1]
                parser = ExpressionParser(''.join(self._parse_buffer))
                indexer.expression = parser.get_ast()
                if not indexer.expression:
                    raise ValidationError()
                self._parse_buffer = []

    def get_most_inner_expr(self, expression):
        if isinstance(expression, Sequence) and len(expression) == 1:
            return self.get_most_inner_expr(Expression(expression[0]))
        elif isinstance(expression, Expression) and len(expression) == 1:
            return self.get_most_inner_expr(expression[0])
        else:
            return expression

    def parse_function_call(self, ch):
        self._parse_buffer.append(ch)
        if ch == ')':
            del self._parse_buffer[0]
            del self._parse_buffer[-1]
            parser = ExpressionParser(''.join(self._parse_buffer))
            expression = parser.get_ast()
            if issubclass(type(expression), Expression) and len(expression) <= 1:
                self._expr[-1].args = list(expression)
            else:
                self._expr[-1].args = [expression]
            self._parse_buffer = []

    def parse_group(self, ch):
        self._parse_buffer.append(ch)
        if ch == '(':
            self._num_of_open_braces += 1
        elif ch == ')':
            self._num_of_open_braces -= 1
            if self._num_of_open_braces == 0:
                del self._parse_buffer[0]
                del self._parse_buffer[-1]
                parser = ExpressionParser(''.join(self._parse_buffer))
                expression = parser.get_ast()
                self._expr.append(expression)
                self._parse_buffer = []

    def parse_function(self, ch):
        self._parse_buffer.append(ch)
        if ch == '{':
            self._num_of_open_parentheses += 1
        elif ch == '}':
            self._num_of_open_parentheses -= 1
            if self._num_of_open_parentheses == 0:
                del self._parse_buffer[0]
                del self._parse_buffer[-1]
                if len(self._expr) > 0 and isinstance(self._expr[-1], Function):
                    func = self._expr[-1]
                    func.body = ''.join(self._parse_buffer)
                elif len(self._expr) > 0 and isinstance(self._expr[-1], FunctionCall):
                    func = self._expr[-1]
                    func = Function(func.name, func.object, *func.args)
                    self._expr[-1] = func
                    func.body = ''.join(self._parse_buffer)
                elif len(self._expr) > 0 and isinstance(self._expr[-1], Expression):
                    group = self._expr[-1]
                    body = ''.join(self._parse_buffer)
                    anon_func = Lambda(*group._items, body=body)
                    self._expr[-1] = anon_func
                elif len(self._expr) > 0 and type(self._expr[-1]) == Symbol:
                    attrib = self._expr[-1]
                    parser = ExpressionParser(''.join(self._parse_buffer))
                    expression = parser.get_ast()
                    attrib.args = list(expression) if isinstance(expression, Expression) else [expression]
                else:
                    raise ValidationError()
                self._parse_buffer = []

    def parse_object(self, ch):
        self._parse_buffer.append(ch)
        if ch == '}':
            del self._parse_buffer[0]
            del self._parse_buffer[-1]
            if len(self._expr) > 0 and type(self._expr[-1]) == Function:
                func = self._expr[-1]
                func.body = ''.join(self._parse_buffer)
            else:
                raise ValidationError()
            self._parse_buffer = []

    def parse_comma(self, ch):
        # Do nothing for comma operator
        pass

    _operators = ['=', '==', '===', '!=', '!==',
                  '>', '>=', '<', '<=', '&', '&&',
                  '|', '||', '^', '*', '**', '%',
                  '!', '~', '+', '++', '-', '--',
                  '+=', '-=', '|=', '&=', '/', '//',
                  '->']

    _context = {
        'Comma': parse_comma,
        'Text': parse_text,
        'String': parse_string,
        'Number': parse_number,
        'Operator': parse_operator,
        'Indexer': parse_indexer,
        'FunctionCall': parse_function_call,
        'Group': parse_group,
        'Function': parse_function,
        'Object': parse_object,
    }

    def _context_analyzer(self, ch, contexts):
        if ch == ',':
            contexts.append('Comma')
            self._expr.append(self.get_most_inner_expr(self._expr))
        elif self.is_first_name_letter(ch):
            contexts.append('Text')
            if len(self._expr) == 0 or \
                    type(self._expr[-1]) != Symbol or \
                    self._expr[-1].object == None or \
                    self._expr[-1].name != None:
                if len(self._expr) > 0 and \
                        type(self._expr[-1]) == Expression and \
                        type(self._expr) != Sequence:
                    self._expr[-1].append(Symbol(None))
                else:
                    self._expr.append(Symbol(None))
        elif ch.isdigit():
            contexts.append('Number')
        elif self.is_operator_char(ch):
            contexts.append('Operator')
        elif len(self._expr) > 0 and \
                type(self._expr[-1]) == Symbol and \
                ch == '.':
            contexts.append('Text')
            old_attrib = self._expr[-1]
            obj = Object(old_attrib.name)
            attrib = Symbol(None)
            attrib.object = obj
            self._expr[-1] = attrib
        elif len(self._expr) > 0 and \
                type(self._expr[-1]) == Symbol and \
                self.is_group_operator(ch):
            contexts[-1] = 'FunctionCall'
            if len(self._expr) > 0 and type(self._expr[-1]) == Symbol:
                attr = self._expr[-1]
                func = FunctionCall(attr.name)
                self._expr[-1] = func
                func.object = attr.object
        elif self.is_function_body_operator(ch):
            contexts.append('Function')
        elif self.is_group_operator(ch):
            contexts.append('Group')
        elif self.is_string_operator(ch):
            contexts.append('String')
        elif self.is_index_operator(ch):
            contexts.append('Indexer')
            if len(self._expr) > 0 and type(self._expr[-1]) == Symbol:
                attr = self._expr[-1]
                self._expr[-1] = Indexer(attr)
            else:
                raise ValidationError()
        else:
            raise ValidationError()

    @staticmethod
    def _only_one_true(list):
        return [bool(i) for i in list].count(True) == 1

    @staticmethod
    def _more_than_one_true(list):
        return [bool(i) for i in list].count(True) > 1

    @staticmethod
    def check_all_equal(list):
        return all(i == list[0] for i in list)

    @staticmethod
    def _get_ast_item(parse_item):
        reg = parse_item.re
        if reg == group_regex:
            return None
        elif reg == object_construction_regex:
            return None
        elif reg == function_declaration_regex:
            symbol = parse_item.group('symbol')
            params = parse_item.group('params').split(',')
            parsed_param_meta = list()
            for param in params:
                c_like_param = c_like_param_regex.match(param)
                rust_like_param = rust_like_param_regex.match(param)
                parsed_param_meta.append((c_like_param, rust_like_param))
            ExpressionParser.check_all_equal(parsed_param_meta)
            return Function(symbol, *params)
        elif reg == function_call_regex:
            symbol = parse_item.group('symbol')
            args = parse_item.group('args').split(',')
            for arg in args:
                num_arg = symbol_regex.findall(arg)
                if len(num_arg) > 1:
                    raise ValidationError(msg='num_arg has len {} bigger than 1'.format(len(num_arg)))
                num_arg = value_regex.findall(arg)
                if len(num_arg) > 1:
                    raise ValidationError(msg='num_arg has len {} bigger than 1'.format(len(num_arg)))
            return FunctionCall(symbol, *list(Symbol(arg) if symbol_regex.match(arg) else Value(arg) for arg in args))
        elif reg == lambda_declaration_regex:
            return Lambda()
        else:
            raise ValueError()

    def _handle_letter(self, ch):
        self._parse_buffer.append(ch)
        str_parse_buffer = ''.join(self._parse_buffer)
        match_regex = [object_construction_regex.match(str_parse_buffer),
                       function_declaration_regex.match(str_parse_buffer),
                       function_call_regex.match(str_parse_buffer),
                       method_declaration_regex.match(str_parse_buffer),
                       method_call_regex.match(str_parse_buffer),
                       lambda_declaration_regex.match(str_parse_buffer),
                       group_regex.match(str_parse_buffer),]
        # if ExpressionParser._more_than_one_true(match_regex):
        #     raise ValidationError(msg='Ambiguity error !!')

        if any(match_regex):
            for reg in match_regex:
                if reg:
                    self._parse_item = reg
                    if self._parse_item:
                        self._expr = self._get_ast_item(self._parse_item)
                    break
        # elif not symbol_regex.match(str_parse_buffer):
        #     raise ValidationError(msg='No matched expression !!')

    def _parse_expr(self, ch):
        if len(self._parse_buffer) > 0 or ch != ' ':
            self._handle_letter(ch)

    def _simplify_expr(self, saver, expression):
        if expression and type(expression) == Expression:
            if len(expression) == 1:
                saver(expression[0])
            else:
                index = 0
                first_entry = False
                for subexpr in expression:
                    if not first_entry:
                        first_entry = True
                    else:
                        index += 1
                    self._simplify_expr(lambda obj: expression.__setitem__(index, obj), subexpr)
        return
