import unittest
from main import Parser

__author__ = "Martim Ferreira José"
__version__ = "1.0.1"
__license__ = "MIT"

class LearningCase(unittest.TestCase):
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

def main():
    unittest.main()

if __name__ == "__main__":
    main()