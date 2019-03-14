from fsm_tools.parsers.expression_ast import Symbol


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


class Event(Symbol):
    """
    Object that responsible for storing event information:
        State owner
    """
    def __init__(self, symbol):
        if not isinstance(symbol, Symbol):
            raise TypeError('symbol is not Symbol type')
        super().__init__(symbol.name,
                         symbol.object,
                         *symbol.symbols)


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
