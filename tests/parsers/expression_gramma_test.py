import unittest

from fsm_tools.parsers.expression_parser import lambda_declaration_regex, function_call_regex, \
    function_declaration_regex, function_declaration_expression, method_call_regex, method_declaration_regex, \
    object_construction_regex


class TestingExpressionParser(unittest.TestCase):
    def setUp(self):
        """Currently nothing to do. Use it for initialization data before test"""
        pass

    def tearDown(self):
        """Currently nothing to do. Use it for reinitialization data after test"""
        pass

    def test__ObjectConstruction0_Expression__Valid(self):
        example = "power{}"
        match = object_construction_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)

    def test__ObjectConstruction1_Expression__Valid(self):
        example = "power{arg0, arg1}"
        match = object_construction_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)

    def test__FunctionCall_Expression__Valid(self):
        example = "Action()"
        match = function_call_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)

    def test__FunctionDeclaration0_Expression__Valid(self):
        example = "Action() {}"
        print(f'function_declaration_expression is {function_declaration_expression}')
        match = function_declaration_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)

    def test__FunctionDeclaration1_Expression__Valid(self):
        example = "Action() -> {}"
        print(f'function_declaration_expression is {function_declaration_expression}')
        match = function_declaration_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)

    def test__FunctionDeclaration2_Expression__Valid(self):
        example = "Action() -> Int { }"
        print(f'function_declaration_expression is {function_declaration_expression}')
        match = function_declaration_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)

    def test__MethodCall0_Expression__Valid(self):
        example = "fsm.Action()"
        match = method_call_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)

    def test__MethodCall2_Expression__Valid(self):
        example = "fsm->Action()"
        match = method_call_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)

    def test__MethodDeclaration0_Expression__Valid(self):
        example = "fsm.Action() {}"
        match = method_declaration_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)

    def test__MethodDeclaration1_Expression__Valid(self):
        example = "fsm.Action() -> {}"
        match = method_declaration_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)

    def test__MethodDeclaration2_Expression__Valid(self):
        example = "fsm.Action() -> Int {}"
        match = method_declaration_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)

    def test__MethodDeclaration3_Expression__Invalid(self):
        example = "fsm.Action() ->"
        match = method_declaration_regex.match(example)
        self.assertFalse(match)

    def test__LambdaDeclaration0_Expression__Valid(self):
        example = "() {}"
        match = lambda_declaration_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)

    def test__LambdaDeclaration1_Expression__Valid(self):
        example = "() -> {}"
        match = lambda_declaration_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)

    def test__LambdaArg0Declaration0_Expression__Valid(self):
        example = "(arg0) {}"
        match = lambda_declaration_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)

    def test__LambdaArg0Declaration1_Expression__Valid(self):
        example = "(arg0) -> {}"
        match = lambda_declaration_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)

    def test__LambdaArg0Declaration2_Expression__Invalid(self):
        example = "(arg0) ->"
        match = lambda_declaration_regex.match(example)
        self.assertFalse(match)

    def test__LambdaArg0Arg1Declaration0_Expression__Valid(self):
        example = "(arg0, arg1) {}"
        match = lambda_declaration_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)

    def test__LambdaArg0Arg1Declaration_Expression__Valid(self):
        example = "(arg0, arg1) -> {}"
        match = lambda_declaration_regex.match(example)
        self.assertTrue(match)
        self.assertEqual(match.group(), example)
