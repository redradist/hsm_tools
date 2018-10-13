from src.fsm_types import Value, Attribute, Operator, Indexer, Group, String, Function, Object, Expression
from src.exceptions import ValidationError


class ExpressionParser:
    def __init__(self, statement):
        self._statement = statement
        self._expressions = Expression()
        self._subexpressions = Expression()

    _operators = [ '=', '==', '===', '!=', '!==',
                   '>', '>=', '<', '<=', '&', '&&',
                   '|', '||', '^', '*', '**', '%',
                   '!', '~', '+', '++', '-', '--',
                   '+=', '-=', '|=', '&=', '/', '//',
                   '->']

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
            self.temp.append(ch)
        elif len(self.temp) > 0:
            attrib = self._expressions[-1]
            attrib.name = ''.join(self.temp)
            self.temp = []
            self._parse_expression(ch)

    def parse_string(self, ch):
        self.temp.append(ch)
        if len(self.temp) > 1 and \
           ((self.temp[0] == '\'' and ch == '\'') or \
            (self.temp[0] == '\"' and ch == '\"')):
            del self.temp[0]
            del self.temp[-1]
            self._expressions.append(String(''.join(self.temp)))
            self.temp = []

    def parse_number(self, ch):
        if ch.isdigit():
            self.temp.append(ch)
        elif not ch.isalpha():
            self._expressions.append(Value(''.join(self.temp)))
            self.temp = []
            self._parse_expression(ch)
        else:
            raise ValidationError()

    def parse_operator(self, ch):
        if self.is_operator_char(ch):
            self.temp.append(ch)
        elif self.is_operator(''.join(self.temp)):
            if self.temp[0] == '-' and self.temp[1] == '>':
                if len(self._expressions) > 0 and type(self._expressions[-1]) == Function:
                    if self.is_name_letter(ch) or ch == ' ':
                        if not hasattr(self, 'return_value'):
                            self.return_value = ''
                        self.return_value += ch
                    else:
                        func = self._expressions[-1]
                        return_value = self.return_value.strip()
                        if ' ' in return_value:
                            raise ValidationError()
                        if len(return_value) != 0:
                            func.return_value = return_value
                        self.temp = []
                        self._parse_expression(ch)
                elif len(self._expressions) > 0 and type(self._expressions[-1]) == Group:
                    if self.is_name_letter(ch) or ch == ' ':
                        if not hasattr(self, 'return_value'):
                            self.return_value = ''
                        self.return_value += ch
                    else:
                        args = self._expressions[-1]
                        anon_func = Function(None)
                        anon_func.args = args
                        anon_func.body = ''.join(self.temp)
                        return_value = self.return_value.strip()
                        if ' ' in return_value:
                            raise ValidationError()
                        if len(return_value) != 0:
                            anon_func.return_value = return_value
                        self._expressions[-1] = anon_func
                        self.temp = []
                        self._parse_expression(ch)
                else:
                    raise ValidationError()
            else:
                self._expressions.append(Operator(''.join(self.temp)))
                self.temp = []
                self._parse_expression(ch)
        else:
            raise ValidationError()

    def parse_indexer(self, ch):
        self.temp.append(ch)
        if ch == '[':
            self.num_of_open_square_bracket += 1
        elif ch == ']':
            self.num_of_open_square_bracket -= 1
            if self.num_of_open_square_bracket == 0:
                del self.temp[0]
                del self.temp[-1]
                indexer = self._expressions[-1]
                parser = ExpressionParser(''.join(self.temp))
                indexer.expression = parser.parse()
                if not indexer.expression:
                    raise ValidationError()
                self.temp = []

    def parse_function(self, ch):
        self.temp.append(ch)
        if ch == ')':
            del self.temp[0]
            del self.temp[-1]
            parser = ExpressionParser(''.join(self.temp))
            expression = parser.parse()
            self._expressions[-1].args = list(expression) if isinstance(expression, Expression) else [expression]
            self.temp = []

    def parse_group(self, ch):
        self.temp.append(ch)
        if ch == '(':
            self.num_of_open_braces += 1
        elif ch == ')':
            self.num_of_open_braces -= 1
            if self.num_of_open_braces == 0:
                del self.temp[0]
                del self.temp[-1]
                parser = ExpressionParser(''.join(self.temp))
                expression = parser.parse()
                self._expressions.append(Group(expression))
                self.temp = []

    def parse_function_body(self, ch):
        self.temp.append(ch)
        if ch == '{':
            self.num_of_open_perentesis += 1
        elif ch == '}':
            self.num_of_open_perentesis -= 1
            if self.num_of_open_perentesis == 0:
                del self.temp[0]
                del self.temp[-1]
                if len(self._expressions) > 0 and type(self._expressions[-1]) == Function:
                    func = self._expressions[-1]
                    func.body = ''.join(self.temp)
                elif len(self._expressions) > 0 and type(self._expressions[-1]) == Group:
                    args = self._expressions[-1]
                    anon_func = Function(None)
                    anon_func.args = args
                    anon_func.body = ''.join(self.temp)
                    self._expressions[-1] = anon_func
                elif len(self._expressions) > 0 and type(self._expressions[-1]) == Attribute:
                    attrib = self._expressions[-1]
                    parser = ExpressionParser(''.join(self.temp))
                    expression = parser.parse()
                    attrib.args = list(expression) if isinstance(expression, Expression) else [expression]
                else:
                    raise ValidationError()
                self.temp = []

    def parse_object(self, ch):
        self.temp.append(ch)
        if ch == '}':
            del self.temp[0]
            del self.temp[-1]
            if len(self._expressions) > 0 and type(self._expressions[-1]) == Function:
                func = self._expressions[-1]
                func.body = ''.join(self.temp)
            else:
                raise ValidationError()
            self.temp = []

    def parse_comma(self, ch):
        # Do nothing for comma operator
        pass

    _context = {
        'Comma': parse_comma,
        'Text': parse_text,
        'String': parse_string,
        'Number': parse_number,
        'Operator': parse_operator,
        'Indexer': parse_indexer,
        'Function': parse_function,
        'Group': parse_group,
        'FunctionBody': parse_function_body,
        'Object': parse_object,
    }

    def _context_analyzer(self, ch, contexts):
        if ch == ',':
            contexts.append('Comma')
            self._subexpressions.append(self._expressions)
            self._expressions = Expression()
        elif self.is_first_name_letter(ch):
            contexts.append('Text')
            if len(self._expressions) == 0 or \
                type(self._expressions[-1]) != Attribute or \
                self._expressions[-1].object == None or \
                self._expressions[-1].name != None:
                self._expressions.append(Attribute(None))
        elif ch.isdigit():
            contexts.append('Number')
        elif self.is_operator_char(ch):
            contexts.append('Operator')
        elif len(self._expressions) > 0 and \
            type(self._expressions[-1]) == Attribute and \
            ch == '.':
            contexts.append('Text')
            old_attrib = self._expressions[-1]
            obj = Object(old_attrib.name)
            attrib = Attribute(None)
            attrib.object = obj
            self._expressions[-1] = attrib
        elif len(self._expressions) > 0 and \
            type(self._expressions[-1]) == Attribute and \
            self.is_group_operator(ch):
            contexts[-1] = 'Function'
            if len(self._expressions) > 0 and type(self._expressions[-1]) == Attribute:
                attr = self._expressions[-1]
                func = Function(attr.name)
                func.object = attr.object
                self._expressions[-1] = func
        elif self.is_function_body_operator(ch):
            contexts.append('FunctionBody')
        elif self.is_group_operator(ch):
            contexts.append('Group')
        elif self.is_string_operator(ch):
            contexts.append('String')
        elif self.is_index_operator(ch):
            contexts.append('Indexer')
            if len(self._expressions) > 0 and type(self._expressions[-1]) == Attribute:
                attr = self._expressions[-1]
                self._expressions[-1] = Indexer(attr)
            else:
                raise ValidationError()
        else:
            raise ValidationError()

    def _handle_letter(self, ch):
        current_context = self.contexts[-1]
        if ExpressionParser._context[current_context] == 'Number' and ch.isalpha():
            raise ValidationError()

        ExpressionParser._context[current_context](self, ch)

    def _parse_expression(self, ch):
        if len(self.temp) == 0:
            if ch != ' ':
                self._context_analyzer(ch, self.contexts)
                self._handle_letter(ch)
        else:
            self._handle_letter(ch)

    def _simplify_expression(self, saver, expression):
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
                    self._simplify_expression(lambda obj: expression.__setitem__(index, obj), subexpr)
        return

    @property
    def expressions(self):
        if len(self._subexpressions) > 0:
            if len(self._expressions) > 0:
                self._subexpressions.append(self._expressions)
                self._expressions = Expression()
            self._simplify_expression(lambda obj: setattr(self, '_subexpressions', obj),
                                      self._subexpressions)
            return self._subexpressions if len(self._subexpressions) != 1 else self._subexpressions[0]
        else:
            self._simplify_expression(lambda obj: setattr(self, '_expression', obj),
                                      self._expressions)
            return self._expressions if len(self._expressions) != 1 else self._expressions[0]

    def parse(self):
        self.contexts = []
        self.temp = []
        self.num_of_open_braces = 0
        self.num_of_open_perentesis = 0
        self.num_of_open_square_bracket = 0
        self.num_char = 0
        for ch in self._statement:
            self.num_char += 1
            self._parse_expression(ch)

        # NOTE(redrad): Currently workaround to finish parsing statement
        self._parse_expression(' ')
        return self.expressions


if __name__ == '__main__':
    example = "Action2(int k)"
    parser = ExpressionParser(example)
    condition = parser.parse()
    print(condition)

    example = 'k == isAction(arg0, arg1) -> bool { arg0 = arg1; return arg0; }'
    parser = ExpressionParser(example)
    condition = parser.parse()
    print(condition)

    example = 'MyNameSpace::isAction(arg0 == 1, arg1) == k'
    parser = ExpressionParser(example)
    condition = parser.parse()
    print(condition)

    example = 'MyNameSpace::isAction(arg0, arg1) == k'
    parser = ExpressionParser(example)
    condition = parser.parse()
    print(condition)

    example = 'name.isAction(arg0, arg1) == k'
    parser = ExpressionParser(example)
    condition = parser.parse()
    print(condition)

    example = 'k == isAction(arg0, arg1) { arg0 = arg1; }'
    parser = ExpressionParser(example)
    condition = parser.parse()
    print(condition)

    example = 'k > 0 && isAction(arg0, arg1)'
    parser = ExpressionParser(example)
    condition = parser.parse()
    print(condition)

    example = 'k[1] > 0 || isAction()'
    parser = ExpressionParser(example)
    condition = parser.parse()
    print(condition)
