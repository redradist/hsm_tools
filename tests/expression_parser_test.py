import unittest

from hsm_types import Operator, Attribute, Indexer, Value, Function, String, Object
from expression_parser import ExpressionParser
from exceptions import ValidationError


class TestingExpressionParser(unittest.TestCase):
    def setUp(self):
        """Currently nothing to do. Use it for initialization data before test"""
        pass

    def tearDown(self):
        """Currently nothing to do. Use it for reinitialization data after test"""
        pass

    def test__OperatorVariable_AND_Variable__Valid(self):
        example = "++k && l"
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 4)
        self.assertEqual(type(expression[0]), Operator)
        self.assertEqual(expression[0].name, '++')
        self.assertEqual(type(expression[1]), Attribute)
        self.assertEqual(expression[1].name, 'k')
        self.assertEqual(type(expression[2]), Operator)
        self.assertEqual(expression[2].name, '&&')
        self.assertEqual(type(expression[3]), Attribute)
        self.assertEqual(expression[3].name, 'l')

    def test__VariableOperator_AND_Variable__Valid(self):
        example = "k++ && l"
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 4)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '++')
        self.assertEqual(type(expression[2]), Operator)
        self.assertEqual(expression[2].name, '&&')
        self.assertEqual(type(expression[3]), Attribute)
        self.assertEqual(expression[3].name, 'l')

    def test__Variable_AND_OperatorVariable__Valid(self):
        example = "k && ++l"
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 4)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '&&')
        self.assertEqual(type(expression[2]), Operator)
        self.assertEqual(expression[2].name, '++')
        self.assertEqual(type(expression[3]), Attribute)
        self.assertEqual(expression[3].name, 'l')

    def test__Variable_AND_VariableOperator__Valid(self):
        example = "k && l++"
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 4)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '&&')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'l')
        self.assertEqual(type(expression[3]), Operator)
        self.assertEqual(expression[3].name, '++')

    def test__Variable_AND_StringType0__Valid(self):
        example = "k && 'My String'"
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '&&')
        self.assertEqual(type(expression[2]), String)
        self.assertEqual(expression[2].name, 'My String')

    def test__Variable_AND_StringType1__Valid(self):
        example = 'k && "My String"'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '&&')
        self.assertEqual(type(expression[2]), String)
        self.assertEqual(expression[2].name, 'My String')

    def test__StringType0_AND_Variable__Valid(self):
        example = "'My String' && l"
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), String)
        self.assertEqual(expression[0].name, 'My String')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '&&')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'l')

    def test__StringType1_AND_Variable__Valid(self):
        example = '"My String" && l'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), String)
        self.assertEqual(expression[0].name, 'My String')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '&&')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'l')

    def test__Variable_AND_Variable__Valid(self):
        example = 'k && l'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
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
        self.assertEqual(type(expression[1]), Operator)
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
        self.assertEqual(type(expression[1]), Operator)
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
        self.assertEqual(type(expression[1]), Operator)
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
        self.assertEqual(type(expression[1]), Operator)
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
        self.assertEqual(type(expression[1]), Operator)
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
        self.assertEqual(type(expression[1]), Operator)
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
        self.assertEqual(type(expression[1]), Operator)
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
        self.assertEqual(type(expression[1]), Operator)
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
        self.assertEqual(type(expression[1]), Operator)
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
        self.assertEqual(type(expression[1]), Operator)
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
        self.assertEqual(type(expression[1]), Operator)
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
        self.assertEqual(type(expression[1]), Operator)
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
        self.assertEqual(type(expression[1]), Operator)
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

    def test_Variable_EQUAL_ObjectActionArg0Arg1__Valid(self):
        example = 'k == name.isAction(arg0, arg1)'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Function)
        self.assertEqual(expression[2].name, 'isAction')
        self.assertEqual(type(expression[2].object), Object)
        self.assertEqual(expression[2].object.name, 'name')
        self.assertEqual(len(expression[2].args), 2)
        self.assertEqual(len(expression[2].args[0]), 1)
        self.assertEqual(type(expression[2].args[0][0]), Attribute)
        self.assertEqual(expression[2].args[0][0].name, 'arg0')
        self.assertEqual(len(expression[2].args[1]), 1)
        self.assertEqual(type(expression[2].args[1][0]), Attribute)
        self.assertEqual(expression[2].args[1][0].name, 'arg1')

    def test_Variable_EQUAL_NamespaceActionArg0Arg1__Valid(self):
        example = 'k == MyNamespace::isAction(arg0, arg1)'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Function)
        self.assertEqual(expression[2].name, 'MyNamespace::isAction')
        self.assertEqual(len(expression[2].args), 2)
        self.assertEqual(len(expression[2].args[0]), 1)
        self.assertEqual(type(expression[2].args[0][0]), Attribute)
        self.assertEqual(expression[2].args[0][0].name, 'arg0')
        self.assertEqual(len(expression[2].args[1]), 1)
        self.assertEqual(type(expression[2].args[1][0]), Attribute)
        self.assertEqual(expression[2].args[1][0].name, 'arg1')

    def test_Variable_EQUAL_ActionArg0Arg1Body__Valid(self):
        example = 'k == isAction(arg0, arg1) { arg0 = arg1; }'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
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
        self.assertEqual(expression[2].body, ' arg0 = arg1; ')

    def test_Variable_EQUAL_ActionArgExpressionArg1__Valid(self):
        example = 'k == isAction(arg0 == arg2, arg1)'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Function)
        self.assertEqual(expression[2].name, 'isAction')
        self.assertEqual(len(expression[2].args), 2)
        self.assertEqual(len(expression[2].args[0]), 3)
        self.assertEqual(type(expression[2].args[0][0]), Attribute)
        self.assertEqual(expression[2].args[0][0].name, 'arg0')
        self.assertEqual(type(expression[2].args[0][1]), Operator)
        self.assertEqual(expression[2].args[0][1].name, '==')
        self.assertEqual(type(expression[2].args[0][2]), Attribute)
        self.assertEqual(expression[2].args[0][2].name, 'arg2')
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
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'k')

    def test__ObjectActionArg0Arg1_EQUAL_Variable__Valid(self):
        example = 'name.isAction(arg0, arg1) == k'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Function)
        self.assertEqual(expression[0].name, 'isAction')
        self.assertEqual(type(expression[0].object), Object)
        self.assertEqual(expression[0].object.name, 'name')
        self.assertEqual(len(expression[0].args), 2)
        self.assertEqual(len(expression[0].args[0]), 1)
        self.assertEqual(type(expression[0].args[0][0]), Attribute)
        self.assertEqual(expression[0].args[0][0].name, 'arg0')
        self.assertEqual(len(expression[0].args[1]), 1)
        self.assertEqual(type(expression[0].args[1][0]), Attribute)
        self.assertEqual(expression[0].args[1][0].name, 'arg1')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'k')

    def test__NamespaceActionArg0Arg1_EQUAL_Variable__Valid(self):
        example = 'MyNamespace::isAction(arg0, arg1) == k'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Function)
        self.assertEqual(expression[0].name, 'MyNamespace::isAction')
        self.assertEqual(len(expression[0].args), 2)
        self.assertEqual(len(expression[0].args[0]), 1)
        self.assertEqual(type(expression[0].args[0][0]), Attribute)
        self.assertEqual(expression[0].args[0][0].name, 'arg0')
        self.assertEqual(len(expression[0].args[1]), 1)
        self.assertEqual(type(expression[0].args[1][0]), Attribute)
        self.assertEqual(expression[0].args[1][0].name, 'arg1')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'k')

    def test__ActionArg0Arg1Body_EQUAL_Variable__Valid(self):
        example = 'isAction(arg0, arg1) { arg0 = arg1; } == k'
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
        self.assertEqual(expression[0].body, ' arg0 = arg1; ')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'k')

    def test__ActionArgExpressionArg1_EQUAL_Variable__Valid(self):
        example = 'isAction(arg0 == arg2, arg1) == k'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Function)
        self.assertEqual(expression[0].name, 'isAction')
        self.assertEqual(len(expression[0].args), 2)
        self.assertEqual(len(expression[0].args[0]), 3)
        self.assertEqual(type(expression[0].args[0][0]), Attribute)
        self.assertEqual(expression[0].args[0][0].name, 'arg0')
        self.assertEqual(type(expression[0].args[0][1]), Operator)
        self.assertEqual(expression[0].args[0][1].name, '==')
        self.assertEqual(type(expression[0].args[0][2]), Attribute)
        self.assertEqual(expression[0].args[0][2].name, 'arg2')
        self.assertEqual(len(expression[0].args[1]), 1)
        self.assertEqual(type(expression[0].args[1][0]), Attribute)
        self.assertEqual(expression[0].args[1][0].name, 'arg1')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'k')
