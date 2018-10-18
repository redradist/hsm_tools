import unittest

from src.exceptions import ValidationError
from src.fsm_types import Function, Value, Attribute, Group, Operator, String, Indexer, Expression, Object, Type, \
    FunctionCall, Lambda
from src.parsers.expression_parser import ExpressionParser


class TestingExpressionParser(unittest.TestCase):
    def setUp(self):
        """Currently nothing to do. Use it for initialization data before test"""
        pass

    def tearDown(self):
        """Currently nothing to do. Use it for reinitialization data after test"""
        pass

    # def test__ActionDefinitionArgType__Valid(self):
    #     example = "Action2(int k)"
    #     parser = ExpressionParser(example)
    #     ast = parser.get_ast()
    #     self.assertEqual(type(ast), FunctionCall)
    #     self.assertEqual(len(ast.args), 2)
    #     self.assertEqual(type(ast.args[0]), Attribute)
    #     self.assertEqual(ast.args[0].type, 'int')
    #     self.assertEqual(type(ast.args[1]), Attribute)
    #     self.assertEqual(ast.args[1].type, 'k')

    def test__ActionArgValue__Valid(self):
        example = "Action2(2)"
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(type(ast), FunctionCall)
        self.assertEqual(len(ast.args), 1)
        self.assertEqual(type(ast.args[0]), Value)
        self.assertEqual(ast.args[0].value, '2')

    def test__ActionUnderScoreNameArgValue__Valid(self):
        example = "my_action(2)"
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(type(ast), FunctionCall)
        self.assertEqual(len(ast.args), 1)
        self.assertEqual(type(ast.args[0]), Value)
        self.assertEqual(ast.args[0].value, '2')

    def test__ActionArgAttribute__Valid(self):
        example = "Action2(k)"
        parser = ExpressionParser(example)
        expression = parser.get_ast()
        self.assertEqual(type(expression), FunctionCall)
        self.assertEqual(len(expression.args), 1)
        self.assertEqual(type(expression.args[0]), Attribute)
        self.assertEqual(expression.args[0].name, 'k')

    def test__Group_of_OperatorVariable_AND_Variable__Valid(self):
        example = "(++k && l)"
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(type(ast), Expression)
        self.assertEqual(len(ast), 4)
        self.assertEqual(type(ast[0]), Operator)
        self.assertEqual(ast[0].name, '++')
        self.assertEqual(type(ast[1]), Attribute)
        self.assertEqual(ast[1].name, 'k')
        self.assertEqual(type(ast[2]), Operator)
        self.assertEqual(ast[2].name, '&&')
        self.assertEqual(type(ast[3]), Attribute)
        self.assertEqual(ast[3].name, 'l')

    def test__Group_of_Group_of_OperatorVariable_AND_Variable__Valid(self):
        example = "((++k && l))"
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(type(ast), Expression)
        self.assertEqual(len(ast), 4)
        self.assertEqual(type(ast[0]), Operator)
        self.assertEqual(ast[0].name, '++')
        self.assertEqual(type(ast[1]), Attribute)
        self.assertEqual(ast[1].name, 'k')
        self.assertEqual(type(ast[2]), Operator)
        self.assertEqual(ast[2].name, '&&')
        self.assertEqual(type(ast[3]), Attribute)
        self.assertEqual(ast[3].name, 'l')

    def test__Group_of_Group_of_OperatorVariable_AND_Variable__Invalid(self):
        example = "({++k && l})"
        with self.assertRaises(ValidationError) as context:
            parser = ExpressionParser(example)

    def test__OperatorVariable_AND_Variable__Valid(self):
        example = "++k && l"
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 4)
        self.assertEqual(type(ast[0]), Operator)
        self.assertEqual(ast[0].name, '++')
        self.assertEqual(type(ast[1]), Attribute)
        self.assertEqual(ast[1].name, 'k')
        self.assertEqual(type(ast[2]), Operator)
        self.assertEqual(ast[2].name, '&&')
        self.assertEqual(type(ast[3]), Attribute)
        self.assertEqual(ast[3].name, 'l')

    def test__OperatorVariable_AND_Variable__Invalid(self):
        example = "{++k && l}"
        with self.assertRaises(ValidationError) as context:
            parser = ExpressionParser(example)

    def test__VariableOperator_AND_Variable__Valid(self):
        example = "k++ && l"
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 4)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '++')
        self.assertEqual(type(ast[2]), Operator)
        self.assertEqual(ast[2].name, '&&')
        self.assertEqual(type(ast[3]), Attribute)
        self.assertEqual(ast[3].name, 'l')

    def test__Variable_AND_OperatorVariable__Valid(self):
        example = "k && ++l"
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 4)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '&&')
        self.assertEqual(type(ast[2]), Operator)
        self.assertEqual(ast[2].name, '++')
        self.assertEqual(type(ast[3]), Attribute)
        self.assertEqual(ast[3].name, 'l')

    def test__VariableInitializer_AND_OperatorVariable__Valid(self):
        example = "k{1} && ++l"
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 4)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(len(ast[0].args), 1)
        self.assertEqual(type(ast[0].args[0]), Value)
        self.assertEqual(ast[0].args[0].value, '1')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '&&')
        self.assertEqual(type(ast[2]), Operator)
        self.assertEqual(ast[2].name, '++')
        self.assertEqual(type(ast[3]), Attribute)
        self.assertEqual(ast[3].name, 'l')

    def test__OperatorVariable_AND_VariableInitializer__Valid(self):
        example = "++k && l{1}"
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 4)
        self.assertEqual(type(ast[0]), Operator)
        self.assertEqual(ast[0].name, '++')
        self.assertEqual(type(ast[1]), Attribute)
        self.assertEqual(ast[1].name, 'k')
        self.assertEqual(type(ast[2]), Operator)
        self.assertEqual(ast[2].name, '&&')
        self.assertEqual(type(ast[3]), Attribute)
        self.assertEqual(ast[3].name, 'l')
        self.assertEqual(len(ast[3].args), 1)
        self.assertEqual(type(ast[3].args[0]), Value)
        self.assertEqual(ast[3].args[0].value, '1')

    def test__Variable_AND_VariableOperator__Valid(self):
        example = "k && l++"
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 4)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '&&')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'l')
        self.assertEqual(type(ast[3]), Operator)
        self.assertEqual(ast[3].name, '++')

    def test__Variable_AND_StringType0__Valid(self):
        example = "k && 'My String'"
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '&&')
        self.assertEqual(type(ast[2]), String)
        self.assertEqual(ast[2].name, 'My String')

    def test__Variable_AND_StringType1__Valid(self):
        example = 'k && "My String"'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '&&')
        self.assertEqual(type(ast[2]), String)
        self.assertEqual(ast[2].name, 'My String')

    def test__StringType0_AND_Variable__Valid(self):
        example = "'My String' && l"
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), String)
        self.assertEqual(ast[0].name, 'My String')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '&&')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'l')

    def test__StringType1_AND_Variable__Valid(self):
        example = '"My String" && l'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), String)
        self.assertEqual(ast[0].name, 'My String')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '&&')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'l')

    def test__Variable_AND_Variable__Valid(self):
        example = 'k && l'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '&&')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'l')

    def test__Variable_AND_Value__Valid(self):
        example = 'k && 2'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '&&')
        self.assertEqual(type(ast[2]), Value)
        self.assertEqual(ast[2].value, '2')

    def test__Value_AND_Variable__Valid(self):
        example = '2 && k'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Value)
        self.assertEqual(ast[0].value, '2')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '&&')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'k')

    def test__VariableIndexer_AND_Variable__Valid(self):
        example = 'k[1] && l'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Indexer)
        self.assertEqual(type(ast[0].attribute), Attribute)
        self.assertEqual(ast[0].attribute.name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '&&')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'l')

    def test__VariableComplexIndexer_AND_Variable__Valid(self):
        example = 'k[arr[1]] && l'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Indexer)
        self.assertEqual(type(ast[0].attribute), Attribute)
        self.assertEqual(ast[0].attribute.name, 'k')
        self.assertEqual(type(ast[0].expression), Indexer)
        self.assertEqual(type(ast[0].expression.attribute), Attribute)
        self.assertEqual(ast[0].expression.attribute.name, 'arr')
        self.assertEqual(type(ast[0].expression.expression), Value)
        self.assertEqual(ast[0].expression.expression.value, '1')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '&&')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'l')

    def test__VariableComplexIndexer_AND_Variable__Invalid(self):
        example = 'k[{arr[1]}] && l'
        with self.assertRaises(ValidationError) as context:
            parser = ExpressionParser(example)

    def test_Variable_AND_VariableIndexer__Valid(self):
        example = 'k && l[1]'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '&&')
        self.assertEqual(type(ast[2]), Indexer)
        self.assertEqual(type(ast[2].attribute), Attribute)
        self.assertEqual(ast[2].attribute.name, 'l')

    def test_Variable_AND_VariableComplex0Indexer__Valid(self):
        example = 'k && l[getIndex()]'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '&&')
        self.assertEqual(type(ast[2]), Indexer)
        self.assertEqual(type(ast[2].attribute), Attribute)
        self.assertEqual(ast[2].attribute.name, 'l')
        self.assertEqual(type(ast[2].expression), FunctionCall)
        self.assertEqual(ast[2].expression.name, 'getIndex')
        self.assertEqual(len(ast[2].expression.args), 0)

    def test_Variable_AND_VariableComplex1Indexer__Valid(self):
        example = 'k && l[getIndex() { return 1; }]'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '&&')
        self.assertEqual(type(ast[2]), Indexer)
        self.assertEqual(type(ast[2].attribute), Attribute)
        self.assertEqual(ast[2].attribute.name, 'l')
        self.assertEqual(type(ast[2].expression), Function)
        self.assertEqual(ast[2].expression.name, 'getIndex')
        self.assertEqual(len(ast[2].expression.params), 0)

    def test_Variable_AND_VariableIndexer__Invalid(self):
        example = 'k && l[{1}]'
        with self.assertRaises(ValidationError) as context:
            parser = ExpressionParser(example)

    def test__Variable_OR_Variable__Valid(self):
        example = 'k || l'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '||')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'l')

    def test__VariableIndexer_OR_Variable__Valid(self):
        example = 'k[1] || l'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Indexer)
        self.assertEqual(type(ast[0].attribute), Attribute)
        self.assertEqual(ast[0].attribute.name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '||')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'l')

    def test__Variable_OR_VariableIndexer__Valid(self):
        example = 'k || l[1]'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '||')
        self.assertEqual(type(ast[2]), Indexer)
        self.assertEqual(type(ast[2].attribute), Attribute)
        self.assertEqual(ast[2].attribute.name, 'l')

    def test__Variable_EQUAL_Variable__Valid(self):
        example = 'k == l'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'l')

    def test__Variable_NOT_EQUAL_Variable__Valid(self):
        example = 'k != l'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '!=')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'l')

    def test__Variable_EQUAL_TYPES_Variable__Valid(self):
        example = 'k === l'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '===')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'l')

    def test__Variable_NOT_EQUAL_TYPES_Variable__Valid(self):
        example = 'k !== l'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '!==')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'l')

    def test__Variable_EQUAL_VariableIndexer__Invalid(self):
        example = 'k == l[]'
        with self.assertRaises(ValidationError) as context:
            parser = ExpressionParser(example)

    def test__VariableIndexer_EQUAL_Variable__Invalid(self):
        example = 'k[] == l'
        with self.assertRaises(ValidationError) as context:
            parser = ExpressionParser(example)

    def test__Variable_EQUAL_ActionVoid__Valid(self):
        example = 'k == isAction()'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), FunctionCall)
        self.assertEqual(ast[2].name, 'isAction')
        self.assertEqual(ast[2].args, [])

    def test_Variable_EQUAL_ActionArg0Arg1__Valid(self):
        example = 'k == isAction(arg0, arg1)'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), FunctionCall)
        self.assertEqual(ast[2].name, 'isAction')
        self.assertEqual(len(ast[2].args), 2)
        self.assertEqual(type(ast[2].args[0]), Attribute)
        self.assertEqual(ast[2].args[0].name, 'arg0')
        self.assertEqual(type(ast[2].args[1]), Attribute)
        self.assertEqual(ast[2].args[1].name, 'arg1')

    def test_Variable_EQUAL_ObjectActionArg0Arg1__Valid(self):
        example = 'k == name.isAction(arg0, arg1)'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), FunctionCall)
        self.assertEqual(ast[2].name, 'isAction')
        self.assertEqual(type(ast[2].object), Object)
        self.assertEqual(ast[2].object.name, 'name')
        self.assertEqual(len(ast[2].args), 2)
        self.assertEqual(type(ast[2].args[0]), Attribute)
        self.assertEqual(ast[2].args[0].name, 'arg0')
        self.assertEqual(type(ast[2].args[1]), Attribute)
        self.assertEqual(ast[2].args[1].name, 'arg1')

    def test_Variable_EQUAL_NamespaceActionArg0Arg1__Valid(self):
        example = 'k == MyNamespace::isAction(arg0, arg1)'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), FunctionCall)
        self.assertEqual(ast[2].name, 'MyNamespace::isAction')
        self.assertEqual(len(ast[2].args), 2)
        self.assertEqual(type(ast[2].args[0]), Attribute)
        self.assertEqual(ast[2].args[0].name, 'arg0')
        self.assertEqual(type(ast[2].args[1]), Attribute)
        self.assertEqual(ast[2].args[1].name, 'arg1')

    def test_Variable_EQUAL_NamespaceActionArgExpression0Arg1__Valid(self):
        example = 'k == MyNameSpace::isAction(arg0 == 1, arg1)'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), FunctionCall)
        self.assertEqual(ast[2].name, 'MyNameSpace::isAction')
        self.assertEqual(len(ast[2].args), 2)
        self.assertEqual(type(ast[2].args[0]), Expression)
        self.assertEqual(len(ast[2].args[0]), 3)
        self.assertEqual(type(ast[2].args[0][0]), Attribute)
        self.assertEqual(ast[2].args[0][0].name, 'arg0')
        self.assertEqual(type(ast[2].args[0][1]), Operator)
        self.assertEqual(ast[2].args[0][1].name, '==')
        self.assertEqual(type(ast[2].args[0][2]), Value)
        self.assertEqual(ast[2].args[0][2].value, '1')
        self.assertEqual(type(ast[2].args[1]), Attribute)
        self.assertEqual(ast[2].args[1].name, 'arg1')

    def test_Variable_EQUAL_NamespaceActionArgExpression1Arg1__Valid(self):
        example = 'k == MyNameSpace::isAction(1 == arg0, arg1)'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), FunctionCall)
        self.assertEqual(ast[2].name, 'MyNameSpace::isAction')
        self.assertEqual(len(ast[2].args), 2)
        self.assertEqual(type(ast[2].args[0]), Expression)
        self.assertEqual(len(ast[2].args[0]), 3)
        self.assertEqual(type(ast[2].args[0][0]), Value)
        self.assertEqual(ast[2].args[0][0].value, '1')
        self.assertEqual(type(ast[2].args[0][1]), Operator)
        self.assertEqual(ast[2].args[0][1].name, '==')
        self.assertEqual(type(ast[2].args[0][2]), Attribute)
        self.assertEqual(ast[2].args[0][2].name, 'arg0')
        self.assertEqual(type(ast[2].args[1]), Attribute)
        self.assertEqual(ast[2].args[1].name, 'arg1')

    def test_Variable_EQUAL_NamespaceActionArgExpression2Arg1__Valid(self):
        example = 'k == MyNameSpace::isAction(arg0 = k, arg1)'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), FunctionCall)
        self.assertEqual(ast[2].name, 'MyNameSpace::isAction')
        self.assertEqual(len(ast[2].args), 2)
        self.assertEqual(type(ast[2].args[0]), Expression)
        self.assertEqual(len(ast[2].args[0]), 3)
        self.assertEqual(type(ast[2].args[0][0]), Attribute)
        self.assertEqual(ast[2].args[0][0].name, 'arg0')
        self.assertEqual(type(ast[2].args[0][1]), Operator)
        self.assertEqual(ast[2].args[0][1].name, '=')
        self.assertEqual(type(ast[2].args[0][2]), Attribute)
        self.assertEqual(ast[2].args[0][2].name, 'k')
        self.assertEqual(type(ast[2].args[1]), Attribute)
        self.assertEqual(ast[2].args[1].name, 'arg1')

    def test_Variable_EQUAL_ActionArg0Arg1Body__Valid(self):
        example = 'k == isAction(arg0, arg1) { arg0 = arg1; }'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Function)
        self.assertEqual(ast[2].name, 'isAction')
        self.assertEqual(len(ast[2].params), 2)
        self.assertEqual(type(ast[2].params[0]), Attribute)
        self.assertEqual(ast[2].params[0].name, 'arg0')
        self.assertEqual(type(ast[2].params[1]), Attribute)
        self.assertEqual(ast[2].params[1].name, 'arg1')
        self.assertEqual(ast[2].body, ' arg0 = arg1; ')

    def test_Variable_EQUAL_AnonymousActionArg0Arg1Body__Valid(self):
        example = 'k == (arg0, arg1) { arg0 = arg1; }'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Lambda)
        self.assertEqual(ast[2].name, None)
        self.assertEqual(len(ast[2].params), 2)
        self.assertEqual(type(ast[2].params[0]), Attribute)
        self.assertEqual(ast[2].params[0].name, 'arg0')
        self.assertEqual(type(ast[2].params[1]), Attribute)
        self.assertEqual(ast[2].params[1].name, 'arg1')
        self.assertEqual(ast[2].body, ' arg0 = arg1; ')

    def test_Variable_EQUAL_AnonymousActionArg0Arg1Body__ReturnAuto__Valid(self):
        example = 'k == (arg0, arg1) -> { arg0 = arg1; }'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Lambda)
        self.assertEqual(ast[2].name, None)
        self.assertEqual(len(ast[2].params), 2)
        self.assertEqual(type(ast[2].params[0]), Attribute)
        self.assertEqual(ast[2].params[0].name, 'arg0')
        self.assertEqual(type(ast[2].params[1]), Attribute)
        self.assertEqual(ast[2].params[1].name, 'arg1')
        self.assertEqual(ast[2].body, ' arg0 = arg1; ')

    def test__AnonymousActionArg0Arg1Body__ReturnAuto__EQUAL__Variable__Valid(self):
        example = '(arg0, arg1) -> { arg0 = arg1; } == k'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Lambda)
        self.assertEqual(ast[0].name, None)
        self.assertEqual(len(ast[0].params), 2)
        self.assertEqual(type(ast[0].params[0]), Attribute)
        self.assertEqual(ast[0].params[0].name, 'arg0')
        self.assertEqual(type(ast[0].params[1]), Attribute)
        self.assertEqual(ast[0].params[1].name, 'arg1')
        self.assertEqual(ast[0].body, ' arg0 = arg1; ')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'k')

    def test_Variable_EQUAL_AnonymousActionArg0Arg1Body__ReturnBool__Valid(self):
        example = 'k == (arg0, arg1) -> bool { arg0 = arg1; }'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Lambda)
        self.assertEqual(ast[2].name, None)
        self.assertEqual(len(ast[2].params), 2)
        self.assertEqual(type(ast[2].params[0]), Attribute)
        self.assertEqual(ast[2].params[0].name, 'arg0')
        self.assertEqual(type(ast[2].params[1]), Attribute)
        self.assertEqual(ast[2].params[1].name, 'arg1')
        self.assertEqual(ast[2].return_value, 'bool')
        self.assertEqual(ast[2].body, ' arg0 = arg1; ')

    def test__AnonymousActionArg0Arg1Body__ReturnBool__EQUAL__Variable__Valid(self):
        example = '(arg0, arg1) -> bool { arg0 = arg1; } == k'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Lambda)
        self.assertEqual(ast[0].name, None)
        self.assertEqual(len(ast[0].params), 2)
        self.assertEqual(type(ast[0].params[0]), Attribute)
        self.assertEqual(ast[0].params[0].name, 'arg0')
        self.assertEqual(type(ast[0].params[1]), Attribute)
        self.assertEqual(ast[0].params[1].name, 'arg1')
        self.assertEqual(ast[0].body, ' arg0 = arg1; ')
        self.assertEqual(ast[0].return_value, 'bool')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'k')

    def test_Variable_EQUAL_AnonymousActionArg0Arg1Body__ReturnStdString__Valid(self):
        example = 'k == (arg0, arg1) -> std::string { arg0 = arg1; }'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Lambda)
        self.assertEqual(ast[2].name, None)
        self.assertEqual(len(ast[2].params), 2)
        self.assertEqual(type(ast[2].params[0]), Attribute)
        self.assertEqual(ast[2].params[0].name, 'arg0')
        self.assertEqual(type(ast[2].params[1]), Attribute)
        self.assertEqual(ast[2].params[1].name, 'arg1')
        self.assertEqual(ast[2].return_value, 'std::string')
        self.assertEqual(ast[2].body, ' arg0 = arg1; ')

    def test__AnonymousActionArg0Arg1Body__ReturnStdString__EQUAL__Variable__Valid(self):
        example = '(arg0, arg1) -> std::string { arg0 = arg1; } == k'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Lambda)
        self.assertEqual(ast[0].name, None)
        self.assertEqual(len(ast[0].params), 2)
        self.assertEqual(type(ast[0].params[0]), Attribute)
        self.assertEqual(ast[0].params[0].name, 'arg0')
        self.assertEqual(type(ast[0].params[1]), Attribute)
        self.assertEqual(ast[0].params[1].name, 'arg1')
        self.assertEqual(ast[0].body, ' arg0 = arg1; ')
        self.assertEqual(ast[0].return_value, 'std::string')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'k')

    def test_Variable_EQUAL_ActionArg0Arg1Body_DoubleBraces__Valid(self):
        example = 'k == isAction(arg0, arg1) { { arg0 = arg1; } }'
        parser = ExpressionParser(example)

    def test_Variable_EQUAL_ActionArg0Arg1Body__ReturnAuto__Valid(self):
        example = 'k == isAction(arg0, arg1) -> { arg0 = arg1; return arg0; }'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Function)
        self.assertEqual(ast[2].name, 'isAction')
        self.assertEqual(len(ast[2].params), 2)
        self.assertEqual(type(ast[2].params[0]), Attribute)
        self.assertEqual(ast[2].params[0].name, 'arg0')
        self.assertEqual(type(ast[2].params[1]), Attribute)
        self.assertEqual(ast[2].params[1].name, 'arg1')
        self.assertEqual(ast[2].body, ' arg0 = arg1; return arg0; ')

    def test_Variable_EQUAL_ActionArg0Arg1Body_ReturnValue__Valid(self):
        example = 'k == isAction(arg0, arg1) -> bool { arg0 = arg1; return arg0; }'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Function)
        self.assertEqual(ast[2].name, 'isAction')
        self.assertEqual(len(ast[2].params), 2)
        self.assertEqual(type(ast[2].params[0]), Attribute)
        self.assertEqual(ast[2].params[0].name, 'arg0')
        self.assertEqual(type(ast[2].params[1]), Attribute)
        self.assertEqual(ast[2].params[1].name, 'arg1')
        self.assertEqual(ast[2].return_value, 'bool')
        self.assertEqual(ast[2].body, ' arg0 = arg1; return arg0; ')

    def test_Variable_EQUAL_ActionArg0Arg1Body_ReturnStdString__Valid(self):
        example = 'k == isAction(arg0, arg1) -> std::string { arg0 = arg1; return arg0; }'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Function)
        self.assertEqual(ast[2].name, 'isAction')
        self.assertEqual(len(ast[2].params), 2)
        self.assertEqual(type(ast[2].params[0]), Attribute)
        self.assertEqual(ast[2].params[0].name, 'arg0')
        self.assertEqual(type(ast[2].params[1]), Attribute)
        self.assertEqual(ast[2].params[1].name, 'arg1')
        self.assertEqual(ast[2].return_value, 'std::string')
        self.assertEqual(ast[2].body, ' arg0 = arg1; return arg0; ')

    def test_Variable_EQUAL_ActionArgExpressionArg1__Valid(self):
        example = 'k == isAction(arg0 == arg2, arg1)'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Attribute)
        self.assertEqual(ast[0].name, 'k')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), FunctionCall)
        self.assertEqual(ast[2].name, 'isAction')
        self.assertEqual(len(ast[2].args), 2)
        self.assertEqual(type(ast[2].args[0]), Expression)
        self.assertEqual(len(ast[2].args[0]), 3)
        self.assertEqual(type(ast[2].args[0][0]), Attribute)
        self.assertEqual(ast[2].args[0][0].name, 'arg0')
        self.assertEqual(type(ast[2].args[0][1]), Operator)
        self.assertEqual(ast[2].args[0][1].name, '==')
        self.assertEqual(type(ast[2].args[0][2]), Attribute)
        self.assertEqual(ast[2].args[0][2].name, 'arg2')
        self.assertEqual(type(ast[2].args[1]), Attribute)
        self.assertEqual(ast[2].args[1].name, 'arg1')

    def test__ActionArg0Arg1_EQUAL_Variable__Valid(self):
        example = 'isAction(arg0, arg1) == k'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), FunctionCall)
        self.assertEqual(ast[0].name, 'isAction')
        self.assertEqual(len(ast[0].args), 2)
        self.assertEqual(type(ast[0].args[0]), Attribute)
        self.assertEqual(ast[0].args[0].name, 'arg0')
        self.assertEqual(type(ast[0].args[1]), Attribute)
        self.assertEqual(ast[0].args[1].name, 'arg1')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'k')

    def test__ObjectActionArg0Arg1_EQUAL_Variable__Valid(self):
        example = 'name.isAction(arg0, arg1) == k'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), FunctionCall)
        self.assertEqual(ast[0].name, 'isAction')
        self.assertEqual(type(ast[0].object), Object)
        self.assertEqual(ast[0].object.name, 'name')
        self.assertEqual(len(ast[0].args), 2)
        self.assertEqual(type(ast[0].args[0]), Attribute)
        self.assertEqual(ast[0].args[0].name, 'arg0')
        self.assertEqual(type(ast[0].args[1]), Attribute)
        self.assertEqual(ast[0].args[1].name, 'arg1')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'k')

    def test__NamespaceActionArg0Arg1_EQUAL_Variable__Valid(self):
        example = 'MyNamespace::isAction(arg0, arg1) == k'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), FunctionCall)
        self.assertEqual(ast[0].name, 'MyNamespace::isAction')
        self.assertEqual(len(ast[0].args), 2)
        self.assertEqual(type(ast[0].args[0]), Attribute)
        self.assertEqual(ast[0].args[0].name, 'arg0')
        self.assertEqual(type(ast[0].args[1]), Attribute)
        self.assertEqual(ast[0].args[1].name, 'arg1')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'k')

    def test__NamespaceActionArgExpression0Arg1_EQUAL_Variable__Valid(self):
        example = 'MyNamespace::isAction(arg0 == 1, arg1) == k'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), FunctionCall)
        self.assertEqual(ast[0].name, 'MyNamespace::isAction')
        self.assertEqual(len(ast[0].args), 2)
        self.assertEqual(type(ast[0].args[0]), Expression)
        self.assertEqual(len(ast[0].args[0]), 3)
        self.assertEqual(type(ast[0].args[0][0]), Attribute)
        self.assertEqual(ast[0].args[0][0].name, 'arg0')
        self.assertEqual(type(ast[0].args[0][1]), Operator)
        self.assertEqual(ast[0].args[0][1].name, '==')
        self.assertEqual(type(ast[0].args[0][2]), Value)
        self.assertEqual(ast[0].args[0][2].value, '1')
        self.assertEqual(type(ast[0].args[1]), Attribute)
        self.assertEqual(ast[0].args[1].name, 'arg1')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'k')

    def test__NamespaceActionArgExpression1Arg1_EQUAL_Variable__Valid(self):
        example = 'MyNamespace::isAction(1 == arg0, arg1) == k'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), FunctionCall)
        self.assertEqual(ast[0].name, 'MyNamespace::isAction')
        self.assertEqual(len(ast[0].args), 2)
        self.assertEqual(type(ast[0].args[0]), Expression)
        self.assertEqual(len(ast[0].args[0]), 3)
        self.assertEqual(type(ast[0].args[0][0]), Value)
        self.assertEqual(ast[0].args[0][0].value, '1')
        self.assertEqual(type(ast[0].args[0][1]), Operator)
        self.assertEqual(ast[0].args[0][1].name, '==')
        self.assertEqual(type(ast[0].args[0][2]), Attribute)
        self.assertEqual(ast[0].args[0][2].name, 'arg0')
        self.assertEqual(type(ast[0].args[1]), Attribute)
        self.assertEqual(ast[0].args[1].name, 'arg1')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'k')

    def test__ActionArg0Arg1Body_EQUAL_Variable__Valid(self):
        example = 'isAction(arg0, arg1) { arg0 = arg1; } == k'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), Function)
        self.assertEqual(ast[0].name, 'isAction')
        self.assertEqual(len(ast[0].params), 2)
        self.assertEqual(type(ast[0].params[0]), Attribute)
        self.assertEqual(ast[0].params[0].name, 'arg0')
        self.assertEqual(type(ast[0].params[1]), Attribute)
        self.assertEqual(ast[0].params[1].name, 'arg1')
        self.assertEqual(ast[0].body, ' arg0 = arg1; ')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'k')

    def test__ActionArgExpressionArg1_EQUAL_Variable__Valid(self):
        example = 'isAction(arg0 == arg2, arg1) == k'
        parser = ExpressionParser(example)
        ast = parser.get_ast()
        self.assertEqual(len(ast), 3)
        self.assertEqual(type(ast[0]), FunctionCall)
        self.assertEqual(ast[0].name, 'isAction')
        self.assertEqual(len(ast[0].args), 2)
        self.assertEqual(len(ast[0].args[0]), 3)
        self.assertEqual(type(ast[0].args[0][0]), Attribute)
        self.assertEqual(ast[0].args[0][0].name, 'arg0')
        self.assertEqual(type(ast[0].args[0][1]), Operator)
        self.assertEqual(ast[0].args[0][1].name, '==')
        self.assertEqual(type(ast[0].args[0][2]), Attribute)
        self.assertEqual(ast[0].args[0][2].name, 'arg2')
        self.assertEqual(type(ast[0].args[1]), Attribute)
        self.assertEqual(ast[0].args[1].name, 'arg1')
        self.assertEqual(type(ast[1]), Operator)
        self.assertEqual(ast[1].name, '==')
        self.assertEqual(type(ast[2]), Attribute)
        self.assertEqual(ast[2].name, 'k')
