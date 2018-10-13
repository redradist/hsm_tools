import json
import os
import re

from src.fsm_types import Action, Function
from src.parsers.expression_parser import ExpressionParser


class ActionParser:
    scratch_file_pattern = re.compile(r'.+?(?P<action_name>[^/]+)\.scratch\.(?P<lang>.+)')
    import_module_pattern = re.compile(r'#include\s*.+')

    def is_nested_type(self, type):
        lst = ['cpp', 'java']
        lst = '|'.join(lst)
        return re.match(r'.+.scratch.(' + lst + r')$', type)

    def _parse_objects(self, objs, owner=None, path=None):
        actions = []
        for key, value in objs.items():
            if type(value) == str:
                func = Function(key, object=owner)
                if self.is_nested_type(value):
                    if not path:
                        raise ValueError('Unknown current path !!')
                    full_file_path = os.path.abspath(path) + '/' + value
                    with open(full_file_path, 'r') as f:
                        text = f.read()
                        objects = json.loads(text)
                        nested_attributes = self._parse_objects(objects, path=path)
                        func.args = nested_attributes
                else:
                    func.attr_type = self._convert_unified(value)
                actions.append(func)
            elif type(value) == dict:
                acts = self._parse_objects(value, key, path=path)
                func = Function(key, object=owner)
                func.attr_type = None
                if hasattr(func, 'args'):
                    func.args = []
                func.args.extend(acts)
                actions.append(func)
        return actions

    def is_scratch_action(self):
        pass

    def parse_internal(self, internal_actions, path):
        lang = None
        actions = []
        for action_name, action_body in internal_actions.items():
            options = []
            if type(action_body) == list:
                action_body = ''.join(action_body)
            elif re.match(ActionParser.scratch_file_pattern, action_body):
                match = re.match(ActionParser.scratch_file_pattern, action_body)
                lang = match.group('lang')
                with open(os.path.join(path, action_body)) as f:
                    lines = f.readlines()
                    action_body = []
                    for line in lines:
                        match = re.match(ActionParser.import_module_pattern, line)
                        if match:
                            options.append(match.group(0).strip())
                        else:
                            action_body.append(line)
                    action_body = ''.join(action_body)
                    action_body = action_body.strip()
            expression_parser = ExpressionParser(action_body)
            function = expression_parser.parse()
            function.name = action_name
            if type(function) != Function:
                raise ValueError(f'Type of function[{function}] should be Function !!')
            if lang:
                function.lang = lang
            if options:
                function.options = options
            actions.append(function)
        return actions

    def parse_external(self, external_actions, path):
        actions = []
        for external in external_actions:
            import_statement = external['import']
            using_as = external['using']
            ex_actions = external['actions']
            for ac in ex_actions:
                function = Function(name=ac)
                function.full_name = using_as + ac
                actions.append(function)
        return actions

    def find_all_action_for(self, path, state_name):
        actions = []
        for f in os.listdir(path):
            full_file_path = os.path.abspath(path) + '/' + f
            match_state_json = re.match(r'^' + state_name + r'.(json|yaml)$', f)
            match_state_actions_json = re.match(r'^' + state_name + r'.actions.(json|yaml)$', f)
            if match_state_json:
                with open(full_file_path, 'r') as f:
                    text = f.read()
                    objects = json.loads(text)
                    if 'actions' in objects:
                        temp_actions = objects['actions']
                        internal_actions = temp_actions['internal']
                        external_actions = temp_actions['external']
                        actions = []
                        actions.extend(self.parse_internal(internal_actions, path))
                        actions.extend(self.parse_external(external_actions, path))
                        break
            elif match_state_actions_json:
                with open(full_file_path, 'r') as f:
                    text = f.read()
                    temp_actions = json.loads(text)
                    internal_actions = temp_actions['internal']
                    external_actions = temp_actions['external']
                    actions.extend(self.parse_internal(internal_actions, path))
                    actions.extend(self.parse_external(external_actions, path))
        return actions
