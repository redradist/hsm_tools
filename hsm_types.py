from exceptions import ValidationError


class State:
    """
    Object that responsible for storing state information
    """
    states = dict()

    def __init__(self, name, parent_state=None, comment=None):
        if parent_state is not None and name == '[*]':
            self.name = parent_state.name
            self.parent_state = parent_state.parent_state
            self.comment = parent_state.comment
        else:
            self.name = name
            self.parent_state = parent_state
            self.comment = comment
            State.states[str(self)] = self

    def is_child_of(self, state):
        parent_state = self.parent_state
        while parent_state is not None:
            if parent_state == state:
                return True
            else:
                parent_state = parent_state.parent_state
        else:
            return False

    def __str__(self):
        result = ""
        if self.parent_state is not None:
            result += str(self.parent_state) + '.'
        result += self.name
        return result

    def __eq__(self, other):
        return other is not None and \
               self.parent_state == other.parent_state and \
               self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.parent_state) ^ hash(self.name)


class Transition:
    """
    Object that responsible for storing transition information:
        From State, To State, Event, Action, Condition
    """
    def __init__(self, from_state, to_state, event=None, action=None, condition=None):
        self.from_state = from_state
        self.to_state = to_state
        self.event = event
        self.action = action
        self.condition = condition

    def __eq__(self, other):
        return other is not None and \
               self.from_state == other.from_state and \
               self.to_state == other.to_state

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.from_state) ^ hash(self.to_state)


class Event:
    """
    Object that responsible for storing event information:
        State owner
    """
    def __init__(self, name, owner=None):
        self.name = name
        self.owner = owner

    def __str__(self):
        result = ""
        if self.owner is not None:
            result += str(self.owner) + '.'
        result += self.name
        return result


class Action:
    def __init__(self, name, *args, owner=None):
        self.name = name
        self.args = args
        self.owner = owner

    def __str__(self):
        result = ""
        if self.owner is not None:
            result += str(self.owner) + '.'
        result += self.name
        result += '(' + ', '.join(str(arg) for arg in self.args) + ')'
        return result


class Group:
    def __init__(self, values):
        self.values = values


class Attribute:
    def __init__(self, name):
        self.name = name
        self.indexer = None


class Function:
    def __init__(self, name):
        self.name = name
        self.args = None


class String:
    def __init__(self, name):
        self.name = name

class Indexer:
    def __init__(self, attribute):
        self.attribute = attribute
        self.parts = []


class Operation:
    def __init__(self, name):
        self.name = name


class Value:
    def __init__(self, value):
        self.value = value


