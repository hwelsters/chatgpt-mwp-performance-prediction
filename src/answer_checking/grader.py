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

        if answers.issubset(decimals): return "all"
        if len(decimals.intersection(answers)) > 0: return "some"
        return "none"

    @staticmethod
    def check_correct(response: str, answers):
        return Grader.ans_check(response, answers, lambda x : x)

    @staticmethod
    def check_rounded(response: str, answers):
        return Grader.ans_check(response, answers, lambda x :round(x))

    @staticmethod
    def check_floor(response: str, answers):
        return Grader.ans_check(response, answers, lambda x : math.floor(x))

    @staticmethod
    def extract_decimals(response : str):
        # TODO: Improve this. But it's also done once only so it's not a big deal
        l = '!@#$%&*\(\)_+=[]{}\|;:/?\'\"`'
        for s in l:
            response = response.replace(s, ' ')
        response = response.replace(',', '')

        response = re.sub(r'[a-zA-Z]*', '', response)

        response = response.replace('\n', ' ')
        split_sentence = response.split(' ')
        
        to_return = []
        for ans in split_sentence:
            # VERY HACKY SOLUTION WHICH MIGHT FAIL
            while len(ans) > 0 and (ans[len(ans) - 1] == '.'): ans = ans[:-1]
            if re.match(r"-?\d+", ans) or re.match(r"-?\d+\.?\d*", ans): 
                nums = re.findall(r'\d+(?:\.\d+)?', ans)
                for num in nums:
                    to_return.append(num)

        return to_return