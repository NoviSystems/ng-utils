
import unittest
from itng.common.utils import import_class, choices, override_attr


class ImportClassTestCase(unittest.TestCase):
    def test_dot_notation(self):
        f = import_class('itng.common.utils.import_class')
        self.assertIs(f, import_class)

    def test_colon_notation(self):
        f = import_class('itng.common.utils:import_class')
        self.assertIs(f, import_class)


class ChoicesTestCase(unittest.TestCase):
    def test_attribute_access(self):
        opts = choices((
            ('a', 'A'),
            ('b', 'B'),
        ))

        self.assertTrue(hasattr(opts, 'A'))
        self.assertTrue(hasattr(opts, 'B'))
        self.assertEqual(opts.A, 'a')
        self.assertEqual(opts.B, 'b')
        self.assertEqual(opts[0], ('a', 'A'))
        self.assertEqual(opts[1], ('b', 'B'))

        # ensure we don't accidentally insert additional elements
        with self.assertRaises(IndexError):
            opts[2]


class OverrideAttrTestCase(unittest.TestCase):
    def test_variable_reset(self):
        class Foo(object):
            def __init__(self):
                self.bar = 'baz'
        f = Foo()

        self.assertEqual(f.bar, 'baz')

        with override_attr(f, 'bar', 'flub'):
            self.assertEqual(f.bar, 'flub')

        self.assertEqual(f.bar, 'baz')
