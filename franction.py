import math
from typing import Union, Tuple

class Fraction:
    """分数类，处理真分数和带分数的运算"""
    
    def __init__(self, numerator: int, denominator: int = 1, whole: int = 0):
        if denominator == 0:
            raise ValueError("分母不能为零")
        
        # 处理带分数
        if whole != 0:
            numerator = whole * denominator + numerator
            if numerator < 0:
                numerator = -numerator
        
        # 确保分母为正
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator
        
        self.numerator = numerator
        self.denominator = denominator
        self._simplify()
    
    def _simplify(self):
        """约分"""
        if self.numerator == 0:
            self.denominator = 1
            return
        
        gcd_val = math.gcd(abs(self.numerator), self.denominator)
        self.numerator //= gcd_val
        self.denominator //= gcd_val
    
    def to_mixed_number(self) -> Tuple[int, int, int]:
        """转换为带分数形式"""
        if self.numerator == 0:
            return (0, 0, 1)
        
        whole = self.numerator // self.denominator
        numerator = abs(self.numerator) % self.denominator
        
        if whole != 0:
            return (whole, numerator, self.denominator)
        else:
            return (0, self.numerator, self.denominator)
    
    def __add__(self, other: 'Fraction') -> 'Fraction':
        common_denominator = self.denominator * other.denominator
        numerator = (self.numerator * other.denominator + 
                    other.numerator * self.denominator)
        return Fraction(numerator, common_denominator)
    
    def __sub__(self, other: 'Fraction') -> 'Fraction':
        common_denominator = self.denominator * other.denominator
        numerator = (self.numerator * other.denominator - 
                    other.numerator * self.denominator)
        return Fraction(numerator, common_denominator)
    
    def __mul__(self, other: 'Fraction') -> 'Fraction':
        numerator = self.numerator * other.numerator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)
    
    def __truediv__(self, other: 'Fraction') -> 'Fraction':
        if other.numerator == 0:
            raise ValueError("除数不能为零")
        numerator = self.numerator * other.denominator
        denominator = self.denominator * other.numerator
        return Fraction(numerator, denominator)
    
    def __eq__(self, other: 'Fraction') -> bool:
        return (self.numerator * other.denominator == 
                other.numerator * self.denominator)
    
    def __lt__(self, other: 'Fraction') -> bool:
        return (self.numerator * other.denominator < 
                other.numerator * self.denominator)
    
    def __gt__(self, other: 'Fraction') -> bool:
        return (self.numerator * other.denominator > 
                other.numerator * self.denominator)
    
    def is_positive(self) -> bool:
        return self.numerator > 0
    
    def to_string(self) -> str:
        """转换为字符串表示"""
        if self.numerator == 0:
            return "0"
        
        whole, num, den = self.to_mixed_number()
        
        if whole == 0:
            if num == 0:
                return "0"
            else:
                return f"{num}/{den}"
        else:
            if num == 0:
                return f"{whole}"
            else:
                return f"{whole}^{num}/{den}"
    
    @staticmethod
    def from_string(s: str) -> 'Fraction':
        """从字符串解析分数"""
        s = s.strip()
        
        if '^' in s:
            # 带分数格式: a^b/c
            parts = s.split('^')
            whole = int(parts[0])
            fraction_part = parts[1]
            num, den = map(int, fraction_part.split('/'))
            return Fraction(num, den, whole)
        elif '/' in s:
            # 真分数格式: a/b
            num, den = map(int, s.split('/'))
            return Fraction(num, den)
        else:
            # 整数
            return Fraction(int(s), 1)
    
    def __str__(self) -> str:
        return self.to_string()
    
    def __repr__(self) -> str:
        return f"Fraction({self.numerator}/{self.denominator})"
