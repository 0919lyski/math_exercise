import random
import time
from typing import List, Set, Tuple, Optional
from fraction import Fraction
from expression import Expression

class ProblemGenerator:
    """题目生成器，负责生成不重复的四则运算题目"""
    
    def __init__(self, number_range: int):
        """
        初始化生成器
        
        Args:
            number_range: 数值范围（不包括该值）
        """
        self.number_range = number_range
        self.generated_expressions: Set[str] = set()
        self.max_retry_count = 1000  # 最大重试次数，避免无限循环
    
    def generate_problems(self, count: int, max_operators: int = 3) -> List[Tuple[str, Fraction]]:
        """
        生成指定数量的题目
        
        Args:
            count: 题目数量
            max_operators: 最大运算符数量
            
        Returns:
            题目和答案的列表
        """
        problems = []
        retry_count = 0
        start_time = time.time()
        
        print(f"开始生成 {count} 道题目，数值范围: 0-{self.number_range-1}...")
        
        while len(problems) < count and retry_count < self.max_retry_count:
            try:
                # 随机选择运算符数量（1-3个）
                op_count = random.randint(1, max_operators)
                expr = self.generate_single_expression(op_count)
                
                # 检查是否重复
                if not self._is_duplicate(expr):
                    # 计算答案
                    answer = expr.evaluate()
                    # 格式化为题目字符串
                    problem_str = f"{expr.to_string()} ="
                    problems.append((problem_str, answer))
                    print(f"已生成 {len(problems)}/{count} 道题目")
                
            except (ValueError, ZeroDivisionError) as e:
                # 表达式不合法，继续生成
                pass
            finally:
                retry_count += 1
        
        if len(problems) < count:
            print(f"警告: 只生成了 {len(problems)} 道题目，未能达到要求的 {count} 道")
            print("可能是数值范围太小或去重条件太严格")
        
        end_time = time.time()
        print(f"题目生成完成，耗时: {end_time - start_time:.2f} 秒")
        
        return problems
    
    def generate_single_expression(self, operator_count: int) -> Expression:
        """
        生成单个表达式
        
        Args:
            operator_count: 运算符数量
            
        Returns:
            表达式对象
        """
        if operator_count == 0:
            # 生成叶子节点（数值）
            value = self._generate_random_number()
            return Expression(value=value)
        
        # 随机选择运算符
        operator = random.choice(['+', '-', '×', '÷'])
        
        # 分配左右子树的运算符数量
        left_op_count = random.randint(0, operator_count - 1)
        right_op_count = operator_count - 1 - left_op_count
        
        left_expr = self.generate_single_expression(left_op_count)
        right_expr = self.generate_single_expression(right_op_count)
        
        # 对于减法和除法，进行特殊处理确保合法性
        if operator == '-':
            # 确保左表达式 ≥ 右表达式，避免负数
            left_val = left_expr.evaluate()
            right_val = right_expr.evaluate()
            if left_val < right_val:
                # 交换左右表达式
                left_expr, right_expr = right_expr, left_expr
        elif operator == '÷':
            # 确保除数不为零，且结果为真分数（如果被除数小于除数）
            left_val = left_expr.evaluate()
            right_val = right_expr.evaluate()
            if right_val.numerator == 0:
                # 除数为零，重新生成右表达式
                right_expr = self.generate_single_expression(right_op_count)
                right_val = right_expr.evaluate()
            
            # 如果被除数小于除数，确保结果是真分数
            if left_val < right_val:
                # 这种情况下结果是真分数，符合要求
                pass
        
        expr = Expression(left=left_expr, right=right_expr, operator=operator)
        
        # 最终验证表达式合法性
        try:
            result = expr.evaluate()
            # 确保结果为正数（根据需求）
            if not result.is_positive() and result.numerator != 0:
                raise ValueError("结果必须为正数")
            return expr
        except (ValueError, ZeroDivisionError):
            # 如果表达式不合法，重新生成
            return self.generate_single_expression(operator_count)
    
    def _generate_random_number(self) -> Fraction:
        """
        生成随机数，包括整数和真分数
        
        Returns:
            分数对象
        """
        # 60%概率生成整数，40%概率生成真分数
        if random.random() < 0.6:
            # 生成整数
            return Fraction(random.randint(0, self.number_range - 1), 1)
        else:
            # 生成真分数
            denominator = random.randint(2, self.number_range)
            numerator = random.randint(1, denominator - 1)
            return Fraction(numerator, denominator)
    
    def _is_duplicate(self, expr: Expression) -> bool:
        """
        检查表达式是否重复
        
        Args:
            expr: 要检查的表达式
            
        Returns:
            是否重复
        """
        normalized = expr.normalized_form()
        
        if normalized in self.generated_expressions:
            return True
        
        self.generated_expressions.add(normalized)
        return False
    
    def clear_cache(self):
        """清空已生成表达式的缓存"""
        self.generated_expressions.clear()

    def generate_with_retry(self, count: int, max_retry: int = 3) -> List[Tuple[str, Fraction]]:
        """
        带重试的题目生成
        
        Args:
            count: 题目数量
            max_retry: 最大重试次数
            
        Returns:
            题目列表
        """
        for attempt in range(max_retry):
            try:
                problems = self.generate_problems(count)
                if len(problems) >= count * 0.9:  # 达到90%即认为成功
                    return problems
            except Exception as e:
                print(f"第 {attempt + 1} 次生成失败: {e}")
            
            self.clear_cache()
            print(f"开始第 {attempt + 2} 次重试...")
        
        # 最后一次尝试
        return self.generate_problems(count)
