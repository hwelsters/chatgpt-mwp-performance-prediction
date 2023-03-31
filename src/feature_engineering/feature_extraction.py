class MathFeatureExtraction:
    @staticmethod
    def count_number_of_feature(equations: list, symbol: str):
        count = 0
        for equation in equations:
            count += equation.count(symbol)
        return count

    @staticmethod
    def count_number_of_equations(equations: list):
        MathFeatureExtraction.count_number_of_feature(equations, '=')

    @staticmethod
    def count_number_of_additions(equations: list):
        MathFeatureExtraction.count_number_of_feature(equations, '+')

    @staticmethod
    def count_number_of_subtractions(equations: list):
        MathFeatureExtraction.count_number_of_feature(equations, '-')

    @staticmethod
    def count_number_of_divisions(equations: list):
        MathFeatureExtraction.count_number_of_feature(
            equations, '/') + MathFeatureExtraction.count_number_of_feature(equations, '÷')

    @staticmethod
    def count_number_of_multiplications(equations: list):
        MathFeatureExtraction.count_number_of_feature(
            equations, '×') + MathFeatureExtraction.count_number_of_feature(equations, '*')
