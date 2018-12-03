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

    @staticmethod
    def create_state(name, parent_state=None, comment=None):
        state_name = State.get_state_name(name, parent_state)
        if state_name in State.states:
            return State.states[state_name]
        else:
            parent_state = State.get_parent_state(name, parent_state)
            comment = State.get_state_comment_name(name, parent_state, comment)
            new_state = State(state_name, parent_state, comment)
            State.states[state_name] = new_state
            return new_state

    @staticmethod
    def get_state_name(name, parent_state=None):
        if parent_state is not None and name == '[*]':
            return parent_state.name
        else:
            return name

    @staticmethod
    def get_parent_state(name, parent_state=None):
        if parent_state is not None and name == '[*]':
            return parent_state.parent_state
        else:
            return parent_state

    @staticmethod
    def get_state_comment_name(name, parent_state=None, comment=None):
        if parent_state is not None and name == '[*]':
            return parent_state.comment
        else:
            return comment

    def __init__(self, name, parent_state=None, comment=None):
        self.sub_states = set()
        self.transitions = set()
        self.attributes = set()
        self.actions = set()
        self.name = name
        self.parent_state = parent_state
        self.comment = comment
        if parent_state is not None:
            parent_state.sub_states.add(self)

    def _get_sorted_transitions(self, transitions, predicate):
        event_condition_transitions = []
        event_transitions = []
        simple_transitions = []
        for transition in transitions:
            if predicate(transition):
                if transition.event is not None:
                    if transition.condition is not None:
                        event_condition_transitions.append(transition)
                    else:
                        event_transitions.append(transition)
                else:
                    simple_transitions.append(transition)
        return event_condition_transitions + event_transitions + simple_transitions

    def initial_transitions(self):
        return self._get_sorted_transitions(self.transitions, lambda t: t.from_state == self)

    def final_transitions(self):
        return self._get_sorted_transitions(self.transitions, lambda t: t.to_state == self)

    def internal_transitions(self):
        external_transitions = set()
        external_transitions.update(self.initial_transitions())
        external_transitions.update(self.final_transitions())
        internal_transitions = self.transitions.difference(external_transitions)
        return self._get_sorted_transitions(internal_transitions, lambda t: True)

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
        # if self.parent_state is not None:
        #     result += str(self.parent_state) + '.'
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
    def __init__(self, from_state, to_state, event=None, call_actions=None, condition=None):
        self.from_state = from_state
        self.to_state = to_state
        self.event = event
        self.call_actions = call_actions
        self.condition = condition

    def __eq__(self, other):
        return other is not None and \
               self.from_state == other.from_state and \
               self.to_state == other.to_state and \
               self.event == other.event and \
               self.call_actions == other.call_action and \
               self.condition == other.condition

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.from_state) ^ \
               hash(self.to_state) ^ \
               hash(not self.event or tuple(self.event)) ^ \
               hash(not self.call_actions or tuple(self.call_actions)) ^ \
               hash(not self.condition or tuple(self.condition))


class Sequence(Expression):
    def __init__(self, expression):
        Expression.__init__(self)
        if isinstance(expression, Expression):
            self._items = expression._items
        else:
            self._items = [expression]

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
    def __init__(self, name, object=None, *args):
        self.object = object
        self.name = name
        self.args = args

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
        return result


class Function:
    def __init__(self, name, object=None, *params, body=None, return_value=None):
        self.object = object
        self.name = name
        self.params = params
        self.return_value = return_value
        self.body = body
        self.lang = None

    def __str__(self):
        result = ''
        if self.object:
            result += str(self.object) + '.'
        result += str(self.name)
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
