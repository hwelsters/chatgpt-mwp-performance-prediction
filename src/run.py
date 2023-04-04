import pandas
import os
import shutil
import datetime

from feature_engineering.equation_extraction import EquationExtraction
from feature_engineering.math_feature_extraction import MathFeatureExtraction
from feature_engineering.generate_geq import GenerateGeq

from answer_checking.grader import Grader
from causality_analysis.calculate_causality import Causality

from modelling.sklearn.get_classifier_results import get_classifier_results

from xlsx_creation.xlsx_writer import XlsxWriter

INPUT_FILE_PATH = "data/"
OUTPUT_FILE_PATH = "output/"

TEMPARATURE_COLUMN = 'temperature'

LSOLUTIONS_COLUMN = "lSolutions"
QUESTION_NUMBER_COLUMN = "question_number"
RESPONSE_COLUMN = "response"
EQUATIONS_COLUMN = "equations"
ROUNDED_COLUMN = "rounded"
NORMAL_COLUMN = "normal"
EXTRACTED_SOLUTIONS_COLUMN = "extracted_solution"

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
    input_df[LSOLUTIONS_COLUMN] = input_df.apply(lambda row : question_df.loc[row[QUESTION_NUMBER_COLUMN]][LSOLUTIONS_COLUMN], axis=1)

    # Extract equations from ChatGPT's solution *****************************************************
    input_df[EQUATIONS_COLUMN] = input_df.apply(lambda row : EquationExtraction.extract_equations(row[RESPONSE_COLUMN]), axis=1)
    input_df[EXTRACTED_SOLUTIONS_COLUMN] = input_df.apply(lambda row : Grader.extract_decimals(row[RESPONSE_COLUMN]), axis=1)

    # Extract math features from extracted solution **************************************************
    input_df[NUM_OF_ADDITIONS_COLUMN] = input_df.apply(lambda row : MathFeatureExtraction.count_number_of_additions(row[EQUATIONS_COLUMN]), axis=1)
    input_df[NUM_OF_SUBTRACTIONS_COLUMN] = input_df.apply(lambda row : MathFeatureExtraction.count_number_of_subtractions(row[EQUATIONS_COLUMN]), axis=1)
    input_df[NUM_OF_MULTIPLICATIONS_COLUMN] = input_df.apply(lambda row : MathFeatureExtraction.count_number_of_multiplications(row[EQUATIONS_COLUMN]), axis=1)
    input_df[NUM_OF_DIVISIONS_COLUMN] = input_df.apply(lambda row : MathFeatureExtraction.count_number_of_divisions(row[EQUATIONS_COLUMN]), axis=1)
    input_df[NUM_OF_EQUATIONS_COLUMN] = input_df.apply(lambda row : MathFeatureExtraction.count_number_of_equations(row[EQUATIONS_COLUMN]), axis=1)
    input_df[NUM_OF_UNKNOWNS_COLUMN] = input_df.apply(lambda row : MathFeatureExtraction.count_number_of_unknowns(row[EQUATIONS_COLUMN]), axis=1)
    input_df[UNKNOWNS_COLUMN] = input_df.apply(lambda row : MathFeatureExtraction.get_unknowns(row[EQUATIONS_COLUMN]), axis=1)
    input_df[PAIRS_OF_PARENTHESES_COLUMN] = input_df.apply(lambda row : MathFeatureExtraction.count_number_of_parentheses(row[EQUATIONS_COLUMN]), axis=1)

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
    input_df = GenerateGeq.generate_geq(input_df, NUM_OF_ADDITIONS_AND_SUBTRACTIONS_COLUMN)
    input_df = GenerateGeq.generate_geq(input_df, NUM_OF_DIVISIONS_AND_MULTIPLICATIONS_COLUMN)
    input_df = GenerateGeq.generate_geq(input_df, NUM_OF_EQUATIONS_COLUMN)
    input_df = GenerateGeq.generate_geq(input_df, NUM_OF_UNKNOWNS_COLUMN)
    input_df = GenerateGeq.generate_geq(input_df, PAIRS_OF_PARENTHESES_COLUMN)

    cause_df = input_df.drop(columns=[NORMAL_COLUMN, ROUNDED_COLUMN])
    causality_df = Causality.causality_wrapper(cause_df, VALID_COLUMN=VALID_COLUMN, EFFECT_COLUMN=EFFECT_COLUMN)
    
    results_df_x = input_df[[
        NUM_OF_ADDITIONS_AND_SUBTRACTIONS_COLUMN, 
        NUM_OF_DIVISIONS_AND_MULTIPLICATIONS_COLUMN, 
        NUM_OF_EQUATIONS_COLUMN,
        NUM_OF_UNKNOWNS_COLUMN,
        PAIRS_OF_PARENTHESES_COLUMN]]
    results_df_y = input_df[EFFECT_COLUMN]
    results_dict = get_classifier_results(results_df_x, results_df_y, 5, 42, True)

    XlsxWriter.write_xlsx(
        stats_obj=chatgpt_stats,
        causality_df=causality_df, 
        input_df=input_df,
        output_file_path=output_file_path,
        results_dict=results_dict,
        description=description)


