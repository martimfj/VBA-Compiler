import unittest
from main import Parser

__author__ = "Martim Ferreira José"
__version__ = "1.1.1"
__license__ = "MIT"

class TestCase(unittest.TestCase):
    def test_plus(self):
        self.assertEqual(Parser.run("1+2"), 3)

    def test_minus(self):
        self.assertEqual(Parser.run("3-2"), 1)

    def test_1digit_numbers(self):
        self.assertEqual(Parser.run("1+2-3"), 0)

    def test_2digit_numbers(self):
        self.assertEqual(Parser.run("11+22-33"), 0)

    def test_3digit_numbers_wspace(self):
        self.assertEqual(Parser.run("789  +345 -  123"), 1011)

    def test_comments_start(self):
        with self.assertRaises(ValueError):
            Parser.run("' bla 1 ' bla")

    def test_divide_first(self):
        self.assertEqual(Parser.run("4/2+3"), 5)

    def test_divide_last(self):
        self.assertEqual(Parser.run("3+4/2"), 5)

    def test_op_with_comments(self):
        with self.assertRaises(ValueError):
            Parser.run("2 + 3 * ' bla 5")

def main():
    unittest.main()

if __name__ == "__main__":
    main()