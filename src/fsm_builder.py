import os

from src.fsm_types import State
from src.parsers.actions_parser import ActionParser
from src.parsers.attributes_parser import AttributeParser
from src.parsers.plantuml_parser import PlantUMLParser


class FSMBuilder:
    @staticmethod
    def _index_each_states(states, index):
        for state in states:
            state.index = index
            index += 1
            if state.sub_states:
                FSMBuilder._index_each_states(state.sub_states, 0)

    @staticmethod
    def _index_each_transitions(transitions, index):
        for transition in transitions:
            transition.index = index
            index += 1

    @staticmethod
    def _find_action_name(action_name, state=None):
        if state:
            for action in state.actions:
                if action_name == action.name:
                    return action
            return FSMBuilder._find_action_name(action_name, state.parent_state)

    @staticmethod
    def _tie_tran_action(transition):
        for call_action in transition.call_actions:
            action_name = call_action.name
            if action_name:
                found_action = FSMBuilder._find_action_name(action_name, transition.from_state)
                if found_action is not None:
                    call_action.action = found_action
                    continue

                found_action = FSMBuilder._find_action_name(action_name, transition.to_state)
                if found_action is not None:
                    call_action.action = found_action
                    continue

                raise ValueError(f'Action for transition[{transition}] is not found !!')

    def build_from(self, uml_diagram, lang):
        uml_parser = PlantUMLParser()
        sub_states, transitions = uml_parser.parse_uml_file(uml_diagram)
        fsm_name = os.path.splitext(os.path.basename(uml_diagram))[0]
        fsm = State.create_state(fsm_name)

        FSMBuilder._index_each_states(sub_states, 0)
        FSMBuilder._index_each_transitions(transitions, 0)
        attribute_files = AttributeParser.find_all_attribute_files(
            os.path.dirname(uml_diagram))
        external_attributes = {attrib_name for attrib_name, _ in attribute_files}
        attribute_parser = AttributeParser()
        action_parser = ActionParser()
        fsm.attributes = attribute_parser.find_all_attributes_for(os.path.dirname(uml_diagram),
                                                                  fsm_name)
        for state in sub_states:
            state.attributes = attribute_parser.find_all_attributes_for(os.path.dirname(uml_diagram),
                                                                        state.name)
            state.actions = action_parser.find_all_action_for(os.path.dirname(uml_diagram),
                                                              state.name)
        fsm.sub_states = sub_states
        for tran in transitions:
            FSMBuilder._tie_tran_action(tran)
        return fsm
