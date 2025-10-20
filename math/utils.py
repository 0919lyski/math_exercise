import random
import re
from typing import Union, List
from fraction import Fraction

def safe_eval(expression: str) -> Fraction:
    """
    安全地计算表达式值
    
    Args:
        expression: 表达式字符串
        
    Returns:
        计算结果
    """
    # 移除所有空格
    expr = expression.replace(' ', '')
    
    # 验证表达式只包含允许的字符
    if not re.match(r'^[\d\+\-\*\/\(\)\.]+$', expr):
        raise ValueError("表达式包含非法字符")
    
    # 简单的表达式求值（生产环境应该使用更安全的方法）
    try:
        # 替换分数表示
        expr = expr.replace('^', '+')  # 临时处理带分数
        
        # 使用Python的eval（注意：在生产环境中应该使用更安全的方法）
        result = eval(expr)
        
        if isinstance(result, int):
            return Fraction(result, 1)
        elif isinstance(result, float):
            # 将浮点数转换为分数
            from fractions import Fraction as PyFraction
            py_frac = PyFraction(result).limit_denominator(1000)
            return Fraction(py_frac.numerator, py_frac.denominator)
        else:
            raise ValueError("无法计算表达式")
            
    except Exception as e:
        raise ValueError(f"表达式计算错误: {e}")

def generate_random_fraction(max_value: int) -> Fraction:
    """生成随机分数"""
    if random.random() < 0.6:
        return Fraction(random.randint(0, max_value - 1), 1)
    else:
        denominator = random.randint(2, max_value)
        numerator = random.randint(1, denominator - 1)
        return Fraction(numerator, denominator)

def parse_expression(expr: str) -> Union[int, Fraction]:
    """解析表达式结果为整数或分数"""
    try:
        if '^' in expr or '/' in expr:
            return Fraction.from_string(expr)
        else:
            return int(expr)
    except:
        raise ValueError(f"无法解析表达式结果: {expr}")

def optimize_expression_generation(problems: List, max_cache_size: int = 10000):
    """
    优化表达式生成性能
    
    Args:
        problems: 问题列表
        max_cache_size: 最大缓存大小
    """
    if len(problems) > max_cache_size:
        # 对于大量题目，使用更高效的算法
        print("使用高性能模式生成题目...")
        
        # 可以在这里实现并行生成等优化
        pass

def validate_problem(problem: str, answer: Fraction) -> bool:
    """
    验证题目和答案的合法性
    
    Args:
        problem: 题目字符串
        answer: 答案
        
    Returns:
        是否合法
    """
    try:
        # 检查题目格式
        if not problem.endswith('='):
            return False
        
        # 检查答案格式
        answer_str = answer.to_string()
        if not answer_str:
            return False
        
        # 检查运算符数量
        operators = ['+', '-', '×', '÷']
        op_count = sum(problem.count(op) for op in operators)
        if op_count > 3 or op_count == 0:
            return False
        
        return True
    except:
        return False
