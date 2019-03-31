import unittest
from parser import Parser

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

    def test_op_with_init_comments(self):
        self.assertEqual(Parser.run("' bla \n 1+1"), 2)
    
    def test_op_with_mid_comments(self):
        self.assertEqual(Parser.run("2 + 3 * ' bla \n 5"), 17)

    def test_op_with_end_comments(self):
        with self.assertRaises(ValueError):
            Parser.run("2 + 3 * ' bla 5")

    def test_par_sum_mult(self):
        self.assertEqual(Parser.run("(3 + 2) /5"), 1)

    def test_unary_ops(self):
        self.assertEqual(Parser.run("+--++3"), 3)
    
    def test_unary_ops_with_div(self):
        self.assertEqual(Parser.run("3 - -2/4"), 4)

    def test_par_div_mult(self):
        self.assertEqual(Parser.run("4/(1+1)*2"), 4)

    def test_no_closing_par(self):
        with self.assertRaises(ValueError):
            Parser.run("(2*2")
    def test_lost_par(self):
        with self.assertRaises(ValueError):
            Parser.run("2*2)")

def main():
    unittest.main()

if __name__ == "__main__":
    main()