if os.path.exists("output/draw"):
    shutil.rmtree("output/draw")
os.makedirs("output/draw")
if os.path.exists("output/alg514"):
    shutil.rmtree("output/alg514")
os.makedirs("output/alg514")

current_date = str(datetime.date.today())

run(
    input_file_path=f"data/responses/draw/abhinav_chatgpt_plus_results_feb.jsonl", 
    question_file_path="data/questions/draw.json", 
    output_file_path="output/draw/ChatGPT Plus Web results (extracted equations, DRAW-1K, February, No working).xlsx",
    description='No prompt engineering',
)

run(
    input_file_path=f"data/responses/draw/abhinav_chatgpt_results_feb.jsonl", 
    question_file_path="data/questions/draw.json", 
    output_file_path="output/draw/ChatGPT Web results (extracted equations, DRAW-1K, February, No Prompt Engineering).xlsx",
    description='Instructed ChatGPT to only return numbers without working.',
)

run(
    input_file_path=f"data/responses/draw/abhinav_chatgpt_results_jan.jsonl", 
    question_file_path="data/questions/draw.json", 
    output_file_path="output/draw/ChatGPT Web results (extracted equations, DRAW-1K, January, No working).xlsx",
    description='Instructed ChatGPT to only return numbers without working.',
)

run(
    input_file_path=f"data/responses/draw/hwelsters__gpt-3.5-turbo-0301__v001 (prefix__all_working).jsonl", 
    question_file_path="data/questions/draw.json", 
    output_file_path="output/draw/ChatGPT API results (extracted equations, DRAW-1K, March, All Working).xlsx",
    description='Prefixed with the following text: \'Answer the following math word problem. If there are multiple ways to work through the problem, show all possible ways.\'',
)

run(
    input_file_path=f"data/responses/draw/hwelsters__gpt-3.5-turbo-0301__v001 (prefix__all_working).jsonl", 
    question_file_path="data/questions/draw.json", 
    output_file_path="output/draw/ChatGPT API results (extracted equations, DRAW-1K, March, All Working).xlsx",
    description='Prefixed with the following text: \'Answer the following math word problem. If there are multiple ways to work through the problem, show all possible ways.\'',
)

run(
    input_file_path=f"data/responses/draw/hwelsters__gpt-3.5-turbo-0301__v001 (prefix__as_few_words).jsonl", 
    question_file_path="data/questions/draw.json", 
    output_file_path="output/draw/ChatGPT API results (extracted equations, DRAW-1K, March, As Few Words).xlsx",
    description='Prefixed with the following text: \'Solve the following math word problem with as few words as possible. \'',
)

