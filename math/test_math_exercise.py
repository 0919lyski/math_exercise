#!/usr/bin/env python3
"""测试用例"""

import unittest
import os
import tempfile
from fraction import Fraction
from expression import Expression
from generator import ProblemGenerator
from checker import AnswerChecker

class TestFraction(unittest.TestCase):
    """分数类测试"""
    
    def test_fraction_creation(self):
        f = Fraction(1, 2)
        self.assertEqual(f.numerator, 1)
        self.assertEqual(f.denominator, 2)
    
    def test_addition(self):
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)
        result = f1 + f2
        self.assertEqual(result.numerator, 5)
        self.assertEqual(result.denominator, 6)
    
    def test_mixed_number(self):
        f = Fraction(5, 2)
        whole, num, den = f.to_mixed_number()
        self.assertEqual(whole, 2)
        self.assertEqual(num, 1)
        self.assertEqual(den, 2)

class TestProblemGenerator(unittest.TestCase):
    """题目生成器测试"""
    
    def test_generate_single_expression(self):
        generator = ProblemGenerator(10)
        expr = generator.generate_single_expression(2)
        self.assertIsInstance(expr, Expression)
    
    def test_no_negative_results(self):
        generator = ProblemGenerator(10)
        problems = generator.generate_problems(10)
        
        for problem, answer in problems:
            self.assertTrue(answer.is_positive() or answer.numerator == 0)

def run_example():
    """运行示例"""
    print("=== 小学四则运算题目生成器示例 ===\n")
    
    # 示例1: 生成10道题目
    print("1. 生成10道10以内的题目:")
    print("   python main.py -n 10 -r 10")
    
    # 示例2: 批改答案
    print("\n2. 批改答案:")
    print("   python main.py -e Exercises.txt -a Answers.txt")
    
    # 示例3: 性能测试
    print("\n3. 性能测试（生成1000道题目）:")
    print("   python main.py -n 1000 -r 20")
    
    print("\n=== 测试用例执行 ===")
    
    # 执行单元测试
    unittest.main(verbosity=2, exit=False)

if __name__ == '__main__':
    run_example()
