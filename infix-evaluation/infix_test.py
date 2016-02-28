# infix_test.py - Test cases for infix evaluator
#
# The MIT License (MIT)
# 
# Copyright (c) [2016] [Gaurav Mathur]
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import math
def __test(IE, expr, expected):
    #
    # PEP 0485 -- A Function for testing approximate equality
    #
    # A default relative tolerance of 1e-5 assures that the two values being
    # compared are within 5 decimal digits
    #
    def isclose(a, b, rel_tol=1e-05, abs_tol=0.0):
            return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    result = IE(expr)
    assert (isclose(result, expected)), expr+" [FAILED. Expected "+str(expected)+"]"
    print expr+" = "+ str(result) + " [OK]"

# 
# Test the Stack driven infix evaluator
#
def infix_stack_test():
    from infix_stack import InfixEvaluator

    try:
        IE = InfixEvaluator()
        expr = "2 + 3"
        __test(IE, expr, 5)
        expr = "2 + -3"
        __test(IE, expr, -1.0)
        expr = "2 + ( 3 * 5 )"
        __test(IE, expr, 17)
        expr = "( 2 + 3 ) * 5 )"
        __test(IE, expr, 25)
        expr = "( 2 + 3 ) * ( 5 + 7 )"
        __test(IE, expr, 60)
        expr = "( 1 * ( 2 * ( 3 * ( 4 + 5 ) ) ) )"
        __test(IE, expr, 54)
        expr = "( 1 * ( 2 * ( -3 * ( 4 + 5 ) ) ) )"
        __test(IE, expr, -54)
        expr = "9 / 7"
        __test(IE, expr, 1.28571)
        expr = "( 9 / 7 ) * 34"
        __test(IE, expr, 43.71428)
        expr = "10 - 5"
        __test(IE, expr, 5)
        expr = "-10 / -5"
        __test(IE, expr, 2)
        expr = "( 10 ) / ( 77 )"
        __test(IE, expr, 0.12987)
        expr = "567 * ( 55 - 10 ) / 45"
        __test(IE, expr, 567)
        expr = "( 567 * ( 55 - 10 ) ) / 45"
        __test(IE, expr, 567)
        expr = "5 * ( 6 + 2 ) - 12 / 4"
        __test(IE, expr, 37)

    except AssertionError as e:
        print e

if __name__ == "__main__":
    infix_stack_test()
    
