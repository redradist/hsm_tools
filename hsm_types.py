from exceptions import ValidationError


class Expression:
    def __init__(self):
        self._items = []

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
        self.body = None
        self.owner = owner

    def __str__(self):
        result = ""
        if self.owner is not None:
            result += str(self.owner) + '.'
        result += self.name
        result += '(' + ', '.join(str(arg) for arg in self.args) + ')'
        return result


class Group(Expression):
    def __init__(self, expression):
        if type(expression) == Expression:
            self._items = expression._items
        else:
            self._items = [ expression ]

    def __str__(self):
        result = '(' + ', '.join(str(item) for item in self.items) + ')'
        return result


class Attribute:
    def __init__(self, name):
        self.object = None
        self.name = name

    def __str__(self):
        result = ''
        if self.object:
            result += str(self.object) + '.'
        result += str(self.name)
        return result


class Object:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)


class Function:
    def __init__(self, name):
        self.object = None
        self.name = name
        self.args = None
        self.return_value = None
        self.body = None

    def __str__(self):
        result = ''
        if self.object:
            result += str(self.object) + '.'
        result += str(self.name)
        result += '('
        arg_str = ''
        for arg in self.args:
            if len(arg_str) != 0:
                arg_str += ', '
            arg_str += str(arg)
        result += arg_str
        result += ')'
        if self.return_value:
            result += ' -> ' + self.return_value + ' '
        if self.body:
            result += '{' + self.body + '}'
        return result


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
        return str(self.name)


class Condition:
    def __init__(self, statement, exp_parts, owner=None):
        self.statement = statement
        self.owner = owner
        self.exp_parts = exp_parts

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

