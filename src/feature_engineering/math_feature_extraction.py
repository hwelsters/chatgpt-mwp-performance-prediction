import re

class MathFeatureExtraction:
    @staticmethod
    def count_number_of_equations(equations: list):
        return len(equations)

    @staticmethod
    def count_number_of_unknowns(equations: list):
        return len(MathFeatureExtraction.get_unknowns(equations))
    
    @staticmethod
    def get_unknowns(equations: list):
        unknowns = set()
        for equation in equations:
            split_equations = re.split(
                r'[0-9]|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\-|\_|\=|\+|\[|\{|\]|\}|\;|\:|\"|\'|\,|\<|\.|\>|\/|\?|\s', equation)
            for token in split_equations:
                if (len(token.strip()) != 1):
                    continue
                unknowns.add(token)
        return unknowns

    @staticmethod
    def count_number_of_feature(equations: list, symbol: str):
        equations = str(equations)
        count = 0
        for equation in equations:
            count += equation.count(symbol)
        return count

    @staticmethod
    def count_number_of_equations(equations: list):
        return MathFeatureExtraction.count_number_of_feature(equations, '=')

    @staticmethod
    def count_number_of_additions(equations: list):
        return MathFeatureExtraction.count_number_of_feature(equations, '+')

    @staticmethod
    def count_number_of_subtractions(equations: list):
        return MathFeatureExtraction.count_number_of_feature(equations, '-')

    @staticmethod
    def count_number_of_divisions(equations: list):
        return MathFeatureExtraction.count_number_of_feature(equations, '/') + MathFeatureExtraction.count_number_of_feature(equations, '÷')

    @staticmethod
    def count_number_of_multiplications(equations: list):
        return MathFeatureExtraction.count_number_of_feature(equations, '×') + MathFeatureExtraction.count_number_of_feature(equations, '*')
