import unittest

from .helpers import register_test


@register_test("Challenge 1")
class TestDictionary(unittest.TestCase):

    def test_value(self):
        self.assertEquals(1, self.cell.output, "Make sure you return a value")