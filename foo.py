"""
    (2) Mathematical expression by string substitution
    • Find in input string simple expressions (a, 1+2, f(1)), and replate it by its result.
    • Input language is a sting like a + 2 - sin(-0.3)*(b - c).
    • Should support user-specific functions by passing something like {"foo": lambda x: x*42 } or by named arguments.
    • Run-time error should be processed correctly with detail error message.
    • You should use the default Python logging module to make the interpreter work transparent.
"""

# About reverse polish notation we reference the idea from https://www.jianshu.com/p/9b89703480e0
# Part of our code reference the code that already exists. We didn't remake the wheels.

from math import *

# Define symbol precedence
operators = ['+', '-', '*', '/', '(', ')', ',']
op_levels = {'+': 1, '-': 1, '*': 2, '/': 2, '(': 0}

# 这个暂时也没有仔细读
def negative_test(f):
    def test(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError:
            print('Wrong Expression! Please check the expression!')

    return test


class MathExpBySS(object):
    def __init__(self, formula='0'):
        self.formula = formula
        self.rpn_seq = []  # rpn sequence
        self.values = dict()  # empty dictionary

    def to_rpn(self):
        """ convert string formula to reverse polish notation(rpn_seq) """
        num_flag = 0  # number flag
        let_flag = 0  # letter flag
        op_stack = list()
        math_sym = ''
        # remove blank
        str_formula = self.formula.replace(' ', '')

        for index, tmp in enumerate(str_formula):
            if let_flag == 1:
                # Get math symbols such as cos sin func and pass it to math_sym
                if tmp not in operators:
                    math_sym += tmp
                    # close this loop and start to read next tmp
                    continue
                else:
                    if len(math_sym) == 1:
                        # add cos sin func... to node
                        self.rpn_seq.append(math_sym)
                    else:
                        # add operation to op_stack
                        op_stack.append(math_sym)
                    # reset the let_flag
                    let_flag = 0

            # if tmp is number include decimal
            if ((tmp >= '0') and (tmp <= '9')) or tmp == '.':
                if num_flag == 0:
                    # add number to rpn node
                    self.rpn_seq.append(tmp)
                    num_flag = 1
                else:
                    # Concatenate numeric strings such as '18' = '1'+'8'
                    self.rpn_seq[-1] = self.rpn_seq[-1] + tmp
                continue
            # reset the number flag
            num_flag = 0

            # if tmp is letter set the let_flag which affect the first if.
            if (tmp >= 'a') and (tmp <= 'z'):
                math_sym = tmp
                let_flag = 1
                continue

            if tmp == ',':
                continue

            # if the above if didn't run continue, tmp must be operator.
            if len(op_stack) == 0:
                op_stack.append(tmp)
                continue

            if tmp == '(':
                op_stack.append(tmp)
                continue

            # ) must match ( , so ( must be found
            if tmp == ')':
                while op_stack[-1] != '(':
                    self.rpn_seq.append(op_stack.pop(-1))
                # pop (
                op_stack.pop(-1)
                if (len(op_stack) != 0) and (op_stack[-1] not in operators):
                    self.rpn_seq.append(op_stack.pop(-1))
                continue

            # pop the higher level operator and add it to node
            while len(op_stack) != 0 and op_levels[op_stack[-1]] >= op_levels[tmp]:
                self.rpn_seq.append(op_stack.pop(-1))
            op_stack.append(tmp)

        if let_flag == 1:
            self.rpn_seq.append(math_sym)

        # pop all operator stack elements
        while len(op_stack) != 0:
            self.rpn_seq.append(op_stack.pop(-1))

    """
        Calculate the result based on the generated rpn sequence 
    """

    @negative_test
    def evaluate(self, **kwargs):  # **kwargs -> variable parameter
        stack = list()
        self.values = kwargs
        # facilitate the entire sequence
        for i in self.rpn_seq:
            if i == 'sin':
                stack.append(sin(stack.pop(-1)))
            elif i == 'cos':
                stack.append(cos(stack.pop(-1)))
            elif i == 'tan':
                stack.append(tan(stack.pop(-1)))
            elif i == '+':
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(left + right)
            elif i == '-':
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(left - right)
            elif i == '*':
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(left * right)
            elif i == '/':
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(left / right)
            elif i == 'log':
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(log(left, right))
            elif i == 'pow':
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(pow(left, right))
            elif i not in self.values.keys():
                stack.append(float(i))
            elif len(i) == 1:
                stack.append(self.values[i])
            # 这里还有些问题，暂时没看懂
            else:
                f = self.values[i]
                args_nums = f.__code__.co_argcount

                dic = dict()
                for j in range(args_nums):
                    dic[j] = stack.pop(-1)
                v = f(*dic.values())
                stack.append(v)

        return stack.pop(-1)
