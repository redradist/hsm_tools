import unittest

from hsm_types import Operator, Attribute, Indexer, Value, Function, String, Object, Expression, Group
from parsers.expression_parser import ExpressionParser
from exceptions import ValidationError


class TestingExpressionParser(unittest.TestCase):
    def setUp(self):
        """Currently nothing to do. Use it for initialization data before test"""
        pass

    def tearDown(self):
        """Currently nothing to do. Use it for reinitialization data after test"""
        pass

    def test__Group_of_OperatorVariable_AND_Variable__Valid(self):
        example = "(++k && l)"
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(type(expression), Group)
        self.assertEqual(len(expression), 4)
        self.assertEqual(type(expression[0]), Operator)
        self.assertEqual(expression[0].name, '++')
        self.assertEqual(type(expression[1]), Attribute)
        self.assertEqual(expression[1].name, 'k')
        self.assertEqual(type(expression[2]), Operator)
        self.assertEqual(expression[2].name, '&&')
        self.assertEqual(type(expression[3]), Attribute)
        self.assertEqual(expression[3].name, 'l')

    def test__Group_of_Group_of_OperatorVariable_AND_Variable__Valid(self):
        example = "((++k && l))"
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(type(expression), Group)
        subexpression = expression[0]
        self.assertEqual(type(subexpression), Group)
        self.assertEqual(len(subexpression), 4)
        self.assertEqual(type(subexpression[0]), Operator)
        self.assertEqual(subexpression[0].name, '++')
        self.assertEqual(type(subexpression[1]), Attribute)
        self.assertEqual(subexpression[1].name, 'k')
        self.assertEqual(type(subexpression[2]), Operator)
        self.assertEqual(subexpression[2].name, '&&')
        self.assertEqual(type(subexpression[3]), Attribute)
        self.assertEqual(subexpression[3].name, 'l')

    def test__Group_of_Group_of_OperatorVariable_AND_Variable__Invalid(self):
        example = "({++k && l})"
        parser = ExpressionParser(example)
        with self.assertRaises(ValidationError) as context:
            parser.parse()

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

    def test__OperatorVariable_AND_Variable__Invalid(self):
        example = "{++k && l}"
        parser = ExpressionParser(example)
        with self.assertRaises(ValidationError) as context:
            parser.parse()

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

    def test__VariableComplexIndexer_AND_Variable__Valid(self):
        example = 'k[arr[1]] && l'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Indexer)
        self.assertEqual(type(expression[0].attribute), Attribute)
        self.assertEqual(expression[0].attribute.name, 'k')
        self.assertEqual(type(expression[0].expression), Indexer)
        self.assertEqual(type(expression[0].expression.attribute), Attribute)
        self.assertEqual(expression[0].expression.attribute.name, 'arr')
        self.assertEqual(type(expression[0].expression.expression), Value)
        self.assertEqual(expression[0].expression.expression.value, '1')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '&&')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'l')

    def test__VariableComplexIndexer_AND_Variable__Invalid(self):
        example = 'k[{arr[1]}] && l'
        parser = ExpressionParser(example)
        with self.assertRaises(ValidationError) as context:
            parser.parse()

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

    def test_Variable_AND_VariableComplex0Indexer__Valid(self):
        example = 'k && l[getIndex()]'
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
        self.assertEqual(type(expression[2].expression), Function)
        self.assertEqual(expression[2].expression.name, 'getIndex')
        self.assertEqual(len(expression[2].expression.args), 0)

    def test_Variable_AND_VariableComplex1Indexer__Valid(self):
        example = 'k && l[getIndex() { return 1; }]'
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
        self.assertEqual(type(expression[2].expression), Function)
        self.assertEqual(expression[2].expression.name, 'getIndex')
        self.assertEqual(len(expression[2].expression.args), 0)
        self.assertEqual(expression[2].expression.body, ' return 1; ')

    def test_Variable_AND_VariableIndexer__Invalid(self):
        example = 'k && l[{1}]'
        parser = ExpressionParser(example)
        with self.assertRaises(ValidationError) as context:
            parser.parse()

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
        self.assertEqual(type(expression[2].args[0]), Attribute)
        self.assertEqual(expression[2].args[0].name, 'arg0')
        self.assertEqual(type(expression[2].args[1]), Attribute)
        self.assertEqual(expression[2].args[1].name, 'arg1')

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
        self.assertEqual(type(expression[2].args[0]), Attribute)
        self.assertEqual(expression[2].args[0].name, 'arg0')
        self.assertEqual(type(expression[2].args[1]), Attribute)
        self.assertEqual(expression[2].args[1].name, 'arg1')

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
        self.assertEqual(type(expression[2].args[0]), Attribute)
        self.assertEqual(expression[2].args[0].name, 'arg0')
        self.assertEqual(type(expression[2].args[1]), Attribute)
        self.assertEqual(expression[2].args[1].name, 'arg1')

    def test_Variable_EQUAL_NamespaceActionArgExpression0Arg1__Valid(self):
        example = 'k == MyNameSpace::isAction(arg0 == 1, arg1)'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Function)
        self.assertEqual(expression[2].name, 'MyNameSpace::isAction')
        self.assertEqual(len(expression[2].args), 2)
        self.assertEqual(type(expression[2].args[0]), Expression)
        self.assertEqual(len(expression[2].args[0]), 3)
        self.assertEqual(type(expression[2].args[0][0]), Attribute)
        self.assertEqual(expression[2].args[0][0].name, 'arg0')
        self.assertEqual(type(expression[2].args[0][1]), Operator)
        self.assertEqual(expression[2].args[0][1].name, '==')
        self.assertEqual(type(expression[2].args[0][2]), Value)
        self.assertEqual(expression[2].args[0][2].value, '1')
        self.assertEqual(type(expression[2].args[1]), Attribute)
        self.assertEqual(expression[2].args[1].name, 'arg1')

    def test_Variable_EQUAL_NamespaceActionArgExpression1Arg1__Valid(self):
        example = 'k == MyNameSpace::isAction(1 == arg0, arg1)'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Function)
        self.assertEqual(expression[2].name, 'MyNameSpace::isAction')
        self.assertEqual(len(expression[2].args), 2)
        self.assertEqual(type(expression[2].args[0]), Expression)
        self.assertEqual(len(expression[2].args[0]), 3)
        self.assertEqual(type(expression[2].args[0][0]), Value)
        self.assertEqual(expression[2].args[0][0].value, '1')
        self.assertEqual(type(expression[2].args[0][1]), Operator)
        self.assertEqual(expression[2].args[0][1].name, '==')
        self.assertEqual(type(expression[2].args[0][2]), Attribute)
        self.assertEqual(expression[2].args[0][2].name, 'arg0')
        self.assertEqual(type(expression[2].args[1]), Attribute)
        self.assertEqual(expression[2].args[1].name, 'arg1')

    def test_Variable_EQUAL_NamespaceActionArgExpression2Arg1__Valid(self):
        example = 'k == MyNameSpace::isAction(arg0 = k, arg1)'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Function)
        self.assertEqual(expression[2].name, 'MyNameSpace::isAction')
        self.assertEqual(len(expression[2].args), 2)
        self.assertEqual(type(expression[2].args[0]), Expression)
        self.assertEqual(len(expression[2].args[0]), 3)
        self.assertEqual(type(expression[2].args[0][0]), Attribute)
        self.assertEqual(expression[2].args[0][0].name, 'arg0')
        self.assertEqual(type(expression[2].args[0][1]), Operator)
        self.assertEqual(expression[2].args[0][1].name, '=')
        self.assertEqual(type(expression[2].args[0][2]), Attribute)
        self.assertEqual(expression[2].args[0][2].name, 'k')
        self.assertEqual(type(expression[2].args[1]), Attribute)
        self.assertEqual(expression[2].args[1].name, 'arg1')

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
        self.assertEqual(type(expression[2].args[0]), Attribute)
        self.assertEqual(expression[2].args[0].name, 'arg0')
        self.assertEqual(type(expression[2].args[1]), Attribute)
        self.assertEqual(expression[2].args[1].name, 'arg1')
        self.assertEqual(expression[2].body, ' arg0 = arg1; ')

    def test_Variable_EQUAL_AnonymousActionArg0Arg1Body__Valid(self):
        example = 'k == (arg0, arg1) { arg0 = arg1; }'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Function)
        self.assertEqual(expression[2].name, None)
        self.assertEqual(len(expression[2].args), 2)
        self.assertEqual(type(expression[2].args[0]), Attribute)
        self.assertEqual(expression[2].args[0].name, 'arg0')
        self.assertEqual(type(expression[2].args[1]), Attribute)
        self.assertEqual(expression[2].args[1].name, 'arg1')
        self.assertEqual(expression[2].body, ' arg0 = arg1; ')

    def test_Variable_EQUAL_AnonymousActionArg0Arg1Body__ReturnAuto__Valid(self):
        example = 'k == (arg0, arg1) -> { arg0 = arg1; }'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Function)
        self.assertEqual(expression[2].name, None)
        self.assertEqual(len(expression[2].args), 2)
        self.assertEqual(type(expression[2].args[0]), Attribute)
        self.assertEqual(expression[2].args[0].name, 'arg0')
        self.assertEqual(type(expression[2].args[1]), Attribute)
        self.assertEqual(expression[2].args[1].name, 'arg1')
        self.assertEqual(expression[2].body, ' arg0 = arg1; ')

    def test__AnonymousActionArg0Arg1Body__ReturnAuto__EQUAL__Variable__Valid(self):
        example = '(arg0, arg1) -> { arg0 = arg1; } == k'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Function)
        self.assertEqual(expression[0].name, None)
        self.assertEqual(len(expression[0].args), 2)
        self.assertEqual(type(expression[0].args[0]), Attribute)
        self.assertEqual(expression[0].args[0].name, 'arg0')
        self.assertEqual(type(expression[0].args[1]), Attribute)
        self.assertEqual(expression[0].args[1].name, 'arg1')
        self.assertEqual(expression[0].body, ' arg0 = arg1; ')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'k')

    def test_Variable_EQUAL_AnonymousActionArg0Arg1Body__ReturnBool__Valid(self):
        example = 'k == (arg0, arg1) -> bool { arg0 = arg1; }'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Function)
        self.assertEqual(expression[2].name, None)
        self.assertEqual(len(expression[2].args), 2)
        self.assertEqual(type(expression[2].args[0]), Attribute)
        self.assertEqual(expression[2].args[0].name, 'arg0')
        self.assertEqual(type(expression[2].args[1]), Attribute)
        self.assertEqual(expression[2].args[1].name, 'arg1')
        self.assertEqual(expression[2].return_value, 'bool')
        self.assertEqual(expression[2].body, ' arg0 = arg1; ')

    def test__AnonymousActionArg0Arg1Body__ReturnBool__EQUAL__Variable__Valid(self):
        example = '(arg0, arg1) -> bool { arg0 = arg1; } == k'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Function)
        self.assertEqual(expression[0].name, None)
        self.assertEqual(len(expression[0].args), 2)
        self.assertEqual(type(expression[0].args[0]), Attribute)
        self.assertEqual(expression[0].args[0].name, 'arg0')
        self.assertEqual(type(expression[0].args[1]), Attribute)
        self.assertEqual(expression[0].args[1].name, 'arg1')
        self.assertEqual(expression[0].body, ' arg0 = arg1; ')
        self.assertEqual(expression[0].return_value, 'bool')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'k')

    def test_Variable_EQUAL_AnonymousActionArg0Arg1Body__ReturnStdString__Valid(self):
        example = 'k == (arg0, arg1) -> std::string { arg0 = arg1; }'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Attribute)
        self.assertEqual(expression[0].name, 'k')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Function)
        self.assertEqual(expression[2].name, None)
        self.assertEqual(len(expression[2].args), 2)
        self.assertEqual(type(expression[2].args[0]), Attribute)
        self.assertEqual(expression[2].args[0].name, 'arg0')
        self.assertEqual(type(expression[2].args[1]), Attribute)
        self.assertEqual(expression[2].args[1].name, 'arg1')
        self.assertEqual(expression[2].return_value, 'std::string')
        self.assertEqual(expression[2].body, ' arg0 = arg1; ')

    def test__AnonymousActionArg0Arg1Body__ReturnStdString__EQUAL__Variable__Valid(self):
        example = '(arg0, arg1) -> std::string { arg0 = arg1; } == k'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Function)
        self.assertEqual(expression[0].name, None)
        self.assertEqual(len(expression[0].args), 2)
        self.assertEqual(type(expression[0].args[0]), Attribute)
        self.assertEqual(expression[0].args[0].name, 'arg0')
        self.assertEqual(type(expression[0].args[1]), Attribute)
        self.assertEqual(expression[0].args[1].name, 'arg1')
        self.assertEqual(expression[0].body, ' arg0 = arg1; ')
        self.assertEqual(expression[0].return_value, 'std::string')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'k')

    def test_Variable_EQUAL_ActionArg0Arg1Body_DoubleBraces__Valid(self):
        example = 'k == isAction(arg0, arg1) { { arg0 = arg1; } }'
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
        self.assertEqual(type(expression[2].args[0]), Attribute)
        self.assertEqual(expression[2].args[0].name, 'arg0')
        self.assertEqual(type(expression[2].args[1]), Attribute)
        self.assertEqual(expression[2].args[1].name, 'arg1')
        self.assertEqual(expression[2].body, ' { arg0 = arg1; } ')

    def test_Variable_EQUAL_ActionArg0Arg1Body__ReturnAuto__Valid(self):
        example = 'k == isAction(arg0, arg1) -> { arg0 = arg1; return arg0; }'
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
        self.assertEqual(type(expression[2].args[0]), Attribute)
        self.assertEqual(expression[2].args[0].name, 'arg0')
        self.assertEqual(type(expression[2].args[1]), Attribute)
        self.assertEqual(expression[2].args[1].name, 'arg1')
        self.assertEqual(expression[2].body, ' arg0 = arg1; return arg0; ')

    def test_Variable_EQUAL_ActionArg0Arg1Body_ReturnValue__Valid(self):
        example = 'k == isAction(arg0, arg1) -> bool { arg0 = arg1; return arg0; }'
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
        self.assertEqual(type(expression[2].args[0]), Attribute)
        self.assertEqual(expression[2].args[0].name, 'arg0')
        self.assertEqual(type(expression[2].args[1]), Attribute)
        self.assertEqual(expression[2].args[1].name, 'arg1')
        self.assertEqual(expression[2].return_value, 'bool')
        self.assertEqual(expression[2].body, ' arg0 = arg1; return arg0; ')

    def test_Variable_EQUAL_ActionArg0Arg1Body_ReturnStdString__Valid(self):
        example = 'k == isAction(arg0, arg1) -> std::string { arg0 = arg1; return arg0; }'
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
        self.assertEqual(type(expression[2].args[0]), Attribute)
        self.assertEqual(expression[2].args[0].name, 'arg0')
        self.assertEqual(type(expression[2].args[1]), Attribute)
        self.assertEqual(expression[2].args[1].name, 'arg1')
        self.assertEqual(expression[2].return_value, 'std::string')
        self.assertEqual(expression[2].body, ' arg0 = arg1; return arg0; ')

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
        self.assertEqual(type(expression[2].args[0]), Expression)
        self.assertEqual(len(expression[2].args[0]), 3)
        self.assertEqual(type(expression[2].args[0][0]), Attribute)
        self.assertEqual(expression[2].args[0][0].name, 'arg0')
        self.assertEqual(type(expression[2].args[0][1]), Operator)
        self.assertEqual(expression[2].args[0][1].name, '==')
        self.assertEqual(type(expression[2].args[0][2]), Attribute)
        self.assertEqual(expression[2].args[0][2].name, 'arg2')
        self.assertEqual(type(expression[2].args[1]), Attribute)
        self.assertEqual(expression[2].args[1].name, 'arg1')

    def test__ActionArg0Arg1_EQUAL_Variable__Valid(self):
        example = 'isAction(arg0, arg1) == k'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Function)
        self.assertEqual(expression[0].name, 'isAction')
        self.assertEqual(len(expression[0].args), 2)
        self.assertEqual(type(expression[0].args[0]), Attribute)
        self.assertEqual(expression[0].args[0].name, 'arg0')
        self.assertEqual(type(expression[0].args[1]), Attribute)
        self.assertEqual(expression[0].args[1].name, 'arg1')
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
        self.assertEqual(type(expression[0].args[0]), Attribute)
        self.assertEqual(expression[0].args[0].name, 'arg0')
        self.assertEqual(type(expression[0].args[1]), Attribute)
        self.assertEqual(expression[0].args[1].name, 'arg1')
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
        self.assertEqual(type(expression[0].args[0]), Attribute)
        self.assertEqual(expression[0].args[0].name, 'arg0')
        self.assertEqual(type(expression[0].args[1]), Attribute)
        self.assertEqual(expression[0].args[1].name, 'arg1')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'k')

    def test__NamespaceActionArgExpression0Arg1_EQUAL_Variable__Valid(self):
        example = 'MyNamespace::isAction(arg0 == 1, arg1) == k'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Function)
        self.assertEqual(expression[0].name, 'MyNamespace::isAction')
        self.assertEqual(len(expression[0].args), 2)
        self.assertEqual(type(expression[0].args[0]), Expression)
        self.assertEqual(len(expression[0].args[0]), 3)
        self.assertEqual(type(expression[0].args[0][0]), Attribute)
        self.assertEqual(expression[0].args[0][0].name, 'arg0')
        self.assertEqual(type(expression[0].args[0][1]), Operator)
        self.assertEqual(expression[0].args[0][1].name, '==')
        self.assertEqual(type(expression[0].args[0][2]), Value)
        self.assertEqual(expression[0].args[0][2].value, '1')
        self.assertEqual(type(expression[0].args[1]), Attribute)
        self.assertEqual(expression[0].args[1].name, 'arg1')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'k')

    def test__NamespaceActionArgExpression1Arg1_EQUAL_Variable__Valid(self):
        example = 'MyNamespace::isAction(1 == arg0, arg1) == k'
        parser = ExpressionParser(example)
        expression = parser.parse()
        self.assertEqual(len(expression), 3)
        self.assertEqual(type(expression[0]), Function)
        self.assertEqual(expression[0].name, 'MyNamespace::isAction')
        self.assertEqual(len(expression[0].args), 2)
        self.assertEqual(type(expression[0].args[0]), Expression)
        self.assertEqual(len(expression[0].args[0]), 3)
        self.assertEqual(type(expression[0].args[0][0]), Value)
        self.assertEqual(expression[0].args[0][0].value, '1')
        self.assertEqual(type(expression[0].args[0][1]), Operator)
        self.assertEqual(expression[0].args[0][1].name, '==')
        self.assertEqual(type(expression[0].args[0][2]), Attribute)
        self.assertEqual(expression[0].args[0][2].name, 'arg0')
        self.assertEqual(type(expression[0].args[1]), Attribute)
        self.assertEqual(expression[0].args[1].name, 'arg1')
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
        self.assertEqual(type(expression[0].args[0]), Attribute)
        self.assertEqual(expression[0].args[0].name, 'arg0')
        self.assertEqual(type(expression[0].args[1]), Attribute)
        self.assertEqual(expression[0].args[1].name, 'arg1')
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
        self.assertEqual(type(expression[0].args[1]), Attribute)
        self.assertEqual(expression[0].args[1].name, 'arg1')
        self.assertEqual(type(expression[1]), Operator)
        self.assertEqual(expression[1].name, '==')
        self.assertEqual(type(expression[2]), Attribute)
        self.assertEqual(expression[2].name, 'k')
