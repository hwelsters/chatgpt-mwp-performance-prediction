import pandas
import nltk

from feature_engineering.equation_extraction import EquationExtraction
from feature_engineering.math_feature_extraction import MathFeatureExtraction
from feature_engineering.generate_geq import GenerateGeq

from answer_checking.grader import Grader
from causality_analysis.calculate_causality import Causality

from xlsx_creation.xlsx_writer import XlsxWriter

INPUT_FILE_PATH = "input/"
OUTPUT_FILE_PATH = "output/"

TEMPARATURE_COLUMN = 'temperature'

LSOLUTIONS_COLUMN = "lSolutions"
QUESTION_NUMBER_COLUMN = "question_number"
RESPONSE_COLUMN = "response"
EQUATIONS_COLUMN = "equations"
ROUNDED_COLUMN = "rounded"
NORMAL_COLUMN = "normal"

EFFECT_COLUMN = 'correct'
VALID_COLUMN = 'valid'

NUM_OF_ADDITIONS_COLUMN = 'num_of_additions'
NUM_OF_SUBTRACTIONS_COLUMN = 'num_of_subtractions'
NUM_OF_DIVISIONS_COLUMN = 'num_of_divisions'
NUM_OF_MULTIPLICATIONS_COLUMN = 'num_of_multiplications'
NUM_OF_EQUATIONS_COLUMN = 'num_of_equations'
NUM_OF_UNKNOWNS_COLUMN = 'num_of_unknowns'
PAIRS_OF_PARENTHESES_COLUMN = 'pairs_of_parentheses'

UNKNOWNS_COLUMN = 'unknowns'

NUM_OF_ADDITIONS_AND_SUBTRACTIONS_COLUMN = 'num_of_additions_and_subtractions'
NUM_OF_DIVISIONS_AND_MULTIPLICATIONS_COLUMN = 'num_of_divisions_and_multiplications'

