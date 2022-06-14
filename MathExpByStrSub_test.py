import unittest

from MathExpByStrSub import MathExpByStrSub


class TestMathExpByStrSub(unittest.TestCase):

    def test_Sin(self) -> None:
        mathExp = MathExpByStrSub('sin(0)+2*sin(0)-3')
        mathExp.to_rpn()
        self.assertEqual(mathExp.evaluate(), -3.0)
        mathExp2 = MathExpByStrSub('sin(0) + 2 * sin(0) + 3')
        mathExp2.to_rpn()
        self.assertEqual(mathExp2.evaluate(), 3.0)

    def test_Cos(self) -> None:
        mathExp = MathExpByStrSub('cos(0)+3*(cos(0)-1)')
        mathExp.to_rpn()
        self.assertEqual(mathExp.evaluate(), 1.0)
        mathExp2 = MathExpByStrSub('cos(0) - 3 * (cos(0) + 1)')
        mathExp2.to_rpn()
        self.assertEqual(mathExp2.evaluate(), -5.0)

    def test_Tan(self) -> None:
        mathExp = MathExpByStrSub('tan(0)+cos(0)')
        mathExp.to_rpn()
        self.assertEqual(mathExp.evaluate(), 1.0)
        mathExp2 = MathExpByStrSub('tan(0) - 3 * cos(0)')
        mathExp2.to_rpn()
        self.assertEqual(mathExp2.evaluate(), -3.0)

    def test_Add(self) -> None:
        mathExp = MathExpByStrSub('7+5+11+17')
        mathExp.to_rpn()
        self.assertEqual(mathExp.evaluate(), 40.0)
        mathExp2 = MathExpByStrSub('8 + 4 + 6')
        mathExp2.to_rpn()
        self.assertEqual(mathExp2.evaluate(), 18.0)

    def test_Subtract(self) -> None:
        mathExp = MathExpByStrSub('8*5-(10-7)')
        mathExp.to_rpn()
        self.assertEqual(mathExp.evaluate(), 37.0)
        mathExp2 = MathExpByStrSub('8 - 5 - (10 + 7)')
        mathExp2.to_rpn()
        self.assertEqual(mathExp2.evaluate(), -14.0)

    def test_Multiply(self) -> None:
        mathExp = MathExpByStrSub('3*5-4*7')
        mathExp.to_rpn()
        self.assertEqual(mathExp.evaluate(), -13.0)
        mathExp2 = MathExpByStrSub('3 * 5 + 4 * 7')
        mathExp2.to_rpn()
        self.assertEqual(mathExp2.evaluate(), 43.0)

    def test_Divide(self) -> None:
        mathExp = MathExpByStrSub('8/4+4/2')
        mathExp.to_rpn()
        self.assertEqual(mathExp.evaluate(), 4.0)
        mathExp2 = MathExpByStrSub('8 / 4 + 2 * (4 / 3 + 6 / 2)')
        mathExp2.to_rpn()
        self.assertEqual(round(mathExp2.evaluate(), 1), 10.7)

    def test_Log(self) -> None:
        mathExp = MathExpByStrSub('log(4,2)+log(8,2)')
        mathExp.to_rpn()
        self.assertEqual(mathExp.evaluate(), 5.0)
        mathExp2 = MathExpByStrSub('log(2,2) * log(9, 3)')
        mathExp2.to_rpn()
        self.assertEqual(mathExp2.evaluate(), 2.0)

    def test_Pow(self) -> None:
        mathExp = MathExpByStrSub('pow(4,2)+pow(2,3)')
        mathExp.to_rpn()
        self.assertEqual(mathExp.evaluate(), 24.0)
        mathExp2 = MathExpByStrSub('pow(4,2) / pow(2,3)')
        mathExp2.to_rpn()
        self.assertEqual(mathExp2.evaluate(), 2.0)

    def test_UserSpecificFunction(self) -> None:
        mathExp = MathExpByStrSub('a+b-5*c')
        mathExp.to_rpn()
        self.assertEqual(mathExp.evaluate(a=2, b=3, c=4), -15.0)

        mathExp1 = MathExpByStrSub('foo(x)+2+2*cos(0)/2-y')
        mathExp1.to_rpn()
        self.assertEqual(mathExp1.evaluate(x=2, y=3, foo=lambda x: x*42), 84.0)

        mathExp2 = MathExpByStrSub('a + 2 - sin(0.3) * (b - c)')
        mathExp2.to_rpn()
        self.assertEqual(round(mathExp2.evaluate(a=10, b=20, c=30), 1), 15.0)


if __name__ == '__main__':
    unittest.main()
