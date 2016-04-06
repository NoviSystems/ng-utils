
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

    def test_empty_choice(self):
        opts = choices((
            ('', 'N/A'),
            ('a', 'A'),
            ('b', 'B'),
        ))

        self.assertTrue(hasattr(opts, '__EMPTY__'))
        self.assertEqual(opts.keys(), ['', 'a', 'b'])
        self.assertEqual(opts.__EMPTY__, '')

    def test_snake_case(self):
        # dashes and whitespace => _
        opts = choices((
            ('a 1', 'A'),
            ('b-2', 'B'),
        ))
        self.assertTrue(hasattr(opts, 'A_1'))
        self.assertTrue(hasattr(opts, 'B_2'))

    def test_keys(self):
        opts = choices((
            ('a', 'A'),
            ('b', 'B'),
        ))

        self.assertEqual(opts.keys(), ['a', 'b'])

    def test_values(self):
        opts = choices((
            ('a', 'A'),
            ('b', 'B'),
        ))

        self.assertEqual(opts.values(), ['A', 'B'])

    def test_boolean_type(self):
        opts = choices((
            (True, 'A'),
            (False, 'B'),
        ))

        self.assertTrue(hasattr(opts, 'TRUE'))
        self.assertTrue(hasattr(opts, 'FALSE'))
        self.assertEqual(opts.TRUE, True)
        self.assertEqual(opts.FALSE, False)
        self.assertEqual(opts.keys(), [True, False])

    def test_integer_type(self):
        opts = choices((
            (1, 'A'),
            (2, 'B'),
        ))

        self.assertTrue(hasattr(opts, '_1'))
        self.assertTrue(hasattr(opts, '_2'))
        self.assertEqual(opts._1, 1)
        self.assertEqual(opts._2, 2)
        self.assertEqual(opts.keys(), [1, 2])


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
