
import unittest
from itng.common.utils import import_class, override_attr


class ImportClassTestCase(unittest.TestCase):
    def test_dot_notation(self):
        f = import_class('itng.common.utils.import_class')
        self.assertIs(f, import_class)

    def test_colon_notation(self):
        f = import_class('itng.common.utils:import_class')
        self.assertIs(f, import_class)


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
