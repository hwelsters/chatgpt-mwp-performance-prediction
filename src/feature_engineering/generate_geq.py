class GenerateGeq:
    @staticmethod
    def generate_geq(input_df, column_name):
        max_val = int(round(input_df[column_name].max()))

        # Generate greater than or equal columns
        # It will be 1 if the number in column_name is greater than i. Otherwise, it will be 0
        for i in range(1, max_val + 1): 
            input_df[f"{column_name}_geq_{i}"] = input_df.apply(lambda row : 1 if row[column_name] >= i else 0, axis=1)

        return input_df