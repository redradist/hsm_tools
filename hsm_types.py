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
    def __init__(self, from_state, to_state, event=None, action=None):
        self.from_state = from_state
        self.to_state = to_state
        self.event = event
        self.action = action

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
    def __init__(self, name, owner=None, *args):
        self.name = name
        self.owner = owner

    def __str__(self):
        result = ""
        if self.owner is not None:
            result += str(self.owner) + '.'
        result += self.name
        return result


class Attribute:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class Operation:
    def __init__(self, name, type):
        pass