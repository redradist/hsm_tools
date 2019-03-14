import os
import unittest

from fsm_tools.fsm_types import Symbol
from fsm_tools.parsers.attributes_parser import AttributeParser


class TestingAttributesParser(unittest.TestCase):
    def setUp(self):
        """Currently nothing to do. Use it for initialization data before test"""
        pass

    def tearDown(self):
        """Currently nothing to do. Use it for reinitialization data after test"""
        pass

    def test__FindAllAttributesFiles__Valid(self):
        attribute_files = AttributeParser.find_all_attribute_files('../simple_fsm')
        self.assertEqual(len(attribute_files), 3)
        set_of_file_names = set(os.path.basename(entry[1]) for entry in attribute_files)
        self.assertTrue('FSM.json' in set_of_file_names)
        self.assertTrue('SimpleFSM.json' in set_of_file_names)
        self.assertTrue('SimpleFSM.attributes.json' in set_of_file_names)

    def test__ParseAllAttributesFiles__Valid(self):
        attribute_files = AttributeParser.find_all_attribute_files('../simple_fsm')
        self.assertEqual(len(attribute_files), 3)
        set_of_file_names = set(os.path.basename(entry[1]) for entry in attribute_files)
        self.assertTrue('FSM.json' in set_of_file_names)
        self.assertTrue('SimpleFSM.json' in set_of_file_names)
        self.assertTrue('SimpleFSM.attributes.json' in set_of_file_names)
        attributes = []
        for attribute_file in attribute_files:
            parser = AttributeParser(file=attribute_file[1])
            new_attributes = parser.attributes
            if new_attributes:
                attributes.extend(new_attributes)

        self.assertEqual(len(attributes), 12)

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
        parser = AttributeParser(example_json)
        attributes = parser.attributes
        list_of_attributes = list(attributes)
        self.assertEqual(len(list_of_attributes), 1)
        attribute0 = list_of_attributes[0]
        self.assertEqual(len(attribute0.symbols), 5)
        self.assertEqual(type(attribute0.symbols[0]), Symbol)
        self.assertEqual(attribute0.symbols[0].attr_type, 'String')
        self.assertEqual(type(attribute0.symbols[1]), Symbol)
        self.assertEqual(attribute0.symbols[1].attr_type, 'Number')
        self.assertEqual(type(attribute0.symbols[2]), Symbol)
        self.assertEqual(attribute0.symbols[2].attr_type, 'Integer')
        self.assertEqual(type(attribute0.symbols[3]), Symbol)
        self.assertEqual(attribute0.symbols[3].attr_type, 'Float')
        self.assertEqual(type(attribute0.symbols[4]), Symbol)
        self.assertEqual(attribute0.symbols[4].attr_type, 'Boolean')

    def test__OneAttributes1__Valid(self):
        example_json = '''
        {
            "id0": "Number"
        }
        '''
        parser = AttributeParser(example_json)
        attributes = parser.attributes
        list_of_attributes = list(attributes)
        self.assertEqual(len(list_of_attributes), 1)
        attribute0 = list_of_attributes[0]
        self.assertEqual(type(attribute0), Symbol)
        self.assertEqual(attribute0.name, 'id0')
        self.assertEqual(attribute0.attr_type, 'Number')

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
        parser = AttributeParser(example_json)
        attributes = parser.attributes
        list_of_attributes = list(attributes)
        self.assertEqual(len(list_of_attributes), 2)
        attribute0 = list_of_attributes[0]
        self.assertEqual(attribute0.name, 'name')
        self.assertEqual(len(attribute0.symbols), 5)
        self.assertEqual(type(attribute0.symbols[0]), Symbol)
        self.assertEqual(attribute0.symbols[0].name, 'name')
        self.assertEqual(attribute0.symbols[0].attr_type, 'String')
        self.assertEqual(type(attribute0.symbols[1]), Symbol)
        self.assertEqual(attribute0.symbols[1].name, 'id0')
        self.assertEqual(attribute0.symbols[1].attr_type, 'Number')
        self.assertEqual(type(attribute0.symbols[2]), Symbol)
        self.assertEqual(attribute0.symbols[2].name, 'id1')
        self.assertEqual(attribute0.symbols[2].attr_type, 'Integer')
        self.assertEqual(type(attribute0.symbols[3]), Symbol)
        self.assertEqual(attribute0.symbols[3].name, 'id3')
        self.assertEqual(attribute0.symbols[3].attr_type, 'Float')
        self.assertEqual(type(attribute0.symbols[4]), Symbol)
        self.assertEqual(attribute0.symbols[4].name, 'id4')
        self.assertEqual(attribute0.symbols[4].attr_type, 'Boolean')

        attribute1 = list_of_attributes[1]
        self.assertEqual(type(attribute1), Symbol)
        self.assertEqual(attribute1.name, 'id4')
        self.assertEqual(attribute1.attr_type, 'Boolean')

    def test__ThreeAttributes0__Valid(self):
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
        parser = AttributeParser(example_json)
        attributes = parser.attributes
        list_of_attributes = list(attributes)
        self.assertEqual(len(list_of_attributes), 3)
        attribute0 = list_of_attributes[0]
        self.assertEqual(attribute0.name, 'name')
        self.assertEqual(len(attribute0.symbols), 5)
        self.assertEqual(type(attribute0.symbols[0]), Symbol)
        self.assertEqual(attribute0.symbols[0].name, 'name')
        self.assertEqual(attribute0.symbols[0].attr_type, 'String')
        self.assertEqual(type(attribute0.symbols[1]), Symbol)
        self.assertEqual(attribute0.symbols[1].name, 'id0')
        self.assertEqual(attribute0.symbols[1].attr_type, 'Number')
        self.assertEqual(type(attribute0.symbols[2]), Symbol)
        self.assertEqual(attribute0.symbols[2].name, 'id1')
        self.assertEqual(attribute0.symbols[2].attr_type, 'Integer')
        self.assertEqual(type(attribute0.symbols[3]), Symbol)
        self.assertEqual(attribute0.symbols[3].name, 'id3')
        self.assertEqual(attribute0.symbols[3].attr_type, 'Float')
        self.assertEqual(type(attribute0.symbols[4]), Symbol)
        self.assertEqual(attribute0.symbols[4].name, 'id4')
        self.assertEqual(attribute0.symbols[4].attr_type, 'Boolean')

        attribute1 = list_of_attributes[1]
        self.assertEqual(type(attribute1), Symbol)
        self.assertEqual(attribute1.name, 'id4')
        self.assertEqual(attribute1.attr_type, 'Boolean')

        attribute2 = list_of_attributes[2]
        self.assertEqual(type(attribute2), Symbol)
        self.assertEqual(attribute2.name, 'id5')
        self.assertEqual(attribute2.attr_type, 'Integer')

    def test__ThreeAttributes1__Valid(self):
        example_json = '''
        {
            "name0": {
              "name1": {
                "id0": "Number"
              },
              "id0": "Number",
              "id1": "Integer",
              "id3": "Float",
              "id4": "Boolean"
            },
            "id4": "Boolean",
            "id5": "Integer"
        }
        '''
        parser = AttributeParser(example_json)
        attributes = parser.attributes
        list_of_attributes = list(attributes)
        self.assertEqual(len(list_of_attributes), 3)
        attribute0 = list_of_attributes[0]
        self.assertEqual(attribute0.name, 'name0')
        self.assertEqual(len(attribute0.symbols), 5)
        sub_attribute0 = list_of_attributes[0].symbols[0]
        self.assertEqual(type(sub_attribute0), Symbol)
        self.assertEqual(sub_attribute0.name, 'name1')
        self.assertEqual(len(sub_attribute0.symbols), 1)
        self.assertEqual(type(sub_attribute0.symbols[0]), Symbol)
        self.assertEqual(sub_attribute0.symbols[0].name, 'id0')
        self.assertEqual(sub_attribute0.symbols[0].attr_type, 'Number')
        self.assertEqual(type(attribute0.symbols[1]), Symbol)
        self.assertEqual(attribute0.symbols[1].name, 'id0')
        self.assertEqual(attribute0.symbols[1].attr_type, 'Number')
        self.assertEqual(type(attribute0.symbols[2]), Symbol)
        self.assertEqual(attribute0.symbols[2].name, 'id1')
        self.assertEqual(attribute0.symbols[2].attr_type, 'Integer')
        self.assertEqual(type(attribute0.symbols[3]), Symbol)
        self.assertEqual(attribute0.symbols[3].name, 'id3')
        self.assertEqual(attribute0.symbols[3].attr_type, 'Float')
        self.assertEqual(type(attribute0.symbols[4]), Symbol)
        self.assertEqual(attribute0.symbols[4].name, 'id4')
        self.assertEqual(attribute0.symbols[4].attr_type, 'Boolean')

        attribute1 = list_of_attributes[1]
        self.assertEqual(type(attribute1), Symbol)
        self.assertEqual(attribute1.name, 'id4')
        self.assertEqual(attribute1.attr_type, 'Boolean')

        attribute2 = list_of_attributes[2]
        self.assertEqual(type(attribute2), Symbol)
        self.assertEqual(attribute2.name, 'id5')
        self.assertEqual(attribute2.attr_type, 'Integer')
