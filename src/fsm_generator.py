#!/usr/bin/python3

import argparse
import datetime
import re
import traceback

from jinja2 import Template, Environment

from src.parsers.attributes_parser import AttributeParser
from src.parsers.plantuml_parser import PlantUMLParser

jinja2_do_ext = Environment(extensions=['jinja2.ext.do'])


def generate_state_attributes_wrapper(fsm_name, state, template_file, dir_to_save):
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime("%d %b %Y")

    with open(template_file, 'r') as file:
        lines = file.readlines()
        lines = "".join(lines)
        template = jinja2_do_ext.from_string(lines)
        if not os.path.exists(dir_to_save):
            os.mkdir(dir_to_save)
        files_output = template.render(fsm_name=fsm_name,
                                       state_name=state.name,
                                       attributes=state.attributes,
                                       date=current_date)
        file_name_to_save = dir_to_save + state.name + "_Attributes.hpp"
        with open(file_name_to_save, mode='w') as file_to_save:
            file_to_save.write(files_output)


def generate_attributes_wrapper(fsm_name, struct_name, attributes, attribute_template, dir_to_save):
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime("%d %b %Y")

    with open(attribute_template, 'r') as file:
        lines = file.readlines()
        lines = "".join(lines)
        template = jinja2_do_ext.from_string(lines)
        if not os.path.exists(dir_to_save):
            os.mkdir(dir_to_save)
        files_output = template.render(fsm_name=fsm_name,
                                       struct_name=struct_name,
                                       attributes=attributes,
                                       date=current_date)
        file_name_to_save = dir_to_save + struct_name + "Attributes.hpp"
        with open(file_name_to_save, mode='w') as file_to_save:
            file_to_save.write(files_output)


def generate_actions_wrapper(fsm_name, actions, action_templates,  dir_to_save):
    pass


def generate_state_wrapper(fsm_name, state, extern_attribs, state_templates, attribute_template, action_templates, dir_to_save):
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime("%d %b %Y")

    index = 0
    for template_file_name in state_templates:
        if template_file_name:
            with open(template_file_name, 'r') as file:
                lines = file.readlines()
                lines = "".join(lines)
                template = jinja2_do_ext.from_string(lines)
                wrapper_name = state.name
                __file_extension_regex = r"\w+\.(?P<file_extension>\w+)\.\w+"
                __file_extension = re.compile(__file_extension_regex)
                file_extension = __file_extension.search(template_file_name).group(1)
                if not os.path.exists(dir_to_save):
                    os.mkdir(dir_to_save)
                files_output = template.render(fsm_name=fsm_name,
                                               state=state,
                                               date=current_date)
                with open(dir_to_save + wrapper_name + "_State." + file_extension, mode='w') as file_to_save:
                    file_to_save.write(files_output)
                if state.attributes:
                    generate_state_attributes_wrapper(fsm_name, state, attribute_template, dir_to_save)
        index += 1
    for sub_state in state.sub_states:
        generate_state_wrapper(fsm_name, sub_state, extern_attribs, state_templates, attribute_template, action_templates, dir_to_save)


def _index_each_states(states, index):
    for state in states:
        state.index = index
        index += 1
        if state.sub_states:
            _index_each_states(state.sub_states, 0)


def _index_each_transitions(transitions, index):
    for transition in transitions:
        transition.index = index
        index += 1


def generate_fsm_wrappers(uml_diagram, dir_to_save, state_templates=[], attribute_templates=[], action_templates=[]):
    if len(state_templates) != 2:
        raise ValueError("Size of state_templates argument should be 2 : CommonAPI Client and CommonAPI Service")

    if len(attribute_templates) != 2:
        raise ValueError("Size of attribute_templates argument should be 2 !!")

    if len(action_templates) != 4:
        raise ValueError("Size of action_templates argument should be 4 !!")

    if len(dir_to_save) == 0:
        raise ValueError("dir_to_save is empty !!")
    elif dir_to_save[len(dir_to_save) - 1] != '/':
        dir_to_save += '/'

    uml_parser = PlantUMLParser()
    states, transitions = uml_parser.parse_uml_file(uml_diagram)
    fsm_name = os.path.splitext(os.path.basename(uml_diagram))[0]

    if len(states) == 0:
        raise ValueError("Size of states is zero. No work to do man !?")

    if len(transitions) == 0:
        raise ValueError("Size of transitions is zero. No work to do man !?")

    _index_each_states(states, 0)
    _index_each_transitions(transitions, 0)
    attribute_files, state_attribute_files = AttributeParser.find_all_attribute_files(os.path.dirname(uml_diagram))
    external_attributes = { attrib_name for attrib_name, _ in attribute_files }
    attribute_parser = AttributeParser(external_attributes)
    for state in states:
        for state_name, attribute_file_name in state_attribute_files:
            if state.name == state_name:
                state.attributes = attribute_parser.parse_file(attribute_file_name)

    for state in states:
        generate_state_wrapper(fsm_name, state, external_attributes, state_templates, attribute_templates[1], action_templates[2:], dir_to_save)

    for attribute in attribute_files:
        attribute_parser = AttributeParser(external_attributes)
        attributes = attribute_parser.parse_file(attribute[1])
        generate_attributes_wrapper(fsm_name, attribute[0], attributes, attribute_templates[0], dir_to_save)

    actions = []
    for attribute in attribute_files:
        attribute_parser = AttributeParser(external_attributes)
        attributes = attribute_parser.parse_file(attribute[1])
        generate_actions_wrapper(fsm_name, actions, action_templates[:2], dir_to_save)


if __name__ == '__main__':
    import os
    os.chdir(os.path.dirname(__file__))
    current_dir = os.getcwd()

    parser = argparse.ArgumentParser()
    parser.add_argument("uml_diagram",
                        help="State Machine UML diagram /<path>/<name>.uml")
    parser.add_argument("dir_to_save",
                        help="State Machine /<path_to_generate>/")
    parser.add_argument("--default",
                        action='store_true',
                        help="Choose default templates")
    parser.add_argument("--state_templates",
                        help="Templates for generating State Machine")
    parser.add_argument("--attribute_templates",
                        help="Templates for generating Attribute file")
    parser.add_argument("--action_templates",
                        help="Templates for generating Action file")
    args = parser.parse_args()
    if args.default:
        if not args.state_templates:
            args.state_templates = []
            args.state_templates.append(os.path.join(current_dir, "../templates/default/StateDefault.hpp.jinja2"))
            args.state_templates.append(os.path.join(current_dir, "../templates/default/StateDefault.cpp.jinja2"))
        if not args.attribute_templates:
            args.attribute_templates = []
            args.attribute_templates.append(os.path.join(current_dir, "../templates/default/AttributesDefault.hpp.jinja2"))
            args.attribute_templates.append(os.path.join(current_dir, "../templates/default/StateAttributesDefault.hpp.jinja2"))
        if not args.action_templates:
            args.action_templates = []
            args.action_templates.append(os.path.join(current_dir, "../templates/default/ActionsDefault.hpp.jinja2"))
            args.action_templates.append(os.path.join(current_dir, "../templates/default/ActionsDefault.cpp.jinja2"))
            args.action_templates.append(os.path.join(current_dir, "../templates/default/StateActionsDefault.hpp.jinja2"))
            args.action_templates.append(os.path.join(current_dir, "../templates/default/StateActionsDefault.cpp.jinja2"))
    try:
        generate_fsm_wrappers(args.uml_diagram,
                              args.dir_to_save,
                              args.state_templates,
                              args.attribute_templates,
                              args.action_templates)
    except Exception as ex:
        print("ex is " + str(ex))
        traceback.print_exc()
