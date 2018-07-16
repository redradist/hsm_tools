#!/usr/bin/python3

import argparse
import datetime
import itertools
import re
import traceback

from sys import exc_info
from jinja2 import Template

from src.plantuml_parser import PlantUMLParser


def generate_wrapper(state, templates, dir_to_save):
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime("%d %b %Y")

    index = 0
    for template_file_name in templates:
        if template_file_name:
            with open(template_file_name, 'r') as file:
                lines = file.readlines()
                lines = "".join(lines)

                template = Template(lines)
                files_output = template.render(state=state,
                                               date=current_date)
                wrapper_name = state.name
                __file_extension_regex = r"\w+\.(?P<file_extension>\w+)\.\w+"
                __file_extension = re.compile(__file_extension_regex)
                file_extension = __file_extension.search(template_file_name).group(1)
                if not os.path.exists(dir_to_save):
                    os.mkdir(dir_to_save)
                if index < 2:
                    with open(dir_to_save + wrapper_name + "State." + file_extension, mode='w') as file_to_save:
                        file_to_save.write(files_output)
                else:
                    with open(dir_to_save + wrapper_name + "StateAttributes." + file_extension, mode='w') as file_to_save:
                        file_to_save.write(files_output)
        index += 1
    for sub_state in state.sub_states:
        generate_wrapper(sub_state, templates, dir_to_save)


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


def generate_fsm_wrappers(uml_diagram, dir_to_save, templates=[]):
    if len(templates) != 3:
        raise ValueError("Size of templates argument should be 3 : CommonAPI Client and CommonAPI Service")

    if len(dir_to_save) == 0:
        raise ValueError("dir_to_save is empty !!")
    elif dir_to_save[len(dir_to_save) - 1] != '/':
        dir_to_save += '/'

    parser = PlantUMLParser()
    states, transitions = parser.parse_uml_file(uml_diagram)
    _index_each_states(states, 0)
    _index_each_transitions(transitions, 0)
    if len(states) == 0:
        raise ValueError("Size of states is zero. No work to do man !?")

    if len(transitions) == 0:
        raise ValueError("Size of transitions is zero. No work to do man !?")

    for state in states:
        generate_wrapper(state, templates, dir_to_save)


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
    parser.add_argument("--templates",
                        help="Template for generating State Machine")
    args = parser.parse_args()
    if args.default:
        if not args.templates:
            args.templates = []
            args.templates.append(os.path.join(current_dir, "../templates/default/StateDefault.hpp.jinja2"))
            args.templates.append(os.path.join(current_dir, "../templates/default/StateDefault.cpp.jinja2"))
            args.templates.append(os.path.join(current_dir, "../templates/default/StateAttributesDefault.hpp.jinja2"))
    try:
        generate_fsm_wrappers(args.uml_diagram, args.dir_to_save, args.templates)
    except Exception as ex:
        print("ex is " + str(ex))
        traceback.print_exc()
