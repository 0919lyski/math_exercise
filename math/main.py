#!/usr/bin/env python3
"""
小学四则运算题目生成器
支持生成题目、计算答案和批改功能
"""

import argparse
import sys
import os
from typing import List, Tuple
from fraction import Fraction
from generator import ProblemGenerator
from checker import AnswerChecker

class MathExerciseApp:
    """主应用程序类"""
    
    def __init__(self):
        self.generator = None
        self.checker = AnswerChecker()
    
    def run(self):
        """运行主程序"""
        parser = self._setup_argument_parser()
        args = parser.parse_args()
        
        try:
            if args.n and args.r:
                self.generate_exercises(args.n, args.r)
            elif args.e and args.a:
                self.check_answers(args.e, args.a)
            else:
                parser.print_help()
        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)
    
    def _setup_argument_parser(self) -> argparse.ArgumentParser:
        """设置命令行参数解析器"""
        parser = argparse.ArgumentParser(
            description='小学四则运算题目生成器',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''
示例:
  %(prog)s -n 10 -r 10         生成10道10以内的题目
  %(prog)s -e exercises.txt -a answers.txt  批改答案
            '''
        )
        
        # 题目生成参数
        parser.add_argument('-n', type=int, help='生成题目的数量')
        parser.add_argument('-r', type=int, help='数值范围（不包括该值）')
        
        # 答案批改参数
        parser.add_argument('-e', type=str, help='题目文件路径')
        parser.add_argument('-a', type=str, help='答案文件路径')
        
        return parser
    
    def generate_exercises(self, count: int, number_range: int):
        """
        生成题目和答案
        
        Args:
            count: 题目数量
            number_range: 数值范围
        """
        if count <= 0:
            raise ValueError("题目数量必须大于0")
        if number_range <= 1:
            raise ValueError("数值范围必须大于1")
        if count > 10000:
            print("警告: 生成题目数量超过10000，可能需要较长时间")
        
        # 初始化生成器
        self.generator = ProblemGenerator(number_range)
        
        # 生成题目
        problems = self.generator.generate_with_retry(count)
        
        if not problems:
            raise ValueError("未能生成任何题目，请调整参数重试")
        
        # 保存题目和答案
        self._save_exercises(problems)
        self._save_answers(problems)
        
        print(f"成功生成 {len(problems)} 道题目")
        print("题目文件: Exercises.txt")
        print("答案文件: Answers.txt")
    
    def _save_exercises(self, problems: List[Tuple[str, Fraction]]):
        """保存题目到文件"""
        with open('Exercises.txt', 'w', encoding='utf-8') as f:
            for i, (problem, _) in enumerate(problems, 1):
                f.write(f"{i}. {problem}\n")
    
    def _save_answers(self, problems: List[Tuple[str, Fraction]]):
        """保存答案到文件"""
        with open('Answers.txt', 'w', encoding='utf-8') as f:
            for i, (_, answer) in enumerate(problems, 1):
                f.write(f"{i}. {answer.to_string()}\n")
    
    def check_answers(self, exercise_file: str, answer_file: str):
        """
        批改答案
        
        Args:
            exercise_file: 题目文件路径
            answer_file: 答案文件路径
        """
        if not os.path.exists(exercise_file):
            raise FileNotFoundError(f"题目文件不存在: {exercise_file}")
        if not os.path.exists(answer_file):
            raise FileNotFoundError(f"答案文件不存在: {answer_file}")
        
        print(f"开始批改题目...")
        print(f"题目文件: {exercise_file}")
        print(f"答案文件: {answer_file}")
        
        # 批改答案
        result = self.checker.check_answers(exercise_file, answer_file)
        
        # 保存批改结果
        self.checker.save_grade_result()
        
        # 显示统计信息
        self._display_statistics(result)
    
    def _display_statistics(self, result: dict):
        """显示统计信息"""
        print("\n批改完成!")
        print(f"总题数: {result['total_count']}")
        print(f"正确: {result['correct_count']}题")
        print(f"错误: {result['wrong_count']}题")
        
        if result['total_count'] > 0:
            accuracy = result['correct_count'] / result['total_count'] * 100
            print(f"正确率: {accuracy:.1f}%")

def main():
    """主函数"""
    app = MathExerciseApp()
    app.run()

if __name__ == '__main__':
    main()
