from typing import List, Union, Optional
import random
from fraction import Fraction

class Expression:
    """表达式类，表示一个四则运算表达式"""
    
    def __init__(self, value=None, left=None, right=None, operator=None):
        self.left = left  # 左子表达式
        self.right = right  # 右子表达式
        self.operator = operator  # 运算符
        self.value = value  # 如果是叶子节点，存储数值
        
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None
    
    def evaluate(self) -> Fraction:
        """计算表达式的值"""
        if self.is_leaf():
            return self.value
        
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()
        
        if self.operator == '+':
            return left_val + right_val
        elif self.operator == '-':
            # 确保不产生负数
            if left_val < right_val:
                raise ValueError("减法结果不能为负数")
            return left_val - right_val
        elif self.operator == '×':
            return left_val * right_val
        elif self.operator == '÷':
            if right_val.numerator == 0:
                raise ValueError("除数不能为零")
            return left_val / right_val
        else:
            raise ValueError(f"未知运算符: {self.operator}")
    
    def to_string(self, parent_priority: int = 0) -> str:
        """将表达式转换为字符串"""
        if self.is_leaf():
            return self.value.to_string()
        
        # 定义运算符优先级
        priorities = {'+': 1, '-': 1, '×': 2, '÷': 2}
        current_priority = priorities[self.operator]
        
        left_str = self.left.to_string(current_priority)
        right_str = self.right.to_string(current_priority)
        
        # 根据优先级决定是否加括号
        expr_str = f"{left_str} {self.operator} {right_str}"
        if current_priority < parent_priority:
            expr_str = f"({expr_str})"
        
        return expr_str
    
    def __str__(self) -> str:
        return self.to_string()
    
    def normalized_form(self) -> str:
        """生成规范化形式用于去重比较"""
        if self.is_leaf():
            return self.value.to_string()
        
        left_norm = self.left.normalized_form()
        right_norm = self.right.normalized_form()
        
        # 对于可交换的运算符，排序子表达式
        if self.operator in ['+', '×']:
            if left_norm > right_norm:
                left_norm, right_norm = right_norm, left_norm
        
        return f"({left_norm}{self.operator}{right_norm})"
    
    def get_operator_count(self) -> int:
        """获取运算符数量"""
        if self.is_leaf():
            return 0
        return 1 + self.left.get_operator_count() + self.right.get_operator_count()
