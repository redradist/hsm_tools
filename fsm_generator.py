import argparse
import datetime
import itertools
import re

from jinja2 import Template
from plantuml_parser import PlantUMLParser


def generate_fsm_wrappers(uml_diagram, dir_to_save, templates=[]):
    if len(templates) != 2:
        raise ValueError("Size of templates argument should be 2 : CommonAPI Client and CommonAPI Service")

    if len(dir_to_save) == 0:
        raise ValueError("dir_to_save is empty !!")
    elif dir_to_save[len(dir_to_save) - 1] != '/':
        dir_to_save += '/'

    parser = PlantUMLParser()
    states, transitions = parser.parse_uml_file(uml_diagram)
    if len(states) == 0:
        raise ValueError("Size of states is zero. No work to do man !?")

    if len(transitions) == 0:
        raise ValueError("Size of transitions is zero. No work to do man !?")

    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime("%d %b %Y")

    for template_file_name in templates:
        if template_file_name:
            with open(template_file_name, 'r') as file:
                lines = file.readlines()
                lines = "".join(lines)
                for state, transition in itertools.zip_longest(states, transitions):
                    template = Template(lines)
                    files_output = template.render(state=state,
                                                   date=current_date)
                    wrapper_name = state.name
                    __comment_regex = r"\w+\.(?P<file_extension>\w+)\.\w+"
                    __comment = re.compile(__comment_regex)
                    file_extension = __comment.search(template_file_name).group(1)
                    with open(dir_to_save + wrapper_name + "State." + file_extension, mode='w') as file_to_save:
                        file_to_save.write(files_output)


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
            args.templates.append(os.path.join(current_dir, "default_templates/StatesDefault.hpp.jinja2"))
            args.templates.append(os.path.join(current_dir, "default_templates/StatesDefault.cpp.jinja2"))
    try:
        generate_fsm_wrappers(args.uml_diagram, args.dir_to_save, args.templates)
    except Exception as ex:
        print("ex is " + str(ex))
