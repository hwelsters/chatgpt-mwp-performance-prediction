import pandas as pd

MAX_NAME_DIFFERENCE = 5

class Causality:
    @staticmethod
    def causality_wrapper(input_df, VALID_COLUMN, EFFECT_COLUMN):
        def negation(column):
            # negation -- 
            # OUTPUT: returns a column of 0s and 1s of the negation of [column]. 1s are flipped to 0 and vice versa
            # INPUT: [column] should be a column of 0s and 1s
            return 1 - column
            
            """"""
        def conjunction(column_1, column_2):
            # conjunction -- 
            # output: returns a column of 0s and 1s of the conjunction between [column_1] and [column_2].
            # INPUT: [column_1] and [column_2] should be columns of 0s and 1s
            return column_1 * column_2
            
            """"""
        def disjunction(column_1, column_2):
            # disjunction -- 
            # OUTPUT: returns a column of 0s and 1s of the disjunction between [column_1] and [column_2].
            # INPUT: [column_1] and [column_2] should be columns of 0s and 1s
            return column_1 | column_2
            
            """"""
        def conditional_probability(occurence_column, condition_column):
            # conditional_probability -- 
            # OUTPUT: returns a number which represents the conditional probability p(occurence | condition)
            # INPUT: [occurence_column] and [condition_column] should be columns of 0s and 1s
            if condition_column.sum() == 0: return 0
            return conjunction(occurence_column, condition_column).sum() / condition_column.sum()
            
            """"""
        def prior(data):
            # prior -- 
            # OUTPUT: returns a number which represents the prior
            # INPUT: [data] should be a Pandas dataframe with the columns [CORRECT_COLUMN] and [VALID_COLUMN].
            # TODO : Possible optimizations can be made where we cache the result instead of calling this expensive operation again and again
            return conditional_probability(data[EFFECT_COLUMN], data[VALID_COLUMN])
            
            """"""
        def is_prima_facie(data, column_name):
            # is_prima_facie -- 
            # OUTPUT: returns a boolean which determines whether the column indicated by [column_name] is a prima facie
            # INPUT: [data] should be a Pandas dataframe with the columns [CORRECT_COLUMN] and [VALID_COLUMN].
            # INPUT: [column_name] should be a valid column in [data]
            # INPUT: The [CORRECT_COLUMN] and [VALID_COLUMN] columns should be columns of 0s and 1s 
            return conditional_probability(data[EFFECT_COLUMN], data[column_name]) - prior(data) > 0
            
            """"""
        def is_cooccur(column_1, column_2):
            # is_cooccur -- 
            # OUTPUT: returns a boolean based on if there is at least one row where both [column_1] and [column_2] is equal to 1
            # INPUT: [column_1] and [column_2] should both be columns of 0s and 1s
            return conjunction(column_1, column_2).sum() > 0
            
            """"""
        def is_same_category(column_name_1, column_name_2):
            # same_category -- 
            # OUTPUT: Returns a boolean signifying whether the [column_name_1] and [column_name_2] are different by [MAX_NAME_DIFFERENCE]
            #         If the two words are not different by [MAX_NAME_DIFFERENCE], they are in the same category so it returns true
            count = 0
            shortest = min(len(column_name_1), len(column_name_2))
            for i in range(0, shortest):
                if column_name_1[i] == column_name_2[i]:
                    count = count + 1
            return max(len(column_name_1), len(column_name_2)) - count < MAX_NAME_DIFFERENCE
            
            """"""
        def rel(data, column_name):
            # rel -- 
            # OUTPUT: returns a list of the names of other columns which cooccur with [column_name] and are prima facie
            # INPUT: [data] should be a Pandas dataframe with the columns [CORRECT_COLUMN] and [VALID_COLUMN].
            # INPUT: [column_name] should be a valid column in [data]
            # INPUT: The [CORRECT_COLUMN] and [VALID_COLUMN] columns should be columns of 0s and 1s 
            
            # # If it is not a prima facie cause, we don't bother to find its rel
            if not is_prima_facie(data,column_name): return[]
            
            if prior(data) >= conditional_probability(data[EFFECT_COLUMN], data[column_name]):
                return []
                
            if column_name in [VALID_COLUMN, EFFECT_COLUMN]: return []
            
            name_list = []
            for potential_cause in data.columns:
                # Make sure we are not including the [CORRECT_COLUMN] and [VALID_COLUMN] as part of rel
                if potential_cause in [EFFECT_COLUMN, VALID_COLUMN, column_name]: continue

                if is_same_category(potential_cause, column_name): continue

                if is_cooccur(data[column_name], data[potential_cause]) and is_prima_facie(data, potential_cause):
                    name_list.append(potential_cause)
            return name_list
            
            """"""
        def calculate_causality(data, column_name):
            # calculate_causality -- 
            # OUTPUT: returns a number which represents the causality value of the column indicated by [column_name]
            # INPUT: [data] should be a Pandas dataframe with the columns [CORRECT_COLUMN].
            # INPUT: [column_name] should be a valid column in [data]
            # INPUT: The [CORRECT_COLUMN] and [VALID_COLUMN] columns should be columns of 0s and 1s 

            # If it's not a prima facie cause, we don't bother to calculate its causality value
            if not is_prima_facie(data, column_name):
                return "n/a"

            relateds = rel(data, column_name)
            total_probability = 0
            for related in relateds:
                conj = conjunction(data[column_name], data[related])
                negj = conjunction(negation(data[column_name]), data[related])

                k = data[column_name].sum() / len(data)
                conj = conditional_probability(data[EFFECT_COLUMN], conj)
                negj = conditional_probability(data[EFFECT_COLUMN], negj)

                total_probability += k * (conj - negj)

            if (len(relateds) > 0): return total_probability / len(relateds)
            return total_probability
            
            """"""
        def is_binary_column(data, column_name):
            # is_binary_column --
            # Checks to see if a column is a column of 1s and 0s
            # INPUT: [data] is a dataframe
            # INPUT: [column_name] should be the name of a valid column in [data]
            return data.apply(lambda row : 0 if (isinstance(row[column_name], int) and (row[column_name] <= 1)) else 1, axis=1).sum() <= 0
            
            """"""
        def remove_non_binary_columns(data):
            # remove_non_binary_columns --
            # Removes all columns that are not 0s or 1s in the dataset
            # INPUT: [data] is a dataframe
            non_binary = []
            for i in data.columns:
                if i in [EFFECT_COLUMN, VALID_COLUMN]: continue
                if not is_binary_column(data, i):
                    non_binary.append(i)

            return data.drop(columns=non_binary)
            
            """"""
        def generate_row(data, column_name):
            # generate_row --
            # TODO: This is kind of a terrible name but I can't really think of anything more descriptive. If anyone has any ideas, feel free to modify it
            # It basically creates a row, which is actually a data frame with all the data that is needed
            # OUTPUT: It outputs a row with all the required values
            # INPUT: [data] should be a dataframe
            # INPUT: [column_name] should be a string representing a valid column in [data]
            toReturn = pd.DataFrame({
                "name": [column_name], 
                "support": conjunction(data[column_name], data[VALID_COLUMN]).sum(),
                "causality": [calculate_causality(data, column_name)],
                "rel": ','.join(rel(data, column_name)),
                "conditional_probability":[conditional_probability(data[EFFECT_COLUMN], data[column_name])], 
                "prior": prior(data),
                "conditional - prior": conditional_probability(data[EFFECT_COLUMN], data[column_name]) - prior(data)
            })
            return toReturn
            
            """"""

        def causality_values(input_df):
            # causality_values --
            # Calculates causality values

            # Then remove all the non binary columns
            input_df = remove_non_binary_columns(input_df)

            # TODO: This is a hack
            short_names = []
            for column in input_df.columns:
                if len(column) < 5 and column != VALID_COLUMN and column != EFFECT_COLUMN: short_names.append(column)
            input_df = input_df.drop(columns=short_names, axis=1)

            # TODO: I'm not sure if there's another way to do this, so feel free to make modifications
            # Generate a dud data frame with a single so we can append to it.
            to_save = generate_row(input_df, VALID_COLUMN)
            for column in input_df.columns:
                if column in [VALID_COLUMN, EFFECT_COLUMN]: continue
                to_save = to_save.append(generate_row(input_df, column))

            # Remove the dud first row
            to_save = to_save[1:]
            return to_save

            """"""

        to_return = causality_values(input_df)
        return to_return