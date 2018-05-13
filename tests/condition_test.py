import unittest

from exceptions import ValidationError
from expression_parser import ExpressionParser
from hsm_types import Condition, Operation, Attribute, Indexer, Value, Function


class TestingConditional(unittest.TestCase):
    def setUp(self):
        """Currently nothing to do. Use it for initialization data before test"""
        pass

    def tearDown(self):
        """Currently nothing to do. Use it for reinitialization data after test"""
        pass

    def test__Variable_AND_Variable__Valid(self):
        example = 'k && l'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operation)
        self.assertEqual(expression[1].name, '&&')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'l')

    def test__Variable_AND_Value__Valid(self):
        example = 'k && 2'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operation)
        self.assertEqual(expression[1].name, '&&')
        self.assertEqual(type(expression[2]), Value)
        self.assertEqual(expression[2].value, '2')

    def test__Value_AND_Variable__Valid(self):
        example = '2 && k'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Value)
        self.assertEqual(expression[0].value, '2')
        self.assertEqual(type(expression[1]), Operation)
        self.assertEqual(expression[1].name, '&&')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'k')

    def test__VariableIndexer_AND_Variable__Valid(self):
        example = 'k[1] && l'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Indexer)
        self.assertEqual(type(expression[0].attribute), Attribute)
        self.assertEqual(expression[0].attribute.name, 'k')
        self.assertEqual(type(expression[1]), Operation)
        self.assertEqual(expression[1].name, '&&')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'l')

    def test_Variable_AND_VariableIndexer__Valid(self):
        example = 'k && l[1]'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operation)
        self.assertEqual(expression[1].name, '&&')
        self.assertEqual(type(expression[2]), Indexer)
        self.assertEqual(type(expression[2].attribute), Attribute)
        self.assertEqual(expression[2].attribute.name, 'l')

    def test__Variable_OR_Variable__Valid(self):
        example = 'k || l'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operation)
        self.assertEqual(expression[1].name, '||')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'l')

    def test__VariableIndexer_OR_Variable__Valid(self):
        example = 'k[1] || l'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Indexer)
        self.assertEqual(type(expression[0].attribute), Attribute)
        self.assertEqual(expression[0].attribute.name, 'k')
        self.assertEqual(type(expression[1]), Operation)
        self.assertEqual(expression[1].name, '||')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'l')

    def test__Variable_OR_VariableIndexer__Valid(self):
        example = 'k || l[1]'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operation)
        self.assertEqual(expression[1].name, '||')
        self.assertEqual(type(expression[2]), Indexer)
        self.assertEqual(type(expression[2].attribute), Attribute)
        self.assertEqual(expression[2].attribute.name, 'l')

    def test__Variable_EQUAL_Variable__Valid(self):
        example = 'k == l'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operation)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'l')

    def test__Variable_NOT_EQUAL_Variable__Valid(self):
        example = 'k != l'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operation)
        self.assertEqual(expression[1].name, '!=')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'l')

    def test__Variable_EQUAL_TYPES_Variable__Valid(self):
        example = 'k === l'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operation)
        self.assertEqual(expression[1].name, '===')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'l')

    def test__Variable_NOT_EQUAL_TYPES_Variable__Valid(self):
        example = 'k !== l'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operation)
        self.assertEqual(expression[1].name, '!==')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'l')

    def test__Variable_EQUAL_VariableIndexer__Invalid(self):
        example = 'k == l[]'
        with self.assertRaises(ValidationError) as context:
            parser = ExpressionParser(example)
            parser.parse()

    def test__VariableIndexer_EQUAL_Variable__Invalid(self):
        example = 'k[] == l'
        with self.assertRaises(ValidationError) as context:
            parser = ExpressionParser(example)
            parser.parse()

    def test__Variable_EQUAL_ActionVoid__Valid(self):
        example = 'k == isAction()'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operation)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Function)
        self.assertEqual(expression[2].name, 'isAction')
        self.assertEqual(expression[2].args, [])

    def test_Variable_EQUAL_ActionArg0Arg1__Valid(self):
        example = 'k == isAction(arg0, arg1)'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operation)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Function)
        self.assertEqual(expression[2].name, 'isAction')
        self.assertEqual(len(expression[2].args), 2)
        self.assertEqual(len(expression[2].args[0]), 1)
        self.assertEqual(type(expression[2].args[0][0]), Attribute)
        self.assertEqual(expression[2].args[0][0].name, 'arg0')
        self.assertEqual(len(expression[2].args[1]), 1)
        self.assertEqual(type(expression[2].args[1][0]), Attribute)
        self.assertEqual(expression[2].args[1][0].name, 'arg1')

    def test__ActionArg0Arg1_EQUAL_Variable__Valid(self):
        example = 'isAction(arg0, arg1) == k'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Function)
        self.assertEqual(expression[0].name, 'isAction')
        self.assertEqual(len(expression[0].args), 2)
        self.assertEqual(len(expression[0].args[0]), 1)
        self.assertEqual(type(expression[0].args[0][0]), Attribute)
        self.assertEqual(expression[0].args[0][0].name, 'arg0')
        self.assertEqual(len(expression[0].args[1]), 1)
        self.assertEqual(type(expression[0].args[1][0]), Attribute)
        self.assertEqual(expression[0].args[1][0].name, 'arg1')
        self.assertEqual(type(expression[1]), Operation)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'k')
