class State:
    """
    Object that responsible for storing state information
    """
    states = dict()

    def __init__(self, name, parent=None, comment=None):
        if parent is not None and name == '[*]':
            self.name = parent.name
            self.parent = parent.parent
            self.comment = parent.comment
        else:
            self.name = name
            self.parent = parent
            self.comment = comment
            State.states[str(self)] = self

    def is_child_of(self, state):
        parent = self.parent
        while parent is not None:
            if parent == state:
                return True
            else:
                parent = parent.parent
        else:
            return False

    def __str__(self):
        result = ""
        if self.parent is not None:
            result += str(self.parent) + '.'
        result += self.name
        return result

    def __eq__(self, other):
        return other is not None and \
               self.parent == other.parent and \
               self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.parent) ^ hash(self.name)


class Transition:
    """
    Object that responsible for storing transition information:
        Event, Action, Condition
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
    def __init__(self, name, *args):
        self.name = name


class Attribute:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class Operation:
    def __init__(self, name, type):
        pass