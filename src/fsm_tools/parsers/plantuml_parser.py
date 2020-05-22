import copy
import regex as re

from fsm_tools.parsers.expression_ast import Expression
from fsm_tools.parsers.expression_parser import ExpressionParser
from fsm_tools.parsers.transition_parser import TransitionParser
from fsm_tools.fsm_types import State, Transition, Event

''
'EvConfig / isAction(arg0, arg1) \n { arg0 = arg1;  [ arg0 == arg1 ] } //'

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
# _event_regex = r"(?P<event_name>[\.\w]+)\s*?\(\s*?(?P<event_args>.*?)\s*?\)"
# _action_regex = r"(?P<action_name>[\.\w]+)\s*\(\s*(?P<action_args>.*)\s*\)"
# _action = re.compile(_action_regex)
# _actions_regex = r"(?P<actions>(" + _action_regex + r")+)"
# _condition_regex = r"\[\s*(?P<condition>.*)\s*\]"
# _transition_meta_info_regex = _event_regex + r"\s*\/?\s*" + \
#                                r"(" + _actions_regex + r")?\s*" + \
#                                r"(" + _condition_regex + r")?"
# _transition_meta_info = re.compile(_transition_meta_info_regex)

_comment_regex = r"(\<\*\*(?P<comment>(\<\*\*(*PRUNE)(*FAIL)|.|\n)*?)\*\*\>)?"
_comment = re.compile(_comment_regex)
_type_regex = r"(?P<type>([\.\w]+)\s*(\[\])?)"
_parameter_regex = _comment_regex + \
                    r"\s*((" + _type_regex + r")\s+(?P<name>\w+)\s*)\s*"


def _find_least_common_acesentor(root, states=[]):
    if root is None:
        return None

    if root in states:
        return root

    least_common_acesentors = set()
    for sub_state in root.sub_states:
        acesentor = _find_least_common_acesentor(sub_state, states)
        least_common_acesentors.add(acesentor)

    if len(least_common_acesentors) > 0 and root.sub_states == least_common_acesentors:
        if len(least_common_acesentors) == 1:
            return least_common_acesentors.pop()
        else:
            return root
    else:
        return None


class PlantUMLParser:

    def _parse_events(self, events):
        parser = ExpressionParser(events)
        expression = parser.get_ast()
        return [Event(exp) for exp in expression] if isinstance(expression, Expression) else [Event(expression)]

    def _parse_actions(self, actions):
        parser = ExpressionParser(actions)
        expression = parser.get_ast()
        return [exp for exp in expression] if isinstance(expression, Expression) else [expression]

    def _parse_condition(self, condition):
        parser = ExpressionParser(condition)
        return parser.get_ast()

    def _parse_transition(self, instructions, parent_state=None):
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
            events = []
            actions = []
            condition = None
            if comment is not None:
                parser = TransitionParser(comment)
                raw_events, raw_condition, raw_actions = parser.get_transition_items()
                events = self._parse_events(raw_events)
                actions = self._parse_actions(raw_actions)
                condition = self._parse_condition(raw_condition)
            if from_state_name != '[*]':
                from_state = State.create_state(from_state_name, parent_state)
                for state in states:
                    if from_state == state:
                        state.sub_states.update(from_state.sub_states)
                        state.transitions.update(from_state.transitions)
                        break
                else:
                    states.add(from_state)
            else:
                from_state = parent_state
            if to_state_name != '[*]':
                to_state = State.create_state(to_state_name, parent_state)
                for state in states:
                    if to_state == state:
                        state.sub_states.update(to_state.sub_states)
                        state.transitions.update(to_state.transitions)
                        break
                else:
                    states.add(to_state)
            else:
                to_state = parent_state
            transitions.add(Transition(from_state, to_state, events, actions, condition))
        return states, transitions

    def _parse_instructions(self, instructions, parent_state=None):
        """
        Parsing the platuml
        :param instructions:
        :param parent_state:
        :return:
        """
        states = set()
        transitions = set()
        simple_instructions = re.sub(_nested_state_regex, '', copy.copy(instructions))
        new_states, new_transitions = self._parse_transition(simple_instructions, parent_state)
        states.update(new_states)
        transitions.update(new_transitions)
        nested_state_meta = _nested_state.finditer(instructions)
        for nested_state in nested_state_meta:
            state_name = nested_state.group('name')
            state_comment = nested_state.group('comment')
            new_state = State.create_state(state_name, parent_state, state_comment)
            body = nested_state.group('body')
            new_states, new_transitions = self._parse_instructions(body, new_state)
            for state in states:
                if new_state == state:
                    state.sub_states.update(new_state.sub_states)
                    state.transitions.update(new_state.transitions)
                    break
            else:
                states.add(new_state)
            transitions.update(new_transitions)
        return states, transitions

    def _tie_transitions_to_states(self, transitions, root):
        for transition in transitions:
            transition_owner = _find_least_common_acesentor(root, [transition.from_state, transition.to_state])
            if transition_owner is not None:
                transition_owner.transitions.add(transition)

    def parse_uml_file(self, file_name):
        """
        Function for parsing PlantUML State Machine
        :param file_name: Name of file with State Machine
        :return: states, transitions: State and Transitions of State Machine
        """
        with open(file_name, 'r') as file:
            import os
            instructions = file.read()
            state_machine_name = os.path.basename(file_name)
            state_machine_name = state_machine_name.split('.')[0]
            root = State.create_state(state_machine_name)
            states, transitions = self._parse_instructions(instructions, root)
            self._tie_transitions_to_states(transitions, root)
            return states, transitions
