import copy
import io
import json
import os
import re

from src.fsm_types import Symbol

__attributes_json = '''
{
    "name": {
      "name": "String",
      "id0": "Number",
      "id1": "Integer",
      "id3": "Float",
      "id4": "Boolean"
    },
    "id4": "Boolean"
}
'''


__attributes_yaml = '''
# An employee record
name: String
  name: String
  id0: Number

name: String
id0: Number
id1: Integer
id2: Real

'''

class AttributeParser:

    __valid_types = ['bool', 'Bool',
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

    def __init__(self, extern_attribs=set()):
        self.extern_attribs = copy.deepcopy(extern_attribs)

    def is_nested_type(self, type):
        return re.match(r'.+.(json|yaml)$', type)

    def is_valid_type(self, type):
        return type in AttributeParser.__valid_types or \
               type in self.extern_attribs

    def _convert_unified(self, type):
        if self.is_valid_type(type):
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

    def _parse_objects(self, objs, owner=None, path=None):
        attributes = []
        for key, value in objs.items():
            if type(value) == str:
                att = Symbol(key, object=owner)
                if self.is_nested_type(value):
                    if not path:
                        raise ValueError('Unknown current path !!')
                    full_file_path = os.path.abspath(path) + '/' + value
                    with open(full_file_path, 'r') as f:
                        text = f.read()
                        objects = json.loads(text)
                        nested_attributes = self._parse_objects(objects, path=path)
                        att.args = nested_attributes
                elif self.is_valid_type(value):
                    att.attr_type = self._convert_unified(value)
                else:
                    raise ValueError('Invalid type. Type should be one of these: ' + str(AttributeParser.__valid_types))
                attributes.append(att)
            elif type(value) == dict:
                atts = self._parse_objects(value, key, path=path)
                att = Symbol(key, object=owner)
                att.symbols.extend(atts)
                attributes.append(att)
        return attributes

    def parse_yaml(self, text):
        raise NotImplementedError('Currently this method is not implemented !!')

    @staticmethod
    def find_all_attribute_files(path):
        attrib_files = []
        state_attrib_files = []
        state_config_files = dict()
        for f in os.listdir(path):
            full_file_path = os.path.abspath(path) + '/' + f
            match0 = re.match(r'^(?P<state_name>\w+)_attributes.(json|yaml)$', f)
            match1 = re.match(r'^(?P<state_name>\w+).(json|yaml)$', f)
            if match0 or match1:
                state_name = match1.group("state_name")
                state_attrib_files.append((state_name, full_file_path))
        return attrib_files, state_attrib_files, state_config_files

    def parse_file(self, attribute_file):
        if type(attribute_file) == str:
            with open(attribute_file, 'r') as f:
                text = f.read()
                match = re.match(r'[/\w]+.(?P<file_extension>\w+)', attribute_file)
                file_extension = match.group('file_extension')
                if file_extension == 'json':
                    return self.parse_json(text)
                elif file_extension == 'yaml':
                    return self.parse_yaml(text)
                else:
                    assert "Unknown file extention !!"
        elif isinstance(attribute_file, io.IOBase):
            text = attribute_file.readlines()
            return self.parse_json(text)

    def parse_attributes(self, fl):
        if type(fl) == str:
            with open(fl, 'r') as f:
                text = f.read()
                return self.parse_json(text)
        elif isinstance(fl, io.IOBase):
            text = fl.readlines()
            return self.parse_json(text)

    def find_all_attribute_for(self, path, state_name, lang):
        attributes = []
        for f in os.listdir(path):
            full_file_path = os.path.abspath(path) + '/' + f
            match_state_json = re.match(r'^' + state_name + r'.(json|yaml)$', f)
            match_state_attributes_json = re.match(r'^' + state_name + r'.attributes.(json|yaml)$', f)
            if match_state_json:
                with open(full_file_path, 'r') as f:
                    text = f.read()
                    objects = json.loads(text)
                    if 'attributes' in objects:
                        attributes = self._parse_objects(objects['attributes'], path=path)
                        break
            elif match_state_attributes_json:
                with open(full_file_path, 'r') as f:
                    text = f.read()
                    objects = json.loads(text)
                    attributes.extend(self._parse_objects(objects, path=path))
        return attributes


if __name__ == '__main__':
    parser = AttributeParser()
    objs = parser.parse_json(__attributes_json)
    print('objs = ' + str(objs))
