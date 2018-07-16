import io
import json
import os
import re

from src.hsm_types import Attribute

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

    def is_valid_type(self, type):
        return type in AttributeParser.__valid_types

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

    def _parse_objects(self, objs, owner=None):
        attributes = []
        for key, value in objs.items():
            if type(value) == str:
                att = Attribute(key, object=owner)
                if not self.is_valid_type(value):
                    raise ValueError('Invalid type. Type should be one of these: ' + str(__valid_types))
                att.attr_type = self._convert_unified(value)
                attributes.append(att)
            elif type(value) == dict:
                atts = self._parse_objects(value, key)
                att = Attribute(key, object=owner)
                att.attr_type = None
                if hasattr(att, 'args'):
                    att.args = []
                att.args.extend(atts)
                attributes.append(att)
        return attributes

    def parse_json(self, text):
        attributes = []
        objs = json.loads(text)
        attributes.extend(self._parse_objects(objs))
        return attributes

    def parse_yaml(self, text):
        raise NotImplementedError('Currently this method is not implemented !!')

    @staticmethod
    def find_all_attribute_files(path):
        files = []
        for f in os.listdir(path):
            match = re.match(r'(?P<state_name>\w+)Attributes.(json|yaml)', f)
            if match:
                full_file_path = os.path.abspath(path) + '/' + f
                files.append((match.group("state_name"), full_file_path))
        return files

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


if __name__ == '__main__':
    parser = AttributeParser()
    objs = parser.parse_json(__attributes_json)
    print('objs = ' + str(objs))