# Run will execute a single run of:
# Extracting equations from text
# Extracting math features from the equations
# Predicting success
def run(input_file_path : str, question_file_path : str, output_file_path : str, description : str):
    input_df = pandas.read_json(input_file_path, lines=True)
    question_df = pandas.read_json(question_file_path)

    # ***********************************************************************************************

    # We check the following
    # If ChatGPT's response is correct without rounding
    # If ChatGPT's response is correct when both the answer and solution is rounded
    input_df[NORMAL_COLUMN] = input_df.apply(lambda row : Grader.check_correct(row[RESPONSE_COLUMN], question_df.loc[row[QUESTION_NUMBER_COLUMN]][LSOLUTIONS_COLUMN]), axis=1)
    input_df[ROUNDED_COLUMN] = input_df.apply(lambda row : Grader.check_rounded(row[RESPONSE_COLUMN], question_df.loc[row[QUESTION_NUMBER_COLUMN]][LSOLUTIONS_COLUMN]), axis=1)

    # Extract equations from ChatGPT's solution *****************************************************
    input_df[EQUATIONS_COLUMN] = input_df.apply(lambda row : EquationExtraction.extract_equations(row[RESPONSE_COLUMN]), axis=1)

    # Extract math features from extracted solution **************************************************
    input_df[NUM_OF_ADDITIONS_COLUMN] = input_df.apply(lambda row : MathFeatureExtraction.count_number_of_additions(row[EQUATIONS_COLUMN]), axis=1)
    input_df[NUM_OF_SUBTRACTIONS_COLUMN] = input_df.apply(lambda row : MathFeatureExtraction.count_number_of_subtractions(row[EQUATIONS_COLUMN]), axis=1)
    input_df[NUM_OF_MULTIPLICATIONS_COLUMN] = input_df.apply(lambda row : MathFeatureExtraction.count_number_of_multiplications(row[EQUATIONS_COLUMN]), axis=1)
    input_df[NUM_OF_DIVISIONS_COLUMN] = input_df.apply(lambda row : MathFeatureExtraction.count_number_of_divisions(row[EQUATIONS_COLUMN]), axis=1)
    input_df[NUM_OF_EQUATIONS_COLUMN] = input_df.apply(lambda row : MathFeatureExtraction.count_number_of_equations(row[EQUATIONS_COLUMN]), axis=1)
    input_df[NUM_OF_UNKNOWNS_COLUMN] = input_df.apply(lambda row : MathFeatureExtraction.count_number_of_unknowns(row[EQUATIONS_COLUMN]), axis=1)
    input_df[UNKNOWNS_COLUMN] = input_df.apply(lambda row : MathFeatureExtraction.get_unknowns(row[EQUATIONS_COLUMN]), axis=1)

    input_df[NUM_OF_ADDITIONS_AND_SUBTRACTIONS_COLUMN] = input_df.apply(lambda row : row[NUM_OF_ADDITIONS_COLUMN] + row[NUM_OF_SUBTRACTIONS_COLUMN],axis=1)
    input_df[NUM_OF_DIVISIONS_AND_MULTIPLICATIONS_COLUMN] = input_df.apply(lambda row : row[NUM_OF_DIVISIONS_COLUMN] + row[NUM_OF_MULTIPLICATIONS_COLUMN],axis=1)

    input_df = input_df.drop(columns=[NUM_OF_ADDITIONS_COLUMN, NUM_OF_SUBTRACTIONS_COLUMN, NUM_OF_MULTIPLICATIONS_COLUMN, NUM_OF_DIVISIONS_COLUMN])

    # Effect and valid column
    input_df[EFFECT_COLUMN] = input_df.apply(lambda row : 0 if row[NORMAL_COLUMN] == 'all' else 1, axis=1)
    input_df[VALID_COLUMN] = True

    # Observe ChatGPT's performance based on certain metrics *****************************************

    chatgpt_stats = {}
    chatgpt_stats.update(some_correct={
        'count': input_df.apply(lambda row : 1 if row[NORMAL_COLUMN] == 'some' else 0, axis=1).sum(),
        'definition': "ChatGPT's response  mentioned some of the numbers in the solution"
    })
    chatgpt_stats.update(all_correct={
        'count': input_df.apply(lambda row : 1 if row[NORMAL_COLUMN] == 'all' else 0, axis=1).sum(),
        'definition': "ChatGPT's response mentioned all the numbers in the solution"
    })
    chatgpt_stats.update(some_correct_rounded={
        'count': input_df.apply(lambda row : 1 if row[ROUNDED_COLUMN] == 'some' and row[NORMAL_COLUMN] == 'none' else 0, axis=1).sum(),
        'definition':"ChatGPT's response mentioned some of the numbers in the solution when both answers and ChatGPT's solutions were rounded."
    })
    
    chatgpt_stats.update(all_correct_rounded={
        'count': input_df.apply(lambda row : 1 if row[ROUNDED_COLUMN] == 'all'  and row[NORMAL_COLUMN] == 'none' else 0, axis=1).sum(),
        'definition': "ChatGPT's response mentioned all the numbers in the solution when both answers and ChatGPT's solutions were rounded."
    })

    chatgpt_stats.update(none_correct={
        'count': input_df.apply(lambda row : 1 if row[NORMAL_COLUMN] == 'none' and row[ROUNDED_COLUMN] == 'none' else 0, axis=1).sum(),
        'definition': "ChatGPT's response did not mention any of the numbers in the solution."
    })

    # Generate greater than or equal columns *********************************************************
    input_df = input_df.drop(columns=[NORMAL_COLUMN, ROUNDED_COLUMN])
    input_df = GenerateGeq.generate_geq(input_df, NUM_OF_ADDITIONS_AND_SUBTRACTIONS_COLUMN)
    input_df = GenerateGeq.generate_geq(input_df, NUM_OF_DIVISIONS_AND_MULTIPLICATIONS_COLUMN)
    input_df = GenerateGeq.generate_geq(input_df, NUM_OF_EQUATIONS_COLUMN)
    input_df = GenerateGeq.generate_geq(input_df, NUM_OF_UNKNOWNS_COLUMN)

    causality_df = Causality.causality_wrapper(input_df, VALID_COLUMN=VALID_COLUMN, EFFECT_COLUMN=EFFECT_COLUMN)

    XlsxWriter.write_xlsx(
        stats_obj=chatgpt_stats,
        causality_df=causality_df, 
        output_file_path=output_file_path, 
        description=description)

run(
    input_file_path=f"input/responses/draw/hwelsters__gpt-3.5-turbo-0301__v001.jsonl", 
    question_file_path="input/questions/draw.json", 
    output_file_path="output/hwelsters__gpt-3.5-turbo-0301__v001.xlsx",
    description='Suffixed questions with \'Let\'s think things through step by step to get the right answer\'',
)
