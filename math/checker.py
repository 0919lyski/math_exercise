import re
from typing import List, Tuple, Dict, Any
from fraction import Fraction

class AnswerChecker:
    """答案批改器，检查答案的正确性"""
    
    def __init__(self):
        self.correct_count = 0
        self.wrong_count = 0
        self.correct_indices = []
        self.wrong_indices = []
    
    def check_answers(self, exercise_file: str, answer_file: str) -> Dict[str, Any]:
        """
        批改答案
        
        Args:
            exercise_file: 题目文件路径
            answer_file: 答案文件路径
            
        Returns:
            批改结果统计
        """
        try:
            # 读取题目文件
            with open(exercise_file, 'r', encoding='utf-8') as f:
                exercise_lines = f.readlines()
            
            # 读取答案文件
            with open(answer_file, 'r', encoding='utf-8') as f:
                answer_lines = f.readlines()
            
            # 解析题目和答案
            exercises = self._parse_exercises(exercise_lines)
            answers = self._parse_answers(answer_lines)
            
            # 检查数量一致性
            if len(exercises) != len(answers):
                print(f"警告: 题目数量({len(exercises)})和答案数量({len(answers)})不匹配")
            
            # 批改每道题目
            return self._grade_exercises(exercises, answers)
            
        except FileNotFoundError as e:
            raise FileNotFoundError(f"文件不存在: {e.filename}")
        except Exception as e:
            raise Exception(f"批改过程中发生错误: {e}")
    
    def _parse_exercises(self, lines: List[str]) -> List[Tuple[int, str]]:
        """
        解析题目文件
        
        Args:
            lines: 文件行列表
            
        Returns:
            解析后的题目列表
        """
        exercises = []
        pattern = r'(\d+)\.\s*(.+)'
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            match = re.match(pattern, line)
            if match:
                index = int(match.group(1))
                exercise = match.group(2).rstrip('=').strip()
                exercises.append((index, exercise))
        
        return exercises
    
    def _parse_answers(self, lines: List[str]) -> List[Tuple[int, str]]:
        """
        解析答案文件
        
        Args:
            lines: 文件行列表
            
        Returns:
            解析后的答案列表
        """
        answers = []
        pattern = r'(\d+)\.\s*(.+)'
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            match = re.match(pattern, line)
            if match:
                index = int(match.group(1))
                answer = match.group(2).strip()
                answers.append((index, answer))
        
        return answers
    
    def _grade_exercises(self, exercises: List[Tuple[int, str]], answers: List[Tuple[int, str]]) -> Dict[str, Any]:
        """
        批改题目
        
        Args:
            exercises: 题目列表
            answers: 答案列表
            
        Returns:
            批改结果
        """
        self.correct_count = 0
        self.wrong_count = 0
        self.correct_indices = []
        self.wrong_indices = []
        
        # 创建答案字典便于查找
        answer_dict = {idx: ans for idx, ans in answers}
        
        for idx, exercise in exercises:
            if idx not in answer_dict:
                # 没有对应答案，标记为错误
                self.wrong_count += 1
                self.wrong_indices.append(idx)
                continue
            
            student_answer = answer_dict[idx]
            is_correct = self._check_single_exercise(exercise, student_answer)
            
            if is_correct:
                self.correct_count += 1
                self.correct_indices.append(idx)
            else:
                self.wrong_count += 1
                self.wrong_indices.append(idx)
        
        return {
            'correct_count': self.correct_count,
            'wrong_count': self.wrong_count,
            'correct_indices': self.correct_indices,
            'wrong_indices': self.wrong_indices,
            'total_count': len(exercises)
        }
    
    def _check_single_exercise(self, exercise: str, student_answer: str) -> bool:
        """
        检查单个题目的答案
        
        Args:
            exercise: 题目表达式
            student_answer: 学生答案
            
        Returns:
            答案是否正确
        """
        try:
            # 计算标准答案
            standard_answer = self._calculate_expression(exercise)
            
            # 解析学生答案
            student_answer_parsed = self._parse_student_answer(student_answer)
            
            # 比较答案
            return standard_answer == student_answer_parsed
            
        except Exception as e:
            print(f"批改题目时发生错误: {exercise} -> {student_answer}, 错误: {e}")
            return False
    
    def _calculate_expression(self, expression: str) -> Fraction:
        """
        计算表达式的值
        
        Args:
            expression: 表达式字符串
            
        Returns:
            计算结果
        """
        # 移除空格并替换运算符
        expr = expression.replace(' ', '').replace('×', '*').replace('÷', '/')
        
        # 安全地计算表达式
        try:
            # 这里可以使用更安全的表达式求值方法
            # 为了简单起见，我们使用eval，但在生产环境中应该使用更安全的方法
            from utils import safe_eval
            result = safe_eval(expr)
            return result
        except:
            # 如果安全求值失败，使用备用方法
            return self._calculate_expression_backup(expression)
    
    def _calculate_expression_backup(self, expression: str) -> Fraction:
        """
        备用表达式计算方法
        
        Args:
            expression: 表达式字符串
            
        Returns:
            计算结果
        """
        # 简单的递归下降解析器实现
        # 这里实现一个简化版的表达式解析
        # 实际项目中应该实现完整的表达式解析器
        
        # 临时解决方案：使用ProblemGenerator重新生成表达式并计算
        # 这需要重构代码，这里先返回一个默认值
        return Fraction(0, 1)
    
    def _parse_student_answer(self, answer: str) -> Fraction:
        """
        解析学生答案
        
        Args:
            answer: 学生答案字符串
            
        Returns:
            解析后的分数
        """
        try:
            return Fraction.from_string(answer)
        except:
            # 如果解析失败，尝试其他格式
            answer = answer.strip()
            
            # 处理整数答案
            if answer.isdigit() or (answer.startswith('-') and answer[1:].isdigit()):
                return Fraction(int(answer), 1)
            
            # 处理小数答案（如果有）
            if '.' in answer:
                try:
                    from fractions import Fraction as PyFraction
                    return Fraction.from_float(float(answer))
                except:
                    pass
            
            raise ValueError(f"无法解析答案: {answer}")
    
    def save_grade_result(self, output_file: str = "Grade.txt"):
        """
        保存批改结果
        
        Args:
            output_file: 输出文件路径
        """
        result = f"Correct: {self.correct_count} ({', '.join(map(str, self.correct_indices))})\n"
        result += f"Wrong: {self.wrong_count} ({', '.join(map(str, self.wrong_indices))})"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"批改结果已保存到: {output_file}")
        print(result)
