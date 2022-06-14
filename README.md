# Winter Palace - lab 3 - variant 2

## Description

Lab 3:  Basic Model of Computational

Objectives:

* Design an embedded domain-specific language or a simple text parser.
* Design architecture of a simple interpreter.
* Develop a simple interpreter for a specific model of computation.
* Develop unit tests.
* Develop input data control in the aspect-oriented style.

Variant 2:  Mathematical expression by string substitution

* Find in input string simple expressions (a, 1+2, f(1)), and replate it by its result.

* Input language is a sting like a + 2 - sin(-0.3)*(b - c).

* Should support user-specific functions by passing something like

   {"foo": lambda x: x*42 } or by named arguments.

* Run-time error should be processed correctly with detail error message.

* You should use the default Python logging module to make the

  interpreter work transparent.

## Group Information

Group Name: Winter Palace

Group members information as follows.

| HDU Number | Name            |
| ---------- | --------------- |
| 212320024  | Chen Chongzhong |
| 212320025  | Zuo Yuexin      |

## Project structure

- `MathExpByStrSub.py` -- Mathematical expression by string substitution.
- `MathExpByStrSub_test.py` -- Develop unit tests.

## Changelog

The third lab of CPO
HDU-ID: 212320024
Name: Chen Chongzhong
Date: 2022/06/14

1.Fix some problems.
2.Complete tunit tests.

---

The third lab of CPO
HDU-ID: 212320025
Name: Zuo Yuexin
Date: 2022/06/14

1.Fix some problems.
2.Complete some detail such as type and annotate.

---

The third lab of CPO
HDU-ID: 212320025
Name: Zuo Yuexin
Date: 2022/06/13

1.Complete main functions (evaluate and to_rpn).
2.Still have some small problem to fix.

## Design notes

About reverse polish notation, we reference the idea from
https://www.jianshu.com/p/9b89703480e0
Part of our code reference the code that already exists.
We didn't remake the wheels.
