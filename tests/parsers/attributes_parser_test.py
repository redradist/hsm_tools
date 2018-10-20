import unittest

from src.fsm_types import Symbol
from src.parsers.attributes_parser import AttributeParser


class TestingAttributesParser(unittest.TestCase):
    def setUp(self):
        """Currently nothing to do. Use it for initialization data before test"""
        pass

    def tearDown(self):
        """Currently nothing to do. Use it for reinitialization data after test"""
        pass

    def test__FindAllAttributesFiles__Valid(self):
        attribute_files = AttributeParser.find_all_attribute_files('../simple_fsm')
        self.assertEqual(len(attribute_files), 1)

    def test__ParseAllAttributesFiles__Valid(self):
        attribute_files = AttributeParser.find_all_attribute_files('../simple_fsm')
        self.assertEqual(len(attribute_files), 1)
        attributes = []
        parser = AttributeParser()
        for attribute_file in attribute_files:
            new_attributes = parser.parse_file(attribute_file[1])
            if new_attributes:
                attributes.extend(new_attributes)

        self.assertEqual(len(attributes), 2)

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
        parser = AttributeParser()
        attributes = parser.parse_json(example_json)
        list_of_attributes = list(attributes)
        self.assertEqual(len(list_of_attributes), 1)
        attribute0 = list_of_attributes[0]
        self.assertEqual(len(attribute0.args), 5)
        self.assertEqual(type(attribute0.args[0]), Symbol)
        self.assertEqual(attribute0.args[0].attr_type, 'String')
        self.assertEqual(type(attribute0.args[1]), Symbol)
        self.assertEqual(attribute0.args[1].attr_type, 'Number')
        self.assertEqual(type(attribute0.args[2]), Symbol)
        self.assertEqual(attribute0.args[2].attr_type, 'Integer')
        self.assertEqual(type(attribute0.args[3]), Symbol)
        self.assertEqual(attribute0.args[3].attr_type, 'Float')
        self.assertEqual(type(attribute0.args[4]), Symbol)
        self.assertEqual(attribute0.args[4].attr_type, 'Boolean')

    def test__OneAttributes1__Valid(self):
        example_json = '''
        {
            "id0": "Number"
        }
        '''
        parser = AttributeParser()
        attributes = parser.parse_json(example_json)
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
        parser = AttributeParser()
        attributes = parser.parse_json(example_json)
        list_of_attributes = list(attributes)
        self.assertEqual(len(list_of_attributes), 2)
        attribute0 = list_of_attributes[0]
        self.assertEqual(attribute0.name, 'name')
        self.assertEqual(len(attribute0.args), 5)
        self.assertEqual(type(attribute0.args[0]), Symbol)
        self.assertEqual(attribute0.args[0].name, 'name')
        self.assertEqual(attribute0.args[0].attr_type, 'String')
        self.assertEqual(type(attribute0.args[1]), Symbol)
        self.assertEqual(attribute0.args[1].name, 'id0')
        self.assertEqual(attribute0.args[1].attr_type, 'Number')
        self.assertEqual(type(attribute0.args[2]), Symbol)
        self.assertEqual(attribute0.args[2].name, 'id1')
        self.assertEqual(attribute0.args[2].attr_type, 'Integer')
        self.assertEqual(type(attribute0.args[3]), Symbol)
        self.assertEqual(attribute0.args[3].name, 'id3')
        self.assertEqual(attribute0.args[3].attr_type, 'Float')
        self.assertEqual(type(attribute0.args[4]), Symbol)
        self.assertEqual(attribute0.args[4].name, 'id4')
        self.assertEqual(attribute0.args[4].attr_type, 'Boolean')

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
        parser = AttributeParser()
        attributes = parser.parse_json(example_json)
        list_of_attributes = list(attributes)
        self.assertEqual(len(list_of_attributes), 3)
        attribute0 = list_of_attributes[0]
        self.assertEqual(attribute0.name, 'name')
        self.assertEqual(len(attribute0.args), 5)
        self.assertEqual(type(attribute0.args[0]), Symbol)
        self.assertEqual(attribute0.args[0].name, 'name')
        self.assertEqual(attribute0.args[0].attr_type, 'String')
        self.assertEqual(type(attribute0.args[1]), Symbol)
        self.assertEqual(attribute0.args[1].name, 'id0')
        self.assertEqual(attribute0.args[1].attr_type, 'Number')
        self.assertEqual(type(attribute0.args[2]), Symbol)
        self.assertEqual(attribute0.args[2].name, 'id1')
        self.assertEqual(attribute0.args[2].attr_type, 'Integer')
        self.assertEqual(type(attribute0.args[3]), Symbol)
        self.assertEqual(attribute0.args[3].name, 'id3')
        self.assertEqual(attribute0.args[3].attr_type, 'Float')
        self.assertEqual(type(attribute0.args[4]), Symbol)
        self.assertEqual(attribute0.args[4].name, 'id4')
        self.assertEqual(attribute0.args[4].attr_type, 'Boolean')

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
        parser = AttributeParser()
        attributes = parser.parse_json(example_json)
        list_of_attributes = list(attributes)
        self.assertEqual(len(list_of_attributes), 3)
        attribute0 = list_of_attributes[0]
        self.assertEqual(attribute0.name, 'name0')
        self.assertEqual(len(attribute0.args), 5)
        sub_attribute0 = list_of_attributes[0].args[0]
        self.assertEqual(type(sub_attribute0), Symbol)
        self.assertEqual(sub_attribute0.name, 'name1')
        self.assertEqual(len(sub_attribute0.args), 1)
        self.assertEqual(type(sub_attribute0.args[0]), Symbol)
        self.assertEqual(sub_attribute0.args[0].name, 'id0')
        self.assertEqual(sub_attribute0.args[0].attr_type, 'Number')
        self.assertEqual(type(attribute0.args[1]), Symbol)
        self.assertEqual(attribute0.args[1].name, 'id0')
        self.assertEqual(attribute0.args[1].attr_type, 'Number')
        self.assertEqual(type(attribute0.args[2]), Symbol)
        self.assertEqual(attribute0.args[2].name, 'id1')
        self.assertEqual(attribute0.args[2].attr_type, 'Integer')
        self.assertEqual(type(attribute0.args[3]), Symbol)
        self.assertEqual(attribute0.args[3].name, 'id3')
        self.assertEqual(attribute0.args[3].attr_type, 'Float')
        self.assertEqual(type(attribute0.args[4]), Symbol)
        self.assertEqual(attribute0.args[4].name, 'id4')
        self.assertEqual(attribute0.args[4].attr_type, 'Boolean')

        attribute1 = list_of_attributes[1]
        self.assertEqual(type(attribute1), Symbol)
        self.assertEqual(attribute1.name, 'id4')
        self.assertEqual(attribute1.attr_type, 'Boolean')

        attribute2 = list_of_attributes[2]
        self.assertEqual(type(attribute2), Symbol)
        self.assertEqual(attribute2.name, 'id5')
        self.assertEqual(attribute2.attr_type, 'Integer')