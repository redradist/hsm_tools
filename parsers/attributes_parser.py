import io
import json
import tempfile
from struct import Struct
from typing import Tuple, Any

from hsm_types import Attribute

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

class String:

    def __init__(self):
        pass

    def convert_to_str(self, context, lang):
        """

        :param context:
        :param lang: Programming language (C++)
        :return: str object with code that represent string
        """
        pass


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




def is_valid_type(type):
    return type in __valid_types


def _convert_unified(type):
    if is_valid_type(type):
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


def translate_to_common_abriviation():

    pass


def _parse_objects(objs, owner=None):
    attributes = set()
    for key, value in objs.items():
        if type(value) == str:
            att = Attribute(key, object=owner)
            if not is_valid_type(value):
                raise ValueError('Invalid type. Type should be one of these: ' + str(__valid_types))
            att.attr_type = _convert_unified(value)
            attributes.add(att)
        elif type(value) == dict:
            atts = _parse_objects(value, key)
            att = Attribute(key, object=owner)
            att.attr_type = None
            if hasattr(att, 'args'):
                att.args = []
            att.args.extend(atts)
            attributes.add(att)
    return attributes


def parse_str(text):
    attributes = set()
    objs = json.loads(text)
    attributes.update(_parse_objects(objs))
    return attributes


def parse_file(fl):
    if type(fl) == str:
        with open(fl, 'r') as f:
            text = f.read()
            return parse_str(text)
    elif isinstance(fl, io.IOBase):
        text = fl.readlines()
        return parse_str(text)


def parse_attributes(fl):
    if type(fl) == str:
        with open(fl, 'r') as f:
            text = f.read()
            return parse_str(text)
    elif isinstance(fl, io.IOBase):
        text = fl.readlines()
        return parse_str(text)


if __name__ == '__main__':
    objs = parse_str(__attributes_json)
    print('objs = ' + str(objs))
