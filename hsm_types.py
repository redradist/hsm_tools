class State:
    states = dict()

    """
    Object that responsible for storing state information
    """
    def __init__(self, name, parent=None, comment=None):
        if parent is not None and name == '[*]':
            self.name = parent.name
            self.parent = parent.parent
            self.comment = parent.comment
        else:
            self.name = name
            self.parent = parent
            self.comment = comment
            State.states[name] = self

    def __eq__(self, other):
        return other is not None and \
               self.parent == other.parent and \
               self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.parent) ^ hash(self.name)


class Transition:
    def __init__(self, from_state, to_state, comment=None):
        self.from_state = from_state
        self.to_state = to_state
        self.comment = comment

    def __eq__(self, other):
        return other is not None and \
               self.from_state == other.from_state and \
               self.to_state == other.to_state

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.from_state) ^ hash(self.to_state)


class Event:
    def __init__(self, name):
        pass


class Action:
    def __init__(self, name):
        pass


class Attribute:
    def __init__(self, name, type):
        pass


class Operation:
    def __init__(self, name, type):
        pass