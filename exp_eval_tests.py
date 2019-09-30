# Start of unittest - add to completely test functions in exp_eval

import unittest
from exp_eval import *



class test_expressions(unittest.TestCase):
#
#POSTFIX EVALUATION ----------------------------------------------------------------
#
    def test_postfix_eval(self):
        self.assertAlmostEqual(postfix_eval("3 5 +"), 8)
        self.assertEqual(postfix_eval('4 8 + 6 5 - * 3 2 - 2 2 + * /'), 3.0)
        self.assertEqual(postfix_eval('5 1 2 + 4 ** + 3 -'), 83)
        self.assertAlmostEqual(postfix_eval('2.2 2 3 ** **'), 548.75873536)

    def test_postfix_eval_floats(self):
        self.assertAlmostEqual(postfix_eval('2.3 3.4 +'), 5.7)

    def test_postfix_eval_negatives(self):
        self.assertAlmostEqual(postfix_eval('-5 3.2 -'), -8.2)
        self.assertAlmostEqual(postfix_eval('-3 -2 **'), 0.111111111)
        self.assertAlmostEqual(postfix_eval('-5 -3.2 -'), -1.8)

    def test_postfix_eval_invalid_token(self):
        try:
            postfix_eval("blah")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Invalid token")

        try:
            postfix_eval('1.2.2 3.5 +')
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), 'Invalid token')

        try:
            postfix_eval('-2.4-4 5 +')
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), 'Invalid token')

        try:
            postfix_eval("3 52.0 -+")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Invalid token")

    def test_postfix_eval_insufficient_operands(self):
        try:
            postfix_eval("4 +")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")

        try:
            postfix_eval('4 -')
        except PostfixFormatException as e:
            self.assertEqual(str(e), 'Insufficient operands')

        try:
            postfix_eval('4 *')
        except PostfixFormatException as e:
            self.assertEqual(str(e), 'Insufficient operands')

        try:
            postfix_eval('4 **')
        except PostfixFormatException as e:
            self.assertEqual(str(e), 'Insufficient operands')

        try:
            postfix_eval('4 /')
        except PostfixFormatException as e:
            self.assertEqual(str(e), 'Insufficient operands')


    def test_postfix_eval_too_many_operands(self):
        try:
            postfix_eval("1 2 3 +")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Too many operands")

    def test_postfix_eval_value_error(self):
        with self.assertRaises(ValueError):
            postfix_eval('1 2 + 0 /')

    def test_postfix_eval_bitshifts(self):
        self.assertEqual(postfix_eval('120 2 <<'), 480)
        self.assertEqual(postfix_eval('0 6 <<'), 0)
        self.assertEqual(postfix_eval('15 10 >>'), 0)
        self.assertEqual(postfix_eval('60 2 >>'), 15)

    def test_postfix_eval_bitshifts_exceptions(self):
        try:
            postfix_eval('4 3 / 5 <<')
        except PostfixFormatException as e:
            self.assertEqual(str(e), 'Illegal bit shift operand')

        try:
            postfix_eval('4 3 / 5 >>')
        except PostfixFormatException as e:
            self.assertEqual(str(e), 'Illegal bit shift operand')

    def test_postfix_eval_15(self):
        with self.assertRaises(ValueError):
            postfix_eval("2.3 0 /")

#
#INFIX TO POSTFIX ----------------------------------------------------------------
#

    def test_infix_to_postfix_basic_operations(self):
        self.assertEqual(infix_to_postfix("7 - 2"), "7 2 -")
        self.assertEqual(infix_to_postfix('7 + 2'), '7 2 +')
        self.assertEqual(infix_to_postfix('7 * 2'), '7 2 *')
        self.assertEqual(infix_to_postfix('7 / 2'), '7 2 /')
        self.assertEqual(infix_to_postfix('7 ** 2'), '7 2 **')
        self.assertEqual(infix_to_postfix('7 >> 2'), '7 2 >>')
        self.assertEqual(infix_to_postfix('7 << 2'), '7 2 <<')

    def test_infix_to_postfix_single_digit(self):
        self.assertEqual(infix_to_postfix("19"), "19")

    def test_infix_to_postfix_floats(self):
        self.assertEqual(infix_to_postfix('( 7.2 + 3.54 ) * 11'),'7.2 3.54 + 11 *')

    def test_infix_to_postfix_negatives(self):
        self.assertEqual(infix_to_postfix('( -7 + 3 ) * -54'), '-7 3 + -54 *')
        self.assertEqual(infix_to_postfix('( -8.4 + -9 ) / 7'), '-8.4 -9 + 7 /')

    def test_infix_to_post_fix_exponent(self):

        self.assertEqual(infix_to_postfix('3 + 4 * 2 / ( 1 - 5 ) ** 2 ** 3'), '3 4 2 * 1 5 - 2 3 ** ** / +')
        self.assertEqual(infix_to_postfix('3 + 5 6 / 3 ** 2'), '3 5 6 3 2 ** / +')
        self.assertEqual(infix_to_postfix('3 - 5 6 / 3 ** 2'), '3 5 6 3 2 ** / -')
    
    def test_infix_to_postfix_extra(self):
        self.assertEqual(infix_to_postfix('3 >> 5'), '3 5 >>')
        self.assertEqual(infix_to_postfix('( 3 + 4 ) >> 10'), '3 4 + 10 >>')
        self.assertEqual(infix_to_postfix(' 3 << 4 >> 6'), '3 4 << 6 >>')
        self.assertEqual(infix_to_postfix("245.3 >> 6 ** 8.0 ** 24 / 24 ** 24"), "245.3 6 >> 8.0 24 ** ** 24 24 ** /") 
#
#PREFIX TO POSTFIX ----------------------------------------------------------------
#

    def test_prefix_to_postfix(self):
        self.assertEqual(prefix_to_postfix('* - 24 / 2 1 - / 4 5 6'), '24 2 1 / - 4 5 / 6 - *')
        self.assertEqual(prefix_to_postfix('* - 5 / 4 2 - / 7 8 9'), '5 4 2 / - 7 8 / 9 - *')
        self.assertEqual(prefix_to_postfix('+ 5 - 3 17'), '5 3 17 - +')
        self.assertEqual(prefix_to_postfix("+ + * 24 -7.8 12.0 5"), "24 -7.8 * 12.0 + 5 +")

    def test_prefix_to_postfix_single_digit(self):
        self.assertEqual(prefix_to_postfix('25'),'25')

    def test_prefix_to_postfix_exponent(self):
        self.assertEqual(prefix_to_postfix('** 10 -2.2'),'10 -2.2 **')

    def test_prefix_to_postfix_float(self):
        self.assertEqual(prefix_to_postfix("+ + + 5.7 7.1 11 3"), "5.7 7.1 + 11 + 3 +")

    def test_prefix_to_postfix_negative(self):
        self.assertEqual(prefix_to_postfix("+ + + -5.7 -6 11 3"), "-5.7 -6 + 11 + 3 +")

    def test_prefix_to_postfix_bitshift(self):
        self.assertEqual(prefix_to_postfix("- << 10 2 >> 3 4"),"10 2 << 3 4 >> -")

    def test_prefix_to_postfix_extra_space(self):
        self.assertEqual(prefix_to_postfix("** ** 8  9 10"),"8 9 ** 10 **")







if __name__ == "__main__":
    unittest.main()