run(
    input_file_path=f"data/responses/draw/hwelsters__gpt-3.5-turbo-0301__v001 (prefix__college students).jsonl", 
    question_file_path="data/questions/draw.json", 
    output_file_path="output/draw/ChatGPT API results (extracted equations, DRAW-1K, March, College Students).xlsx",
    description='Prefixed with the following text: \'Simulate three smart college students solving math word problems: Alice, Bob and Carl. Denote each student by mentioning their name in this format Name: before their response. \'',
)

run(
    input_file_path=f"data/responses/draw/hwelsters__gpt-3.5-turbo-0301__v001 (prefix__logic_reasoning).jsonl", 
    question_file_path="data/questions/draw.json", 
    output_file_path="output/draw/ChatGPT API results (extracted equations, DRAW-1K, March, Logic Reasoning).xlsx",
    description='Prefixed with the following text: \'You are a very smart math solver. You will use logic and reasoning to solve hard problems in the simplest way. Solve the following math problem. \'',
)

run(
    input_file_path=f"data/responses/draw/hwelsters__gpt-3.5-turbo-0301__v001 (prefix__mathematician).jsonl", 
    question_file_path="data/questions/draw.json", 
    output_file_path="output/draw/ChatGPT API results (extracted equations, DRAW-1K, March, Mathematician).xlsx",
    description='Prefixed with the following text: \'You will act as a very intelligent mathematician. You will be presented with a math word problem which I would like you to solve step-by-step with clear working. Output the correct solution at the end. \'',
)

run(
    input_file_path=f"data/responses/draw/hwelsters__gpt-3.5-turbo-0301__v001 (prefix__min_100_words).jsonl", 
    question_file_path="data/questions/draw.json", 
    output_file_path="output/draw/ChatGPT API results (extracted equations, DRAW-1K, March, Min 100 words).xlsx",
    description='Prefixed with the following text: \'Solve the following math word problem with a minimum of 100 words. \'',
)

run(
    input_file_path=f"data/responses/draw/hwelsters__gpt-3.5-turbo-0301__v001 (suffix__no-working).jsonl", 
    question_file_path="data/questions/draw.json", 
    output_file_path="output/draw/ChatGPT API results (extracted equations, DRAW-1K, March, No working).xlsx",
    description='Suffixed with the following text: \'Absolutely do not do any working at all. I just want the answers instantly with nothing but the answers. \'',
)

run(
    input_file_path=f"data/responses/draw/hwelsters__gpt-3.5-turbo-0301__v001 (suffix__step-by-step).jsonl", 
    question_file_path="data/questions/draw.json", 
    output_file_path="output/draw/ChatGPT API results (extracted equations, DRAW-1K, March, Step by step).xlsx",
    description='Suffixed with the following text: \'Let\'s think things through step by step to get the right answer \'',
)

run(
    input_file_path=f"data/responses/draw/hwelsters__gpt-3.5-turbo-0301__v001.jsonl", 
    question_file_path="data/questions/draw.json", 
    output_file_path="output/draw/ChatGPT API results (extracted equations, DRAW-1K, March, No prompt engineering).xlsx",
    description='No prompt engineering',
)

run(
    input_file_path=f"data/responses/alg514/hwelsters__gpt-3.5-turbo-0301__v001 (suffix__no-working).jsonl", 
    question_file_path="data/questions/alg514.json", 
    output_file_path="output/alg514/ChatGPT API results (extracted equations, ALG-514, March, No working).xlsx",
    description='No prompt engineering',
)

run(
    input_file_path=f"data/responses/alg514/hwelsters__gpt-3.5-turbo-0301__v001 (suffix__step-by-step).jsonl", 
    question_file_path="data/questions/alg514.json", 
    output_file_path="output/alg514/ChatGPT API results (extracted equations, ALG-514, March, Step-by-step).xlsx",
    description='No prompt engineering',
)

run(
    input_file_path=f"data/responses/alg514/hwelsters__gpt-3.5-turbo-0301__v001.jsonl", 
    question_file_path="data/questions/alg514.json", 
    output_file_path="output/alg514/ChatGPT API results (extracted equations, ALG-514, March, No prompt engineering).xlsx",
    description='No prompt engineering',
)
