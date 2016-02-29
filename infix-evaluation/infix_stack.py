# infix_stack.py - A stack-based infix evaluator
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
# Features and Caveats
# --------------------
# 01. Supports the following operators - '*', '+', '-', '/'
# 02. Supports negative and positive integer and float numbers
# 03. The implementation evaluates the expression with the help of two stacks
# 04. The implementation does not define and implement a grammer for the 
#       arithmetic expression
#
# Usage: infix.py "<expression with operators and operands seperated by space>"
#
# Example:
#
#   >> python infix.py "2 + 3 * 5"
#   Result: 17.0
#   >> python infix.py "2 + (3 * 5)"
#   Invalid infix expression
#   >> python infix.py "2 + ( 3 * 5 )"
#   Result: 17.0
#   >> python infix.py "( 2 + 3 ) * 5"
#   Result: 25.0
#   >> python infix.py "( 2 + 3 ) * ( 5 + 2 )"
#   Result: 35.0
#   >> python infix.py "2 + 3 * 5 + 2"
#   Result: 19.0
#   >> python infix.py "-2 + 10.02"
#   Result: 8.02
#
#
import sys
import operator as optr
from sets import Set

#
# Stack defnition
#
class Stack:
    def __init__(self, max):
        self.max = max
        self.count = 0
        self.sl = []

    def push(self, ele):
        if (self.count == self.max):
            return "Overflow"
        self.sl.append(ele)
        self.count = self.count + 1
        return None

    def pop(self):
        if self.count == 0:
            return None
        self.count = self.count - 1
        return self.sl.pop()

    def peek(self):
        if self.count == 0:
            return None
        return self.sl[len(self.sl)-1]

    # Generator API to pop all elements on the stack
    def popall(self):
        while len(self.sl) > 0:
            obj = self.sl.pop()
            self.count = self.count - 1 
            yield obj

    def __str__(self):
        mstr = ""
        for obj in self.sl:
            mstr += str(obj)+" "
        return mstr

#
# Core Infix evaluation logic
#
class InfixEvaluator:
    # Operator precedence
    opprec = {
            '/':450, 
            '*':430, 
            '+':350, 
            '-':330
            }
    # All supported operators
    v_operators = Set(['+', '-', '*', '/'])
    # All supported operator operations
    v_operations = {
        '+':optr.add,
        '-':optr.sub,
        '*':optr.mul,
        '/':optr.div
        }
    # Supported parenthesis symbol
    v_parens = Set(['(', ')'])
    # Open parenthesis definition
    v_open_paren = '('
    # Close parenthesis definition
    v_close_paren = ')'

    def __init__(self):
        # Instance variable
        self.operators = Stack(1014)
        self.operands = Stack(1014)

    @staticmethod
    def is_operator(token):
        return token in InfixEvaluator.v_operators

    @staticmethod
    def is_operand(token):
        def is_int(token):
            try:
                int(token)
                return True
            except ValueError:
                return False

        def is_float(token):
            try:
                float(token)
                return True
            except ValueError:
                return False

        return is_int(token) or is_float(token) 

    @staticmethod
    def is_paren(token):
        return token in InfixEvaluator.v_parens

    @staticmethod
    def validate(tokens):
        for t in tokens:
            if not(InfixEvaluator.is_operator(t) or \
                    InfixEvaluator.is_operand(t) or \
                    InfixEvaluator.is_paren(t)):
                return False
        return True

    @staticmethod
    def tokenize(expr):
        tokens = expr.split(' ')
        return tokens

    @staticmethod
    def compute(operand2, operand1, operator):
        return InfixEvaluator.v_operations[operator](float(operand2), float(operand1))

    @staticmethod
    def precedence(operator1, operator2):
        return InfixEvaluator.opprec[operator1] >= InfixEvaluator.opprec[operator2]
     
    def __evaluate(self):
        for operator in self.operators.popall():
            if operator is not self.v_open_paren:
                operand1 = self.operands.pop()
                operand2 = self.operands.pop()
                result = InfixEvaluator.compute(operand2, operand1, operator)
                self.operands.push(result)
   
    # Evaluate the artimetic expression
    def evaluate(self, tokens):
        for t in tokens:
            if InfixEvaluator.is_operand(t):
                self.operands.push(t)
            elif InfixEvaluator.is_operator(t):
                top_operator = self.operators.peek()
                if top_operator is not None and \
                    top_operator is not self.v_open_paren and \
                    True == self.precedence(top_operator, t):
                        operand1 = self.operands.pop()
                        operand2 = self.operands.pop()
                        result = InfixEvaluator.compute(operand2, operand1, \
                                self.operators.pop())
                        self.operands.push(result)
                self.operators.push(t)
            elif InfixEvaluator.is_paren(t):
                if t == self.v_open_paren:
                    self.operators.push(t)
                else:
                    self.__evaluate()
        
        self.__evaluate()
        return self.operands.pop()

    def __call__(self, expr):
        tokens = self.tokenize(expr)
        if False == InfixEvaluator.validate(tokens):
            print "Invalid infix expression"
            return 

        return self.evaluate(tokens)

def usage():
    print "Usage: infix.py \"<expression with operators and operands seperated by space>\""

# Entry point
if __name__ == "__main__":
    l = len(sys.argv)
    if (l != 2):
        usage()
        exit(-1)

    E = InfixEvaluator()
    print E(sys.argv[1])
    
