import copy
import regex as re
import json

from exceptions import ValidationError
from hsm_types import State, Transition, Event, Action, Condition

_state_declaration_regex = r"((?P<comment>\".*\")\s*as\s+)?\s*?(?P<name>\w+)\s*"
_state_declaration = re.compile(_state_declaration_regex)
_nested_state_regex = r"state\s*" + \
                       _state_declaration_regex + \
                       r"(?P<body>\{((?:[^\{\}]|(?&body))*)\})"
_nested_state = re.compile(_nested_state_regex)

_start_end_point_regex = r"\[\*\]"
_start_end_point = re.compile(_start_end_point_regex)
_state_name_regex = r"(\[\*\]|[\.\d\w]+)"
_state_name = re.compile(_state_name_regex)
_arrow_regex = r"-(down|right|left|up)?-?>"
_arrow = re.compile(_arrow_regex)

_transition_regex = r"(?P<state_from>" + _state_name_regex + r")\s*?" + \
                     _arrow_regex + \
                     r"\s*?(?P<state_to>" + _state_name_regex + r")" + \
                     r"(\s*:\s*(?P<comment>.+))?"
_transition = re.compile(_transition_regex)
_event_regex = r"(?P<event>[\.\w]+)"
_action_regex = r"(?P<action_name>[\.\w]+)\s*\(\s*(?P<action_args>.*)\s*\)"
_action = re.compile(_action_regex)
_actions_regex = r"(?P<actions>(" + _action_regex + r")+)"
_condition_regex = r"\[\s*(?P<condition>.*)\s*\]"
_transition_meta_info_regex = _event_regex + r"\s*\/?\s*" + \
                               r"(" + _actions_regex + r")?\s*" + \
                               r"(" + _condition_regex + r")?"
_transition_meta_info = re.compile(_transition_meta_info_regex)

_comment_regex = r"(\<\*\*(?P<comment>(\<\*\*(*PRUNE)(*FAIL)|.|\n)*?)\*\*\>)?"
_comment = re.compile(_comment_regex)
_type_regex = r"(?P<type>([\.\w]+)\s*(\[\])?)"
_parameter_regex = _comment_regex + \
                    r"\s*((" + _type_regex + r")\s+(?P<name>\w+)\s*)\s*"


class PlantUMLParser:

    def parse_transition(self, instructions, parent_state=None):
        """

        :param instructions:
        :param parent_state:
        :return:
        """
        states = set()
        transitions = set()
        transition_meta = _transition.finditer(instructions)
        for transition in transition_meta:
            from_state_name = transition.group('state_from')
            to_state_name = transition.group('state_to')
            comment = transition.group('comment')
            event = None
            actions = []
            condition = None
            if comment is not None:
                transition_meta_info = _transition_meta_info.match(comment)
                if transition_meta_info is not None:
                    owner_state = None
                    full_event_name = transition_meta_info.group('event')
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
                    all_actions = transition_meta_info.group('actions')
                    if all_actions:
                        all_actions = all_actions.split(',')
                        for action in all_actions:
                            action = action.strip()
                            action_info = _action.match(action)
                            if action_info:
                                print("actions_info =", action_info)
                                full_action_name = action_info.group('action_name')
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
                                    actions.append(Action(action_name, owner=owner_state))
                    full_condition = transition_meta_info.group('condition')
                    if full_condition is not None:
                        condition = Condition(full_condition, owner_state)
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
            transitions.add(Transition(from_state, to_state, event, actions, condition))
        return states, transitions

    def parse_condition(self):
        pass

    def parse_instructions(self, instructions, parent_state=None):
        """
        Parsing the platuml
        :param instructions:
        :param parent_state:
        :return:
        """
        states = set()
        transitions = set()
        simple_instructions = re.sub(_nested_state_regex, '', copy.copy(instructions))
        new_states, new_transitions = self.parse_transition(simple_instructions, parent_state)
        states.update(new_states)
        transitions.update(new_transitions)
        nested_state_meta = _nested_state.finditer(instructions)
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
            new_states, new_transitions = self.parse_instructions(body, new_state)
            states.update(new_states)
            transitions.update(new_transitions)
        return states, transitions


    def parse_uml_file(self, file_name):
        """
        Function for parsing PlantUML State Machine
        :param file_name: Name of file with State Machine
        :return: states, transitions: State and Transitions of State Machine
        """
        with open(file_name, 'r') as file:
            instructions = file.read()
            return self.parse_instructions(instructions)


if __name__ == '__main__':
    parser = PlantUMLParser()
    states, transitions = parser.parse_uml_file('./tests/data/TestFSM.txt')
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
        print("Transition condition: " + str(transition.condition))

    # from subprocess import call
    # call(['java', '-jar', './plantuml.jar'])
