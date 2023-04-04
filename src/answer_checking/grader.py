import re
import math

class Grader:
    @staticmethod
    def ans_check(response : str, answers, process_func):
        decimals = Grader.extract_decimals(response)
        
        decimals = [float(x) for x in decimals]
        decimals = [process_func(x) for x in decimals]
        decimals = set(decimals)

        answers = [process_func(x) for x in answers]
        answers = set(answers)

        if len(answers.intersection(decimals)) == len(answers): return "all"
        if len(decimals.intersection(answers)) > 0: return "some"
        return "none"

    @staticmethod
    def check_correct(response: str, answers):
        return Grader.ans_check(response, answers, lambda x : x)

    @staticmethod
    def check_rounded(response: str, answers):
        return Grader.ans_check(response, answers, lambda x :round(x, 1))

    @staticmethod
    def check_floor(response: str, answers):
        return Grader.ans_check(response, answers, lambda x : math.floor(x))

    @staticmethod
    def extract_decimals(response : str):
        pattern = r'\d+(?:\.\d+)?'
        decimals = re.findall(pattern, response)
        return decimals