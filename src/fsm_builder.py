import json
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

    def build_from(self, uml_diagram):
        uml_parser = PlantUMLParser()
        sub_states, transitions = uml_parser.parse_uml_file(uml_diagram)
        fsm_name = os.path.splitext(os.path.basename(uml_diagram))[0]
        fsm = State(fsm_name)

        FSMBuilder._index_each_states(sub_states, 0)
        FSMBuilder._index_each_transitions(transitions, 0)
        attribute_files, state_attribute_files, state_config_files = AttributeParser.find_all_attribute_files(
            os.path.dirname(uml_diagram))
        external_attributes = {attrib_name for attrib_name, _ in attribute_files}
        attribute_parser = AttributeParser(external_attributes)
        action_parser = ActionParser()
        attributes = attribute_parser.find_all_attribute_for(os.path.dirname(uml_diagram),
                                                             fsm_name)
        for state in sub_states:
            state.attributes = attribute_parser.find_all_attribute_for(os.path.dirname(uml_diagram),
                                                                       state.name)
            state.actions = action_parser.find_all_action_for(os.path.dirname(uml_diagram),
                                                                       state.name)
        fsm.sub_states = sub_states
        fsm.attributes = attributes
        fsm.transitions = transitions
        return fsm
