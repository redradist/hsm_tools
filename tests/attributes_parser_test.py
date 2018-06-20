import unittest

from hsm_types import Value, Function, Attribute
from parsers.attributes_parser import parse_str


class TestingAttributesParser(unittest.TestCase):
    def setUp(self):
        """Currently nothing to do. Use it for initialization data before test"""
        pass

    def tearDown(self):
        """Currently nothing to do. Use it for reinitialization data after test"""
        pass

    def test__OneAttributes0__Valid(self):
        example_json = '''
        {
            "name": {
              "name": "String",
              "id0": "Number",
              "id1": "Integer",
              "id3": "Float",
              "id4": "Boolean"
            }
        }
        '''
        attributes = parse_str(example_json)
        self.assertEqual(len(attributes), 1)

    def test__OneAttributes1__Valid(self):
        example_json = '''
        {
            "id0": "Number"
        }
        '''
        attributes = parse_str(example_json)
        self.assertEqual(len(attributes), 1)

    def test__TwoAttributes__Valid(self):
        example_json = '''
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
        attributes = parse_str(example_json)
        self.assertEqual(len(attributes), 2)

    def test__ThreeAttributes__Valid(self):
        example_json = '''
        {
            "name": {
              "name": "String",
              "id0": "Number",
              "id1": "Integer",
              "id3": "Float",
              "id4": "Boolean"
            },
            "id4": "Boolean",
            "id5": "Integer"
        }
        '''
        attributes = parse_str(example_json)
        self.assertEqual(len(attributes), 3)