class Condition:
    def __init__(self, statement, owner=None):
        self.statement = statement
        self.owner = owner
        self.exp_parts = []
        self.exp_parts = self.parse(statement)

    def parse(self, statement):
        exp_parts = []
        is_parsing_complex = False

        temp = []
        for ch in statement:
            if len(temp) == 0 and ch != ' ':
                temp.append(ch)
            else:
                if ''.join(temp).isdigit() and ch.isalpha():
                    raise ValidationError()
                elif not ch.isdigit() and not ch.isalpha() and not is_parsing_complex:
                    parsed_text = ''.join(temp)
                    if parsed_text.isdigit():
                        exp_parts.append(Value(parsed_text))
                        temp = []
                    elif parsed_text.isalnum():
                        exp_parts.append(Attribute(parsed_text))
                        temp = []
                    elif self.is_single_operator(parsed_text) and \
                        not self.is_single_operator(ch):
                        exp_parts.append(Operation(parsed_text))
                        temp = []
                    elif self.is_single_operator(ch):
                        temp.append(ch)
                else:
                    temp.append(ch)

                if self.is_index_operator(ch):
                    if ch == ']' and (len(temp) == 0 or temp[0] != '['):
                        raise ValidationError()
                    if not is_parsing_complex:
                        temp.append(ch)
                    is_parsing_complex = True
                    if ch == ']':
                        is_parsing_complex = False
                        if len(exp_parts) == 0 or type(exp_parts[-1]) != Attribute:
                            raise ValidationError()
                        attr = exp_parts[-1]
                        del temp[0]; del temp[-1]
                        new_exp_parts = self.parse(''.join(chr for chr in temp))
                        if len(new_exp_parts) == 0:
                            raise ValidationError()
                        attr.index = Indexer(new_exp_parts)
                        temp = []
                elif self.is_group_operator(ch):
                    if ch == ')' and (len(temp) == 0 or temp[0] != '('):
                        raise ValidationError()
                    is_parsing_complex = True
                    if ch == ')':
                        is_parsing_complex = False
                        attr = None
                        if len(exp_parts) != 0 and type(exp_parts[-1]) == Attribute:
                            attr = exp_parts[-1]
                        del temp[0]; del temp[-1]
                        new_exp_parts = self.parse(''.join(chr for chr in temp))
                        if attr:
                            attr.callable_args = new_exp_parts
                        else:
                            exp_parts.append(Group(new_exp_parts))
                        temp = []
                elif self.is_string_operator(ch):
                    if ch == '\'' and len(temp) != 0 and temp[0] != '\'':
                        raise ValidationError()
                    if ch == '\"' and len(temp) != 0 and temp[0] != '\"':
                        raise ValidationError()
                    is_parsing_complex = True
                    if (temp[0] != '\'' and ch == '\'') or \
                       (temp[0] != '\"' and ch == '\"'):
                        is_parsing_complex = False
                        exp_parts.append(Attribute(temp))
                        temp = []

        parsed_text = ''.join(temp)
        if parsed_text.isdigit():
            exp_parts.append(Value(parsed_text))
        elif parsed_text.isalnum():
            exp_parts.append(Attribute(parsed_text))
        elif self.is_single_operator(parsed_text) and \
                not self.is_single_operator(ch):
            exp_parts.append(Operation(parsed_text))
        elif self.is_index_operator(ch):
            if ch == ']' and (len(temp) == 0 or temp[0] != '['):
                raise ValidationError()
            if not is_parsing_complex:
                temp.append(ch)
            if ch == ']':
                if len(exp_parts) == 0 or type(exp_parts[-1]) != Attribute:
                    raise ValidationError()
                attr = exp_parts[-1]
                del temp[0]; del temp[-1]
                new_exp_parts = self.parse(''.join(chr for chr in temp))
                if len(new_exp_parts) == 0:
                    raise ValidationError()
                attr.index = Indexer(new_exp_parts)
        elif self.is_group_operator(ch):
            if ch == ')' and (len(temp) == 0 or temp[0] != '('):
                raise ValidationError()
            if ch == ')':
                attr = None
                if len(exp_parts) != 0 and type(exp_parts[-1]) == Attribute:
                    attr = exp_parts[-1]
                del temp[0]; del temp[-1]
                new_exp_parts = self.parse(''.join(chr for chr in temp))
                if attr:
                    attr.callable_args = new_exp_parts
                else:
                    exp_parts.append(Group(new_exp_parts))
        elif self.is_string_operator(ch):
            if ch == '\'' and len(temp) != 0 and temp[0] != '\'':
                raise ValidationError()
            if ch == '\"' and len(temp) != 0 and temp[0] != '\"':
                raise ValidationError()
            if (temp[0] != '\'' and ch == '\'') or \
               (temp[0] != '\"' and ch == '\"'):
                exp_parts.append(Attribute(temp))

        return exp_parts

    def is_name(self, value):
        return not value[0].isdigit()

    def is_single_operator(self, ch):
        return ch in ['=', '==', '===', '!=', '!==',
                      '>', '>=', '<', '<=', '&', '&&',
                      '|', '||', '^', '*', '**', '%',
                      '!', '~', '+', '++', '-', '--',
                      '+=', '-=', '|=', '&=', '/', '//']

    def is_group_operator(self, ch):
        return ch in ['(', ')']

    def is_index_operator(self, ch):
        return ch in ['[', ']']

    def is_string_operator(self, ch):
        return ch in ['\'', '\"']

    def is_valid(self, tags):
        return any(self.is_method(tag) or \
                   self.is_value(tag) or \
                   self.is_name(tag) or \
                   self.is_single_operator(tag) or \
                   self.is_pair_operator(tag)
                   for tag in tags)
        pass

    def __str__(self):
        result = ""
        if self.owner is not None:
            result += str(self.owner) + '.'
        result += self.statement
        return result


if __name__ == '__main__':
    example = 'k > 0 && isAction()'
    condition = Condition(example)
    print(condition)
    example = 'k > 0 || isAction()'
    condition = Condition(example)
    print(condition)
    example = 'k >= 0 || isAction()'
    condition = Condition(example)
    print(condition)
    example = 'k == 0 || isAction()'
    condition = Condition(example)
    print(condition)
    example = 'k === 0 || isAction()'
    condition = Condition(example)
    print(condition)
    example = 'k === 0 || isAction(ad, gt)'
    condition = Condition(example)
    print(condition)
    example = 'k[1] === 0 || isAction(ad, gt)'
    condition = Condition(example)
    print(condition)
    example = 'k === 0 || isAction(ad, gt, gf)'
    condition = Condition(example)
    print(condition)

