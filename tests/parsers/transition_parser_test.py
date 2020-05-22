import unittest

from fsm_tools.parsers.transition_parser import TransitionParser
from fsm_tools.exceptions import ValidationError


class TestingTransitionParser(unittest.TestCase):
    def setUp(self):
        """Currently nothing to do. Use it for initialization data before test"""
        pass

    def tearDown(self):
        """Currently nothing to do. Use it for reinitialization data after test"""
        pass

    def test__Event_ActionAction_Condition2__Valid(self):
        example = 'powerOn{} [ name.size() > default_name.size() ] / Action(), Action2()'
        parser = TransitionParser(example)
        events, condition, actions = parser.get_transition_items()
        self.assertEqual(events, 'powerOn{}')
        self.assertEqual(condition, 'name.size() > default_name.size()')
        self.assertEqual(actions, 'Action(), Action2()')

    def test__Event_ActionAction_Condition__Valid(self):
        example = 'EvConfig1() [ i > k ] / Action1() { [] }, Action2()'
        parser = TransitionParser(example)
        events, condition, actions = parser.get_transition_items()
        self.assertEqual(events, 'EvConfig1()')
        self.assertEqual(condition, 'i > k')
        self.assertEqual(actions, 'Action1() { [] }, Action2()')

    def test__Event_ActionPlusStringAction_Condition__Valid(self):
        example = 'EvConfig1() [ i > k ] / Action1() { [ "Hello Denis" ] }, Action2()'
        parser = TransitionParser(example)
        events, condition, actions = parser.get_transition_items()
        self.assertEqual(events, 'EvConfig1()')
        self.assertEqual(condition, 'i > k')
        self.assertEqual(actions, 'Action1() { [ "Hello Denis" ] }, Action2()')

    def test__Event_ActionPlusStringAction_Condition__Invalid0(self):
        example = 'EvConfig1() / Action1() { [ "Hello Denis ] }, Action2() [ i > k ]'
        with self.assertRaises(ValidationError) as context:
            parser = TransitionParser(example)

    def test__Event_ActionPlusStringAction_Condition__Invalid1(self):
        example = 'EvConfig1() / Action1() { [ Hello Denis" ] }, Action2() [ i > k ]'
        with self.assertRaises(ValidationError) as context:
            parser = TransitionParser(example)

    def test__Event_ActionPlusStringAction_Condition__Invalid2(self):
        example = "EvConfig1() / Action1() { [ 'Hello Denis ] }, Action2() [ i > k ]"
        with self.assertRaises(ValidationError) as context:
            parser = TransitionParser(example)

    def test__Event_ActionPlusStringAction_Condition__Invalid3(self):
        example = "EvConfig1() / Action1() { [ Hello Denis' ] }, Action2() [ i > k ]"
        with self.assertRaises(ValidationError) as context:
            parser = TransitionParser(example)

    def test__Event_NonActions_Condition__Valid(self):
        example = 'EvConfig1() [ i > k ]'
        parser = TransitionParser(example)
        events, condition, actions = parser.get_transition_items()
        self.assertEqual(events, 'EvConfig1()')
        self.assertEqual(condition, 'i > k')
        self.assertEqual(actions, '')

    def test__Event_NonActions_NonCondition__Valid(self):
        example = 'EvConfig1()'
        parser = TransitionParser(example)
        events, condition, actions = parser.get_transition_items()
        self.assertEqual(events, 'EvConfig1()')
        self.assertEqual(condition, '')
        self.assertEqual(actions, '')

    def test__EventNoBraces_NonActions_NonCondition__Valid(self):
        example = 'EvConfig1'
        parser = TransitionParser(example)
        events, condition, actions = parser.get_transition_items()
        self.assertEqual(events, 'EvConfig1')
        self.assertEqual(actions, '')
        self.assertEqual(condition, '')

    def test__EventArg_ActionAction_Condition__Valid(self):
        example = 'EvConfig1(1) [ i > k ] / Action1() { [] }, Action2()'
        parser = TransitionParser(example)
        events, condition, actions = parser.get_transition_items()
        self.assertEqual(events, 'EvConfig1(1)')
        self.assertEqual(condition, 'i > k')
        self.assertEqual(actions, 'Action1() { [] }, Action2()')

    def test__EventEvent_ActionAction_Condition__Valid(self):
        example = 'EvConfig1(), EvConfig2() [ i > k ] / Action1() { [] }, Action2()'
        parser = TransitionParser(example)
        events, condition, actions = parser.get_transition_items()
        self.assertEqual(events, 'EvConfig1(), EvConfig2()')
        self.assertEqual(condition, 'i > k')
        self.assertEqual(actions, 'Action1() { [] }, Action2()')

    def test__EventArgEventArg_ActionAction_Condition__Valid(self):
        example = 'EvConfig1(1), EvConfig2(2) [ i > k ] / Action1() { [] }, Action2()'
        parser = TransitionParser(example)
        events, condition, actions = parser.get_transition_items()
        self.assertEqual(events, 'EvConfig1(1), EvConfig2(2)')
        self.assertEqual(condition, 'i > k')
        self.assertEqual(actions, 'Action1() { [] }, Action2()')

    def test__EventArgEventArg_ActionArgAction_Condition__Valid(self):
        example = 'EvConfig1(1), EvConfig2(2) [ i > k ] / Action1(8) { [] }, Action2()'
        parser = TransitionParser(example)
        events, condition, actions = parser.get_transition_items()
        self.assertEqual(events, 'EvConfig1(1), EvConfig2(2)')
        self.assertEqual(condition, 'i > k')
        self.assertEqual(actions, 'Action1(8) { [] }, Action2()')

    def test__EventArgBodyEventArg_ActionAction_Condition__Valid(self):
        example = 'EvConfig1(1) { }, EvConfig2(2) [ i > k ] / Action1() { [] }, Action2()'
        parser = TransitionParser(example)
        events, condition, actions = parser.get_transition_items()
        self.assertEqual(events, 'EvConfig1(1) { }, EvConfig2(2)')
        self.assertEqual(condition, 'i > k')
        self.assertEqual(actions, 'Action1() { [] }, Action2()')

    def test__EventArgEventArgBody_ActionAction_Condition__Valid(self):
        example = 'EvConfig1(1), EvConfig2(2) { } [ i > k ] / Action1() { [] }, Action2()'
        parser = TransitionParser(example)
        events, condition, actions = parser.get_transition_items()
        self.assertEqual(events, 'EvConfig1(1), EvConfig2(2) { }')
        self.assertEqual(condition, 'i > k')
        self.assertEqual(actions, 'Action1() { [] }, Action2()')

    def test__EventArgEventArgBody_ActionAction__Valid(self):
        example = 'EvConfig1(1), EvConfig2(2) { } / Action1() { [] }, Action2()'
        parser = TransitionParser(example)
        events, conditions, actions = parser.get_transition_items()
        self.assertEqual(events, 'EvConfig1(1), EvConfig2(2) { }')
        self.assertEqual(conditions, '')
        self.assertEqual(actions, 'Action1() { [] }, Action2()')

    def test__EventArgEventArgBody_ActionAction_Condition__Invalid(self):
        example = 'EvConfig1(1), EvConfig2(2) { } [ i > k ] / Action1() { [] }, Action2() {'
        with self.assertRaises(ValidationError) as context:
            parser = TransitionParser(example)

    def test__EventArgBodyEventArgBody_ActionAction_Condition__Valid(self):
        example = 'EvConfig1(1) { }, EvConfig2(2) { } [ i > k ] / Action1() { [] }, Action2()'
        parser = TransitionParser(example)
        events, condition, actions = parser.get_transition_items()
        self.assertEqual(events, 'EvConfig1(1) { }, EvConfig2(2) { }')
        self.assertEqual(condition, 'i > k')
        self.assertEqual(actions, 'Action1() { [] }, Action2()')

    def test__EventArgBodyEventArgBody_ActionAction__Valid(self):
        example = 'EvConfig1(1) { }, EvConfig2(2) { } / Action1() { [] }, Action2()'
        parser = TransitionParser(example)
        events, conditions, actions = parser.get_transition_items()
        self.assertEqual(events, 'EvConfig1(1) { }, EvConfig2(2) { }')
        self.assertEqual(conditions, '')
        self.assertEqual(actions, 'Action1() { [] }, Action2()')

    def test__EventArgEventArg_ActionAction_Condition__Invalid0(self):
        example = 'EvConfig1(1), EvConfig2(2) [ i > k ] / Action1() {{ [] }, Action2()'
        with self.assertRaises(ValidationError) as context:
            parser = TransitionParser(example)

    def test__EventArgEventArg_ActionAction_Condition__Invalid1(self):
        example = 'EvConfig1(1), EvConfig2(2) [ i > k ] / Action1() { [] }}, Action2()'
        with self.assertRaises(ValidationError) as context:
            parser = TransitionParser(example)

    def test__EventArgEventArg_ActionAction_Condition__Invalid2(self):
        example = 'EvConfig1(1), EvConfig2(2) [ i > k ] / Action1() { [] }), Action2()'
        with self.assertRaises(ValidationError) as context:
            parser = TransitionParser(example)

    def test__EventArgEventArg_ActionAction_Condition__Invalid3(self):
        example = 'EvConfig1(1), EvConfig2(2) [ i > k ] / Action1() { [ }, Action2()'
        with self.assertRaises(ValidationError) as context:
            parser = TransitionParser(example)

    def test__Event_ActionAction_Condition__Invalid(self):
        example = 'EvConfig() [ i > k ]] / Action1() { [] }, Action2()'
        with self.assertRaises(ValidationError) as context:
            parser = TransitionParser(example)

