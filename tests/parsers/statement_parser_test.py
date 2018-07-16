import unittest

from src.parsers.statement_parser import StatementParser
from src.exceptions import ValidationError


class TestingStatementParser(unittest.TestCase):
    def setUp(self):
        """Currently nothing to do. Use it for initialization data before test"""
        pass

    def tearDown(self):
        """Currently nothing to do. Use it for reinitialization data after test"""
        pass

    def test__Event_ActionAction_Condition__Valid(self):
        example = 'EvConfig1() / Action1() { [] }, Action2() [ i > k ]'
        parser = StatementParser(example)
        events, actions, conditions = parser.parse()
        self.assertEqual(events, 'EvConfig1()')
        self.assertEqual(actions, 'Action1() { [] }, Action2()')
        self.assertEqual(conditions, 'i > k')

    def test__Event_ActionPlusStringAction_Condition__Valid(self):
        example = 'EvConfig1() / Action1() { [ "Hello Denis" ] }, Action2() [ i > k ]'
        parser = StatementParser(example)
        events, actions, conditions = parser.parse()
        self.assertEqual(events, 'EvConfig1()')
        self.assertEqual(actions, 'Action1() { [ "Hello Denis" ] }, Action2()')
        self.assertEqual(conditions, 'i > k')

    def test__Event_ActionPlusStringAction_Condition__Invalid0(self):
        example = 'EvConfig1() / Action1() { [ "Hello Denis ] }, Action2() [ i > k ]'
        parser = StatementParser(example)
        with self.assertRaises(ValidationError) as context:
            parser.parse()

    def test__Event_ActionPlusStringAction_Condition__Invalid1(self):
        example = 'EvConfig1() / Action1() { [ Hello Denis" ] }, Action2() [ i > k ]'
        parser = StatementParser(example)
        with self.assertRaises(ValidationError) as context:
            parser.parse()

    def test__Event_ActionPlusStringAction_Condition__Invalid2(self):
        example = "EvConfig1() / Action1() { [ 'Hello Denis ] }, Action2() [ i > k ]"
        parser = StatementParser(example)
        with self.assertRaises(ValidationError) as context:
            parser.parse()

    def test__Event_ActionPlusStringAction_Condition__Invalid3(self):
        example = "EvConfig1() / Action1() { [ Hello Denis' ] }, Action2() [ i > k ]"
        parser = StatementParser(example)
        with self.assertRaises(ValidationError) as context:
            parser.parse()

    def test__Event_NonActions_Condition__Valid(self):
        example = 'EvConfig1() [ i > k ]'
        parser = StatementParser(example)
        events, actions, conditions = parser.parse()
        self.assertEqual(events, 'EvConfig1()')
        self.assertEqual(actions, '')
        self.assertEqual(conditions, 'i > k')

    def test__Event_NonActions_NonCondition__Valid(self):
        example = 'EvConfig1()'
        parser = StatementParser(example)
        events, actions, conditions = parser.parse()
        self.assertEqual(events, 'EvConfig1()')
        self.assertEqual(actions, '')
        self.assertEqual(conditions, '')

    def test__EventNoBraces_NonActions_NonCondition__Valid(self):
        example = 'EvConfig1'
        parser = StatementParser(example)
        events, actions, conditions = parser.parse()
        self.assertEqual(events, 'EvConfig1')
        self.assertEqual(actions, '')
        self.assertEqual(conditions, '')

    def test__EventArg_ActionAction_Condition__Valid(self):
        example = 'EvConfig1(1) / Action1() { [] }, Action2() [ i > k ]'
        parser = StatementParser(example)
        events, actions, conditions = parser.parse()
        self.assertEqual(events, 'EvConfig1(1)')
        self.assertEqual(actions, 'Action1() { [] }, Action2()')
        self.assertEqual(conditions, 'i > k')

    def test__EventEvent_ActionAction_Condition__Valid(self):
        example = 'EvConfig1(), EvConfig2() / Action1() { [] }, Action2() [ i > k ]'
        parser = StatementParser(example)
        events, actions, conditions = parser.parse()
        self.assertEqual(events, 'EvConfig1(), EvConfig2()')
        self.assertEqual(actions, 'Action1() { [] }, Action2()')
        self.assertEqual(conditions, 'i > k')

    def test__EventArgEventArg_ActionAction_Condition__Valid(self):
        example = 'EvConfig1(1), EvConfig2(2) / Action1() { [] }, Action2() [ i > k ]'
        parser = StatementParser(example)
        events, actions, conditions = parser.parse()
        self.assertEqual(events, 'EvConfig1(1), EvConfig2(2)')
        self.assertEqual(actions, 'Action1() { [] }, Action2()')
        self.assertEqual(conditions, 'i > k')

    def test__EventArgEventArg_ActionArgAction_Condition__Valid(self):
        example = 'EvConfig1(1), EvConfig2(2) / Action1(8) { [] }, Action2() [ i > k ]'
        parser = StatementParser(example)
        events, actions, conditions = parser.parse()
        self.assertEqual(events, 'EvConfig1(1), EvConfig2(2)')
        self.assertEqual(actions, 'Action1(8) { [] }, Action2()')
        self.assertEqual(conditions, 'i > k')

    def test__EventArgBodyEventArg_ActionAction_Condition__Valid(self):
        example = 'EvConfig1(1) { }, EvConfig2(2) / Action1() { [] }, Action2() [ i > k ]'
        parser = StatementParser(example)
        events, actions, conditions = parser.parse()
        self.assertEqual(events, 'EvConfig1(1) { }, EvConfig2(2)')
        self.assertEqual(actions, 'Action1() { [] }, Action2()')
        self.assertEqual(conditions, 'i > k')

    def test__EventArgEventArgBody_ActionAction_Condition__Valid(self):
        example = 'EvConfig1(1), EvConfig2(2) { } / Action1() { [] }, Action2() [ i > k ]'
        parser = StatementParser(example)
        events, actions, conditions = parser.parse()
        self.assertEqual(events, 'EvConfig1(1), EvConfig2(2) { }')
        self.assertEqual(actions, 'Action1() { [] }, Action2()')
        self.assertEqual(conditions, 'i > k')

    def test__EventArgEventArgBody_ActionAction_Condition__Invalid(self):
        example = 'EvConfig1(1), EvConfig2(2) { } / Action1() { [] }, Action2() { [ i > k ]'
        parser = StatementParser(example)
        with self.assertRaises(ValidationError) as context:
            parser.parse()

    def test__EventArgBodyEventArgBody_ActionAction_Condition__Valid(self):
        example = 'EvConfig1(1) { }, EvConfig2(2) { } / Action1() { [] }, Action2() [ i > k ]'
        parser = StatementParser(example)
        events, actions, conditions = parser.parse()
        self.assertEqual(events, 'EvConfig1(1) { }, EvConfig2(2) { }')
        self.assertEqual(actions, 'Action1() { [] }, Action2()')
        self.assertEqual(conditions, 'i > k')

    def test__EventArgEventArg_ActionAction_Condition__Invalid0(self):
        example = 'EvConfig1(1), EvConfig2(2) / Action1() {{ [] }, Action2() [ i > k ]'
        parser = StatementParser(example)
        with self.assertRaises(ValidationError) as context:
            parser.parse()

    def test__EventArgEventArg_ActionAction_Condition__Invalid1(self):
        example = 'EvConfig1(1), EvConfig2(2) / Action1() { [] }}, Action2() [ i > k ]'
        parser = StatementParser(example)
        with self.assertRaises(ValidationError) as context:
            parser.parse()

    def test__EventArgEventArg_ActionAction_Condition__Invalid2(self):
        example = 'EvConfig1(1), EvConfig2(2) / Action1() { [] }), Action2() [ i > k ]'
        parser = StatementParser(example)
        with self.assertRaises(ValidationError) as context:
            parser.parse()

    def test__EventArgEventArg_ActionAction_Condition__Invalid3(self):
        example = 'EvConfig1(1), EvConfig2(2) / Action1() { [ }, Action2() [ i > k ]'
        parser = StatementParser(example)
        with self.assertRaises(ValidationError) as context:
            parser.parse()

    def test__Event_ActionAction_Condition__Invalid(self):
        example = 'EvConfig() / Action1() { [] }, Action2() [ i > k ]]'
        parser = StatementParser(example)
        with self.assertRaises(ValidationError) as context:
            parser.parse()
