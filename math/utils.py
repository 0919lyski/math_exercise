import random
from typing import List, Union
from fraction import Fraction

def generate_random_fraction(max_value: int) -> Fraction:
    """生成随机分数"""
    # 50%概率生成整数，50%概率生成真分数
    if random.random() < 0.5:
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
