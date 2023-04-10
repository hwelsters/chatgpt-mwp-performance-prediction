import xlsxwriter

import datetime

CHATGPT_VERSION = "ChatGPT"

STATS_WORKSHEET_TITLE = 'Overall'
CAUSALITY_WORKSHEET_TITLE = 'Causality_Values'
ADDS_AND_SUBS_TITLE = 'AddsSubs'
MULTS_AND_DIVS_TITLE = 'MultsDivs'
EQUATIONS_TITLE = 'Equations'
UNKNOWNS_TITLE = 'Unknowns'
PAIRS_OF_PARENS_TITLE = 'PairsOfParentheses'
MODEL_PERFORMANCE_TITLE='ModelPerformance'
LABELLED_RESPONSES_TITLE='LabelledResponses'

CAUSALITY_NAME_COLUMN = "name"
CAUSALITY_SUPPORT_COLUMN = "support"
CAUSALITY_CAUSALITY_COLUMN = "causality"
CAUSALITY_COND_PROB_COLUMN = "conditional_probability"
CAUSALITY_PRIOR_COLUMN = "prior"
CAUSALITY_REL_COLUMN = "rel"

class XlsxWriter:
    @staticmethod
    def write_xlsx(stats_obj, causality_df, input_df, output_file_path, description, results_dict):
        workbook = xlsxwriter.Workbook(output_file_path)

        header_format = workbook.add_format({
            'bold': True, 
            'underline': True,
            'font_size': 20,
            'font_color': 'black',
            'font_name': 'Calibri'})
        
        normal_format = workbook.add_format({
            'font_color': 'black',
            'font_size': 12,
            'font_color': 'black',
            'font_name': 'Calibri',
        })

        border_format = workbook.add_format({
            'font_color': 'black',
            'font_size': 12,
            'font_color': 'black',
            'font_name': 'Calibri',
            'border': 1,
            'border_color': '#d3cbbe'
        })
        emphasize_format = workbook.add_format({
            'bold': True, 
            'underline': True,
            'font_color': 'black',
            'font_size': 12,
            'font_color': 'black',
            'font_name': 'Calibri'
        })

        # Writing to stats worksheet ***********************************************************
        stats_worksheet = workbook.add_worksheet(STATS_WORKSHEET_TITLE)

        stats_worksheet.set_column(0, 0, 60)

        # Headers ---
        stats_worksheet.write(0, 0, 'Overall Performance Chart', header_format)
        stats_worksheet.write(0, 1, CHATGPT_VERSION, header_format)
        stats_worksheet.write(1, 0, description, header_format)
        
        # Column titles ---
        stats_worksheet.write(2, 0, 'Values', normal_format)
        stats_worksheet.write(2, 1, 'Count', normal_format)
        stats_worksheet.write(2, 3, 'Definitions', normal_format)

        # Info ---
        index = 0
        for key in stats_obj.keys():
            stats_worksheet.write(3 + index, 0, key, normal_format)
            stats_worksheet.write(3 + index, 1, stats_obj[key]['count'], normal_format)
            stats_worksheet.write(3 + index, 3, stats_obj[key]['definition'], normal_format)
            index += 1
        
        total_none_correct = stats_obj['none_correct']['count']
        total_all_correct = stats_obj['all_correct']['count'] + stats_obj['all_correct_rounded']['count']
        total_some_correct = stats_obj['some_correct']['count'] + stats_obj['some_correct_rounded']['count']
        total = total_none_correct + total_all_correct + total_some_correct
        prior = total_none_correct / total

        stats_worksheet.write(5 + index, 0, 'Returns answers, but none are correct', normal_format)
        stats_worksheet.write(5 + index, 1, total_none_correct, normal_format)
        stats_worksheet.write(6 + index, 0, 'Returns all answers correctly', normal_format)
        stats_worksheet.write(6 + index, 1, total_all_correct, normal_format)
        stats_worksheet.write(7 + index, 0, 'Returns some answers correctly, but not all values', normal_format)
        stats_worksheet.write(7 + index, 1, total_some_correct, normal_format)

        stats_worksheet.write(8 + index, 0, 'Total', normal_format)
        stats_worksheet.write(8 + index, 1, total, normal_format)

        stats_worksheet.write(11 + index, 0, 'Prior', normal_format)
        stats_worksheet.write(11 + index, 1, prior, normal_format)

        
        # Pie Chart ---
        pie_chart = workbook.add_chart({'type': 'pie'})
        pie_chart.set_style(10)
        pie_chart.set_size({'width' : 500, 'height': 300})
        pie_chart.set_title({'name': f'{CHATGPT_VERSION} stats'})
        pie_chart.add_series({
            'name' : f'{CHATGPT_VERSION} stats',
            'categories': f"={STATS_WORKSHEET_TITLE}!$A${5+index}:$A${8+index}",
            'values': f"={STATS_WORKSHEET_TITLE}!$B${5+index}:$B${8+index}",
            'points': [
                {'fill': {'color': '#e7366b'}},
                {'fill': {'color': '#29cc7a'}},
                {'fill': {'color': '#ffc619'}},
            ],
            'data_labels':{'value':True, 'category':True, 'position': 'center', 'percentage': True, 'name_font': {'size': 14} }
        })

        stats_worksheet.insert_chart('D11', pie_chart, {'x_offset': 0, 'y_offset': 0})

        # Causality Values *********************************************************************

        causality_worksheet = workbook.add_worksheet(CAUSALITY_WORKSHEET_TITLE)

        causality_worksheet.set_column(0, 0, 60)

        causality_worksheet.write(1, 0, "Causality Values Chart", header_format)
        causality_worksheet.write(1, 1, CHATGPT_VERSION, header_format)

        causality_worksheet.write(1, 0, "Name", normal_format)
        causality_worksheet.write(1, 1, "Support", normal_format)
        causality_worksheet.write(1, 2, "Quantity", normal_format)
        causality_worksheet.write(1, 3, "Conditional Probability", normal_format)
        causality_worksheet.write(1, 4, "Prior", normal_format)
        causality_worksheet.write(0, 5, "Rel", normal_format)

        index = 0
        for idx, row in causality_df.iterrows():
            causality_worksheet.write(2 + index, 0, row[CAUSALITY_NAME_COLUMN], normal_format)
            causality_worksheet.write(2 + index, 1, row[CAUSALITY_SUPPORT_COLUMN], normal_format)
            causality_worksheet.write(2 + index, 2, index + 1, normal_format)
            causality_worksheet.write(2 + index, 3, row[CAUSALITY_COND_PROB_COLUMN], normal_format)
            causality_worksheet.write(2 + index, 4, row[CAUSALITY_PRIOR_COLUMN], normal_format)
            causality_worksheet.write(2 + index, 5, row[CAUSALITY_REL_COLUMN], normal_format)
            index += 1

        def make_scattersheet(title, description, starts_with):
            adds_and_subs_worksheet = workbook.add_worksheet(title)
            adds_and_subs_worksheet.set_column(0, 0, 80)
            
            adds_and_subs_df = causality_df.loc[causality_df.apply(lambda row : row[CAUSALITY_NAME_COLUMN].startswith(starts_with), axis=1)]

            adds_and_subs_worksheet.write(0, 0, f"{description} Chart", header_format)
            adds_and_subs_worksheet.write(0, 1, CHATGPT_VERSION, header_format)

            adds_and_subs_worksheet.write(2, 0, "Name", normal_format)
            adds_and_subs_worksheet.write(2, 1, "Support", normal_format)
            adds_and_subs_worksheet.write(2, 2, "Quantity", normal_format)
            adds_and_subs_worksheet.write(2, 3, "Conditional Probability", normal_format)
            adds_and_subs_worksheet.write(2, 4, "Prior", normal_format)
            adds_and_subs_worksheet.write(2, 5, "Conditional - Prior", normal_format)
            adds_and_subs_worksheet.write(2, 6, "Factor 1", normal_format)
            adds_and_subs_worksheet.write(2, 7, "Factor 2", normal_format)
            adds_and_subs_worksheet.write(2, 8, "Square Error", normal_format)
            adds_and_subs_worksheet.write(2, 9, "Confidence Val", normal_format)
            adds_and_subs_worksheet.write(2, 10, "Amount", normal_format)
            adds_and_subs_worksheet.write(2, 11, "Bar", normal_format)

            index = 0
            for idx, row in adds_and_subs_df.iterrows():
                index += 1
                row_index = 2 + index
                excel_index = row_index + 1
                if row[CAUSALITY_COND_PROB_COLUMN] <= 0.001: break

                adds_and_subs_worksheet.write(row_index, 0, row[CAUSALITY_NAME_COLUMN], border_format)
                adds_and_subs_worksheet.write(row_index, 1, row[CAUSALITY_SUPPORT_COLUMN], border_format)
                adds_and_subs_worksheet.write(row_index, 2, index, normal_format)
                adds_and_subs_worksheet.write(row_index, 3, row[CAUSALITY_COND_PROB_COLUMN], border_format)
                adds_and_subs_worksheet.write(row_index, 4, row[CAUSALITY_PRIOR_COLUMN], border_format)
                adds_and_subs_worksheet.write(row_index, 5, row[CAUSALITY_COND_PROB_COLUMN] - row[CAUSALITY_PRIOR_COLUMN], normal_format)
                adds_and_subs_worksheet.write(row_index, 6, f"=1/(POWER(B{excel_index},1.5))", normal_format)
                adds_and_subs_worksheet.write(row_index, 7, f"=SQRT((D{excel_index}-POWER(10,-4))*B{excel_index}*((1-D{excel_index}+POWER(10,-4))*B{excel_index}))", normal_format)
                adds_and_subs_worksheet.write(row_index, 8, f"=G{excel_index}*H{excel_index}", normal_format)
                adds_and_subs_worksheet.write(row_index, 9, 1.95996398454, normal_format)
                adds_and_subs_worksheet.write(row_index, 10, f"=I{excel_index}*J{excel_index}", normal_format)
                adds_and_subs_worksheet.write(row_index, 11, f"=MIN(K{excel_index},1-D{excel_index})", normal_format)


            add_sub_scatter_chart = workbook.add_chart({'type': 'scatter'})
            add_sub_scatter_chart.add_series({
                'categories': f'={title}!$C$4:$C${4 + index}',
                'values': f'={title}!$D$4:$D${4 + index}',
            })
            add_sub_scatter_chart.set_title({'name': description})
            add_sub_scatter_chart.set_x_axis({'name': description, 'name_font': {'size': 24, 'bold': True},})
            add_sub_scatter_chart.set_y_axis({'name': 'Probability of total failure', 'name_font': {'size': 24, 'bold': True},}) 
            add_sub_scatter_chart.set_size({'width' : 1000, 'height': 1000})
            adds_and_subs_worksheet.insert_chart('M4', add_sub_scatter_chart, {'x_offset': 0, 'y_offset': 0})
        
        make_scattersheet(ADDS_AND_SUBS_TITLE, 'Number of Additions And Subtractions', 'num_of_additions_and_subtractions')
        make_scattersheet(MULTS_AND_DIVS_TITLE, 'Number of Multiplications And Divisions', 'num_of_divisions_and_multiplications')
        make_scattersheet(EQUATIONS_TITLE, 'Number of Equations', 'num_of_equations')
        make_scattersheet(UNKNOWNS_TITLE, 'Number of Unknowns', 'num_of_unknowns')
        make_scattersheet(PAIRS_OF_PARENS_TITLE, 'Pairs of Parentheses', 'pairs_of_parentheses')

        # graded_worksheet = workbook.add_worksheet(LABELLED_RESPONSES_TITLE)
        # graded_worksheet.set_column(0, 6, 80)
        # graded_worksheet.write(0, 0, 'Date Time', border_format)
        # graded_worksheet.write(0, 1, 'Questions', border_format)
        # graded_worksheet.write(0, 2, 'ChatGPT\'s Response', border_format)
        # graded_worksheet.write(0, 3, 'Correct solutions', border_format)
        # graded_worksheet.write(0, 4, 'Extracted solutions', border_format)
        # graded_worksheet.write(0, 5, 'Extracted unknowns', border_format)
        # graded_worksheet.write(0, 6, 'Extracted equations', border_format)
        # graded_worksheet.write(0, 7, 'Normal correct', border_format)
        # graded_worksheet.write(0, 8, 'Normal rounded', border_format)

        # index = 2
        # for idx, row in input_df.iterrows():
        #     if "date_time" in row.keys(): graded_worksheet.write(index, 0, str(row['date_time']), border_format)
        #     graded_worksheet.write(index, 1, str(row['question']), border_format)
        #     graded_worksheet.write(index, 2, str(row['response']), border_format)
        #     graded_worksheet.write(index, 3, str(row['lSolutions']), border_format)
        #     graded_worksheet.write(index, 4, str(row['extracted_solution']), border_format)
        #     graded_worksheet.write(index, 5, str(row['unknowns']), border_format)
        #     graded_worksheet.write(index, 6, str(row['equations']), border_format)
        #     graded_worksheet.write(index, 7, str(row['normal']), border_format)
        #     graded_worksheet.write(index, 8, str(row['rounded']), border_format)
        #     index += 1

        # Model values
        model_worksheet = workbook.add_worksheet(MODEL_PERFORMANCE_TITLE)
        model_worksheet.set_column(0, 6, 40)
        model_worksheet.write(0, 0, "Model type", emphasize_format)
        model_worksheet.write(0, 1, "Notes on Hyper parameters or structure", emphasize_format)
        model_worksheet.write(0, 2, "Date of Test", emphasize_format)
        model_worksheet.write(0, 3, "Average incorrect precision across 5CV", emphasize_format)
        model_worksheet.write(0, 4, "Average incorrect recall across 5CV", emphasize_format)
        model_worksheet.write(0, 5, "Average correct precision across 5CV", emphasize_format)
        model_worksheet.write(0, 6, "Average correct recall across 5CV", emphasize_format)

        bar_chart = workbook.add_chart({'type': 'column'})
        bar_chart.set_size({'width': 720, 'height': 400})

        current_date = str(datetime.date.today())
        index = 1
        for key in results_dict.keys():
            results = results_dict[key]
            model_worksheet.write(index, 0, key, normal_format)
            model_worksheet.write(index, 2, current_date, normal_format)
            model_worksheet.write(index, 3, results["0"]["average precision"], normal_format)
            model_worksheet.write(index, 4, results["0"]["average recall"], normal_format)
            model_worksheet.write(index, 5, results["1"]["average precision"], normal_format)
            model_worksheet.write(index, 6, results["1"]["average recall"], normal_format)

            bar_chart.add_series({
                'name': f'={MODEL_PERFORMANCE_TITLE}!$A${index + 1}',
                'categories': f'={MODEL_PERFORMANCE_TITLE}!$D$1:$G$1',
                'values': f'={MODEL_PERFORMANCE_TITLE}!$D${index + 1}:$G${index + 1}',
                'gap': 600
            })
            index += 1

        
        bar_chart.set_y_axis({'name': 'Percentage'})
        model_worksheet.insert_chart(f'A{index + 2}', bar_chart, {'y_offset': 0, 'x_offset': 0})

        workbook.close()
        

