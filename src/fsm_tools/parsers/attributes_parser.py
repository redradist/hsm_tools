import json
import os
import re

from fsm_tools.fsm_types import Symbol


class AttributeParser:
    __JSON_ATTRIBUTES_KEY = 'attributes'

    __VALID_TYPES = ['bool', 'Bool',
                     'boolean', 'Boolean',
                     'int', 'Int',
                     'integer', 'Integer',
                     'float', 'Float',
                     'double', 'Double',
                     'dec', 'Dec',
                     'decimal', 'Decimal',
                     'num', 'Num',
                     'number', 'Number',
                     'str', 'Str',
                     'string', 'String']

    def __init__(self, file=None, json_text=None):
        """
        Constructor of the object. It parses all
        :param file: Should be eight file name or file object
        """
        self._attributes = []
        if file is not None:
            if type(file) == str:
                if os.path.exists(file):
                    match_state_attributes_json = re.match(r'.+.attributes.(json|yaml)$', file)
                    objects = AttributeParser._parse_json(file)
                    if match_state_attributes_json:
                        self._attributes = self._parse_attributes(objects, path=os.path.dirname(file))
                    elif AttributeParser.__JSON_ATTRIBUTES_KEY in objects:
                        self._attributes = self._parse_attributes(objects[AttributeParser.__JSON_ATTRIBUTES_KEY],
                                                                  path=os.path.dirname(file))
                else:
                    text = file
                    objects = json.loads(text)
                    self._attributes = self._parse_attributes(objects)
            elif 'read' in file:
                text = file.read()
                objects = json.loads(text)
                self._attributes = self._parse_attributes(objects)
            else:
                raise ValueError(f'file{file} should be eight file name or file object !!')

        if json_text is not None:
            self._attributes = json.loads(json_text)

    @property
    def attributes(self):
        return self._attributes

    def _parse_attributes(self, objects, owner=None, path=None):
        attributes = []
        for name, value in objects.items():
            if type(value) == str:
                attr = Symbol(name, object=owner)
                if self.is_nested_type(value):
                    if not path:
                        raise ValueError('Unknown current path !!')
                    full_file_path = os.path.abspath(path) + '/' + value
                    objects = AttributeParser._parse_json(full_file_path)
                    attr.symbols = self._parse_attributes(objects, owner=attr, path=path)
                elif self.is_valid_type(value):
                    attr.attr_type = self.convert_unified(value)
                else:
                    raise ValueError('Invalid type. Type should be one of these: ' + str(AttributeParser.__VALID_TYPES))
                attributes.append(attr)
            elif type(value) == dict:
                attr = Symbol(name, object=owner)
                attr.symbols.extend(self._parse_attributes(value, owner=attr, path=path))
                attributes.append(attr)
        return attributes

    def find_all_attributes_for(self, path, state_name):
        inner_attributes = []
        external_attributes = []
        for f in os.listdir(path):
            full_file_path = os.path.abspath(path) + '/' + f
            match_state_json = re.match(r'^' + state_name + r'.(json|yaml)$', f)
            match_state_attributes_json = re.match(r'^' + state_name + r'.attributes.(json|yaml)$', f)
            if match_state_json:
                objects = AttributeParser._parse_json(full_file_path)
                if AttributeParser.__JSON_ATTRIBUTES_KEY in objects:
                    inner_attributes.extend(self._parse_attributes(objects[AttributeParser.__JSON_ATTRIBUTES_KEY], path=path))
            elif match_state_attributes_json:
                objects = AttributeParser._parse_json(full_file_path)
                attributes = self._parse_attributes(objects, path=path)
                external_attributes.extend(attributes)
        return external_attributes if external_attributes else inner_attributes

    @staticmethod
    def _parse_json(full_file_path):
        with open(full_file_path, 'r') as f:
            text = f.read()
            objects = json.loads(text)
        return objects

    @staticmethod
    def is_nested_type(type):
        return re.match(r'.+.(json|yaml)$', type)

    @staticmethod
    def is_valid_type(type):
        return type in AttributeParser.__VALID_TYPES

    @staticmethod
    def convert_unified(type):
        if AttributeParser.is_valid_type(type):
            if type in ['bool', 'Bool', 'boolean', 'Boolean']:
                return 'Boolean'
            elif type in ['int', 'Int', 'integer', 'Integer']:
                return 'Integer'
            elif type in ['float', 'Float']:
                return 'Float'
            elif type in ['double', 'Double']:
                return 'Double'
            elif type in ['dec', 'Dec', 'decimal', 'Decimal']:
                return 'Decimal'
            elif type in ['num', 'Num', 'number', 'Number']:
                return 'Number'
            elif type in ['str', 'Str', 'string', 'String']:
                return 'String'
            else:
                return type

    @staticmethod
    def find_all_attribute_files(path):
        all_state_attribute_files = []
        for f in os.listdir(path):
            full_file_path = os.path.abspath(path) + '/' + f
            match0 = re.match(r'^(?P<state_name>\w+).attributes.(json|yaml)$', f)
            match1 = re.match(r'^(?P<state_name>\w+).(json|yaml)$', f)
            if match0:
                state_name = match0.group("state_name")
                all_state_attribute_files.append((state_name, full_file_path))
            elif match1:
                objects = AttributeParser._parse_json(full_file_path)
                if AttributeParser.__JSON_ATTRIBUTES_KEY in objects:
                    state_name = match1.group("state_name")
                    all_state_attribute_files.append((state_name, full_file_path))
        return all_state_attribute_files


