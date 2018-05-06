import copy
import regex as re
import json

from exceptions import ValidationError
from hsm_types import State, Transition, Event, Action


__state_declaration_regex = r"((?P<comment>\".*\")\s*as\s+)?\s*?(?P<name>\w+)\s*"
__state_declaration = re.compile(__state_declaration_regex)
__nested_state_regex = r"state\s*" + \
                       __state_declaration_regex + \
                       r"(?P<body>\{((?:[^\{\}]|(?&body))*)\})"
__nested_state = re.compile(__nested_state_regex)

__start_end_point_regex = r"\[\*\]"
__start_end_point = re.compile(__start_end_point_regex)
__state_name_regex = r"(\[\*\]|\w+)"
__state_name = re.compile(__state_name_regex)
__arrow_regex = r"-(down|right|left|up)?-?>"
__arrow = re.compile(__arrow_regex)

__transition_regex = r"(?P<state_from>" + __state_name_regex + r")\s*?" + \
                     __arrow_regex + \
                     r"\s*?(?P<state_to>" + __state_name_regex + r")" + \
                     r"(\s*:\s*(?P<comment>.+))?"
__transition = re.compile(__transition_regex)
__event_regex = r"(?P<event>[\.\w]+)"
__action_regex = r"(?P<action_name>[\.\w]+)\s*\(\s*(?P<action_args>.*)\s*\)"
__condition_regex = r"\[\s*(?P<condition>.*)\s*\]"
__transition_meta_info_regex = __event_regex + r"\s*\/?\s*" + \
                               r"(" + __action_regex + r")?\s*" + \
                               r"(" + __condition_regex + r")?"
__transition_meta_info = re.compile(__transition_meta_info_regex)

__comment_regex = r"(\<\*\*(?P<comment>(\<\*\*(*PRUNE)(*FAIL)|.|\n)*?)\*\*\>)?"
__comment = re.compile(__comment_regex)
__type_regex = r"(?P<type>([\.\w]+)\s*(\[\])?)"
__parameter_regex = __comment_regex + \
                    r"\s*((" + __type_regex + r")\s+(?P<name>\w+)\s*)\s*"


def parse_transition(instructions, parent_state=None):
    """

    :param instructions:
    :param parent_state:
    :return:
    """
    states = set()
    transitions = set()
    transition_meta = __transition.finditer(instructions)
    for transition in transition_meta:
        from_state_name = transition.group('state_from')
        to_state_name = transition.group('state_to')
        comment = transition.group('comment')
        event = None
        action = None
        if comment is not None:
            transition_meta_info_meta = __transition_meta_info.match(comment)
            if transition_meta_info_meta is not None:
                owner_state = None
                full_event_name = transition_meta_info_meta.group('event')
                if full_event_name is not None:
                    index = str.rfind(full_event_name, '.')
                    event_name = full_event_name[index+1:]
                    if index != -1:
                        full_state_name = full_event_name[:index]
                        if full_state_name == '':
                            owner_state = parent_state
                        else:
                            state = State.states[full_state_name]
                            if parent_state == state or parent_state.is_child_of(state):
                                owner_state = state
                            else:
                                raise ValidationError()
                    event = Event(event_name, owner_state)
                owner_state = None
                full_action_name = transition_meta_info_meta.group('action_name')
                if full_action_name is not None:
                    index = str.rfind(full_action_name, '.')
                    action_name = full_action_name[index+1:]
                    if index != -1:
                        full_state_name = full_action_name[:index]
                        if full_state_name == '':
                            owner_state = parent_state
                        else:
                            state = State.states[full_state_name]
                            if parent_state == state or parent_state.is_child_of(state):
                                owner_state = state
                            else:
                                raise ValidationError()
                    action = Action(action_name, owner_state)
        from_state = State(from_state_name, parent_state)
        if from_state in states:
            states.remove(from_state)
            states.add(from_state)
        else:
            states.add(from_state)
        to_state = State(to_state_name, parent_state)
        if to_state in states:
            states.remove(to_state)
            states.add(to_state)
        else:
            states.add(to_state)
        transitions.add(Transition(from_state, to_state, event, action))
    return states, transitions


def parse_instructions(instructions, parent_state=None):
    """
    Parsing the platuml
    :param instructions:
    :param parent_state:
    :return:
    """
    states = set()
    transitions = set()
    simple_instructions = re.sub(__nested_state_regex, '', copy.copy(instructions))
    new_states, new_transitions = parse_transition(simple_instructions, parent_state)
    states.update(new_states)
    transitions.update(new_transitions)
    nested_state_meta = __nested_state.finditer(instructions)
    for nested_state in nested_state_meta:
        state_name = nested_state.group('name')
        state_comment = nested_state.group('comment')
        new_state = State(state_name, parent_state, state_comment)
        if new_state in states:
            states.remove(new_state)
            states.add(new_state)
        else:
            states.add(new_state)
        body = nested_state.group('body')
        new_states, new_transitions = parse_instructions(body, new_state)
        states.update(new_states)
        transitions.update(new_transitions)
    return states, transitions


def parse_uml_file(file_name):
    """
    Function for parsing PlantUML State Machine
    :param file_name: Name of file with State Machine
    :return: states, transitions: State and Transitions of State Machine
    """
    with open(file_name, 'r') as file:
        instructions = file.read()
        return parse_instructions(instructions)


if __name__ == '__main__':
    states, transitions = parse_uml_file('./TestFSM.txt')
    for state in states:
        print("=================")
        print("State name is " + state.name)
        if state.parent_state is not None:
            print("State parent is " + str(state.parent_state))
            print("State parent name is " + str(state.parent_state.name))
            print("State parent comment is " + str(state.parent_state.comment))
        print("State comment is " + str(state.comment))
        print("=================")
    for transition in transitions:
        print("Transition from: " + str(transition.from_state))
        print("Transition to: " + str(transition.to_state))
        print("Transition event: " + str(transition.event))
        print("Transition action: " + str(transition.action))

    # from subprocess import call
    # call(['java', '-jar', './plantuml.jar'])
