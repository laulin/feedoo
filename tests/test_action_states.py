from feedoo.action_states import ActionStates
from feedoo.event import Event
import unittest

class TestActionStates(unittest.TestCase):
    def test_1(self):
        state = ActionStates("my_action", None)

    def test_add_ok(self):
        state = ActionStates("my_action", None)
        event = Event("tag", 123456, {})
        result = state.add_in(event)
        expected = 1

        self.assertEqual(result, expected)

    def test_add_ko(self):
        state = ActionStates("my_action", None)
        event = Event("tag", 123456, {})

        with self.assertRaises(AttributeError):
            result = state.add_xxx(event)

    def test_get_states(self):
        state = ActionStates("my_action", None)
        event = Event("tag", 123456, {})
        state.add_in(event)
        result = state.get_states()
        expected = {'name':"my_action", 'repr':"None", 'in': {'tag': 1}, 'bypass': {}, 'do': {}, 'ignore': {}, 'out': {}}

        self.assertEqual(result, expected)