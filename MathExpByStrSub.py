"""
    1. Find in input string simple expressions (a, 1+2, f(1)),
      and replate it by its result.
    2. Input language is a string like a + 2 - sin(-0.3)*(b - c).
    3. Should support user-specific functions by passing something like
      {"foo": lambda x: x*42 } or by named arguments.
    4. Run-time error should be processed correctly with detail error message.
    5. You should use the default Python logging module to make the
      interpreter work transparent.

    PS:
    About reverse polish notation, we reference the idea from
    https://www.jianshu.com/p/9b89703480e0
    Part of our code reference the code that already exists.
    We didn't remake the wheels.
"""
from typing import Any, List, Dict, Callable
from math import sin, cos, tan, log, pow

# Define symbol precedence
operators = ['+', '-', '*', '/', '(', ')', ',']
# Define operator levels
op_levels = {'+': 1, '-': 1, '*': 2, '/': 2, '(': 0}


def negative_test(f: Callable[..., Any]) -> Callable[..., Any]:
    def test(*args: Any, **kwargs: Any) -> Any:
        try:
            return f(*args, **kwargs)
        except ValueError:
            print('Wrong Expression! Please check the expression again.')
    return test


class MathExpByStrSub(object):
    def __init__(self, formula: str = '0') -> None:
        self.formula = formula
        self.rpn_seq = []  # type: List[Any]
        # dict() function is used to calculate the ordered rpn sequence
        self.values = dict()  # type: Dict[Any, Any]

    def to_rpn(self) -> None:
        """ Convert string formula to reverse polish notation(rpn_seq) """
        num_flag = 0  # Number flag
        let_flag = 0  # Letter flag
        op_stack = list()
        math_sym = ''
        # Remove blank
        str_formula = self.formula.replace(' ', '')

        for index, tmp in enumerate(str_formula):
            if let_flag == 1:
                """
                    Get math symbols such as sin, cos function
                    and pass it to math_sym
                """
                if tmp not in operators:
                    math_sym += tmp
                    # Close this loop and start to read next tmp
                    continue
                else:
                    if len(math_sym) == 1:
                        # Add sin, cos function... to the node
                        self.rpn_seq.append(math_sym)
                    else:
                        # Add operation to op_stack
                        op_stack.append(math_sym)
                    # Reset the let_flag
                    let_flag = 0

            # If tmp is number include decimal
            if ((tmp >= '0') and (tmp <= '9')) or tmp == '.':
                if num_flag == 0:
                    # Add number to rpn node
                    self.rpn_seq.append(tmp)
                    num_flag = 1
                else:
                    # Concatenate numeric strings such as '18' = '1'+'8'
                    self.rpn_seq[-1] = self.rpn_seq[-1] + tmp
                continue
            # Reset the number flag
            num_flag = 0

            # If tmp is letter set the let_flag which affect the first if.
            if (tmp >= 'a') and (tmp <= 'z'):
                math_sym = tmp
                let_flag = 1
                continue

            if tmp == ',':
                continue

            # If the above if didn't run continue, tmp must be operator.
            if len(op_stack) == 0:
                op_stack.append(tmp)
                continue

            if tmp == '(':
                op_stack.append(tmp)
                continue

            # ')' need to match '(' , so '(' must be found
            if tmp == ')':
                while op_stack[-1] != '(':
                    self.rpn_seq.append(op_stack.pop(-1))
                # Pop '('
                op_stack.pop(-1)
                if (len(op_stack) != 0) and (op_stack[-1] not in operators):
                    self.rpn_seq.append(op_stack.pop(-1))
                continue

            # Pop the higher level operator and add it to node
            while len(op_stack) != 0 and \
                    op_levels[op_stack[-1]] >= op_levels[tmp]:
                self.rpn_seq.append(op_stack.pop(-1))
            op_stack.append(tmp)

        if let_flag == 1:
            self.rpn_seq.append(math_sym)

        # Pop all operator stack elements
        while len(op_stack) != 0:
            self.rpn_seq.append(op_stack.pop(-1))

    """
        Calculate the result based on the generated rpn sequence
    """

    @negative_test
    def evaluate(self, **kwargs: Any) -> Any:
        stack = list()  # type: List[Any]
        # **kwargs: Parameter Dict
        self.values = kwargs
        # Facilitate the entire sequence
        for i in self.rpn_seq:
            if i == 'sin':
                """ Function Sine """
                stack.append(sin(stack.pop(-1)))
            elif i == 'cos':
                """ Function Cosine """
                stack.append(cos(stack.pop(-1)))
            elif i == 'tan':
                """ Function Tangent """
                stack.append(tan(stack.pop(-1)))
            elif i == '+':
                """ Function Add """
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(left + right)
            elif i == '-':
                """ Function Subtract """
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(left - right)
            elif i == '*':
                """ Function Multiply """
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(left * right)
            elif i == '/':
                """ Function Divide """
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(left / right)
            elif i == 'log':
                """ Function Log """
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(log(left, right))
            elif i == 'pow':
                """ Function Pow """
                right = stack.pop(-1)
                left = stack.pop(-1)
                stack.append(pow(left, right))
            elif i not in self.values.keys():
                stack.append(float(i))
            elif len(i) == 1:
                stack.append(self.values[i])
            else:
                # the values before operate push into the stack
                f = self.values[i]
                # co_argcount: The number of positional and keyword arguments of the function
                args_nums = f.__code__.co_argcount
                dictionary = dict()
                for j in range(args_nums):
                    dictionary[j] = stack.pop(-1)
                v = f(*dictionary.values())
                stack.append(v)
        # the last element in stack is the final result
        return stack.pop(-1)
