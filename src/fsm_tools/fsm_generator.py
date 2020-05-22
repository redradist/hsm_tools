#!/usr/bin/python3

import argparse
import datetime
import re
import traceback

from jinja2 import Environment
from fsm_tools.fsm_builder import FSMBuilder
from fsm_tools.fsm_types import State

jinja2_do_ext = Environment(extensions=['jinja2.ext.do'])


class Templates:
    def __init__(self, state_templates, attribute_templates, action_templates):
        self.validate_templates(action_templates, attribute_templates, state_templates)

        self.state_templates = dict()
        self.state_templates['header_file'] = state_templates[0]
        self.state_templates['source_file'] = state_templates[1]
        self.attribute_templates = dict()
        self.attribute_templates['attributes_file'] = attribute_templates[0]
        self.attribute_templates['state_attributes_file'] = attribute_templates[1]
        self.action_templates = dict()
        self.action_templates['header_file'] = action_templates[0]
        self.action_templates['source_file'] = action_templates[1]

    @staticmethod
    def validate_templates(action_templates, attribute_templates, state_templates):
        if len(state_templates) != 2:
            raise ValueError("Size of state_templates argument should be 2 : CommonAPI Client and CommonAPI Service")
        if len(attribute_templates) != 2:
            raise ValueError("Size of attribute_templates argument should be 2 !!")
        if len(action_templates) != 4:
            raise ValueError("Size of action_templates argument should be 4 !!")


def generate_state_attributes_wrapper(state, dir_to_save, template_file):
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime("%d %b %Y")

    with open(template_file, 'r') as file:
        template = _prepare_template(file)
        if not os.path.exists(dir_to_save):
            os.mkdir(dir_to_save)
        files_output = template.render(state_name=state.name,
                                       attributes=state.attributes,
                                       date=current_date)
        file_name_to_save = dir_to_save + state.name + "_Attributes.hpp"
        with open(file_name_to_save, mode='w') as file_to_save:
            file_to_save.write(files_output)


def _prepare_template(file):
    lines = file.readlines()
    lines = "".join(lines)
    template = jinja2_do_ext.from_string(lines)
    return template


def generate_attributes_wrapper(struct_name, attributes, attribute_template, dir_to_save):
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime("%d %b %Y")

    with open(attribute_template, 'r') as file:
        template = _prepare_template(file)
        if not os.path.exists(dir_to_save):
            os.mkdir(dir_to_save)
        files_output = template.render(struct_name=struct_name,
                                       attributes=attributes,
                                       date=current_date)
        file_name_to_save = dir_to_save + struct_name + "Attributes.hpp"
        with open(file_name_to_save, mode='w') as file_to_save:
            file_to_save.write(files_output)


def generate_actions_wrapper(fsm_name, actions, action_templates,  dir_to_save):
    pass


def generate_state_wrapper(state, dir_to_save, templates):
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime("%d %b %Y")

    index = 0
    for _, template_file_name in templates.state_templates.items():
        if template_file_name:
            with open(template_file_name, 'r') as file:
                template = _prepare_template(file)
                wrapper_name = state.name
                __file_extension_regex = r"\w+\.(?P<file_extension>\w+)\.\w+"
                __file_extension = re.compile(__file_extension_regex)
                file_extension = __file_extension.search(template_file_name).group(1)
                if not os.path.exists(dir_to_save):
                    os.mkdir(dir_to_save)
                files_output = template.render(state=state,
                                               date=current_date)
                with open(dir_to_save + wrapper_name + "_State." + file_extension, mode='w') as file_to_save:
                    file_to_save.write(files_output)
                if state.attributes:
                    generate_state_attributes_wrapper(state, dir_to_save, templates.attribute_templates['state_attributes_file'])
        index += 1
    # generate_attributes_wrapper(state.name, attribute[0], attributes, attribute_templates[0], dir_to_save)
    for sub_state in state.sub_states:
        generate_state_wrapper(sub_state, dir_to_save, templates)


def generate_fsm(fsm: State, dir_to_save, templates):
    generate_state_wrapper(fsm, dir_to_save, templates)

    # for attribute in attribute_files:
    #     attribute_parser = AttributeParser(external_attributes)
    #     attributes = attribute_parser.parse_file(attribute[1])
    #     generate_attributes_wrapper(fsm_name, attribute[0], attributes, attribute_templates[0], dir_to_save)
    #
    # actions = []
    # for attribute in attribute_files:
    #     attribute_parser = AttributeParser(external_attributes)
    #     attributes = attribute_parser.parse_file(attribute[1])
    #     generate_actions_wrapper(fsm_name, actions, action_templates[:2], dir_to_save)
    #


def generate_fsm_wrappers(uml_diagram, dir_to_save, templates):
    if len(dir_to_save) == 0:
        raise ValueError("dir_to_save is empty !!")

    if dir_to_save[len(dir_to_save) - 1] != '/':
        dir_to_save += '/'

    builder = FSMBuilder()
    fsm = builder.build_from(uml_diagram)
    generate_fsm(fsm, dir_to_save, templates)


def get_command_line_args():
    """
    Gets command line arguments that was passed to script
    :return: Command line arguments
    """
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
    return parser.parse_args()


def analyze_arguments(args):
    if args.default:
        if not args.state_templates:
            args.state_templates = []
            args.state_templates.append(os.path.join(current_dir, "../../templates/default/StateDefault.hpp.jinja2"))
            args.state_templates.append(os.path.join(current_dir, "../../templates/default/StateDefault.cpp.jinja2"))
        if not args.attribute_templates:
            args.attribute_templates = []
            args.attribute_templates.append(
                os.path.join(current_dir, "../../templates/default/AttributesDefault.hpp.jinja2"))
            args.attribute_templates.append(
                os.path.join(current_dir, "../../templates/default/StateAttributesDefault.hpp.jinja2"))
        if not args.action_templates:
            args.action_templates = []
            args.action_templates.append(os.path.join(current_dir, "../../templates/default/ActionsDefault.hpp.jinja2"))
            args.action_templates.append(os.path.join(current_dir, "../../templates/default/ActionsDefault.cpp.jinja2"))
            args.action_templates.append(
                os.path.join(current_dir, "../../templates/default/StateActionsDefault.hpp.jinja2"))
            args.action_templates.append(
                os.path.join(current_dir, "../../templates/default/StateActionsDefault.cpp.jinja2"))


if __name__ == '__main__':
    import os
    os.chdir(os.path.dirname(__file__))
    current_dir = os.getcwd()

    args = get_command_line_args()
    analyze_arguments(args)
    try:
        templates = Templates(args.state_templates, args.attribute_templates, args.action_templates)
        generate_fsm_wrappers(args.uml_diagram,
                              args.dir_to_save,
                              templates)
    except Exception as ex:
        print("ex is {}".format(str(ex)))
        traceback.print_exc()
