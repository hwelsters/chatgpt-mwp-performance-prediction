import xlsxwriter

STATS_WORKSHEET_TITLE = 'Overall'
CAUSALITY_WORKSHEET_TITLE = 'Causality_Values'

class XlsxWriter:
    @staticmethod
    def write_xlsx(stats_obj, causality_df, output_file_path, description):
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

        # Writing to stats worksheet ***********************************************************
        stats_worksheet = workbook.add_worksheet(STATS_WORKSHEET_TITLE)

        stats_worksheet.set_column(0, 0, 60)

        # Headers ---
        stats_worksheet.write(0, 0, 'Overall Performance Chart', header_format)
        stats_worksheet.write(0, 1, 'ChatGPT', header_format)
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
        pie_chart.add_series({
            'name' : 'ChatGPT stats',
            'categories': f"={STATS_WORKSHEET_TITLE}!$A${5+index}:$A${8+index}",
            'values': f"={STATS_WORKSHEET_TITLE}!$B${5+index}:$B${8+index}",
            'points': [
                {'fill': {'color': '#e7366b'}},
                {'fill': {'color': '#29cc7a'}},
                {'fill': {'color': '#ffc619'}},
            ],
            'data_labels':{'value':True, 'category':True, 'position': 'center', 'percentage': True, 'name_font': {'size': 14} }
        })

        stats_worksheet.insert_chart('C11', pie_chart, {'x_offset': 0, 'y_offset': 0})

        # Causality Values *********************************************************************

        causality_worksheet = workbook.add_worksheet(CAUSALITY_WORKSHEET_TITLE)

        causality_worksheet.set_column(0, 0, 60)

        causality_worksheet.write(0, 0, "Name", normal_format)
        causality_worksheet.write(0, 1, "Support", normal_format)
        causality_worksheet.write(0, 2, "Causality", normal_format)
        causality_worksheet.write(0, 3, "Conditional Probability", normal_format)
        causality_worksheet.write(0, 4, "Prior", normal_format)
        causality_worksheet.write(0, 5, "Rel", normal_format)

        index = 0
        for idx, row in causality_df.iterrows():
            causality_worksheet.write(1 + index, 0, row["name"], normal_format)
            causality_worksheet.write(1 + index, 1, row["support"], normal_format)
            causality_worksheet.write(1 + index, 2, row["causality"], normal_format)
            causality_worksheet.write(1 + index, 3, row["conditional_probability"], normal_format)
            causality_worksheet.write(1 + index, 4, row["prior"], normal_format)
            causality_worksheet.write(1 + index, 5, row["rel"], normal_format)
            index += 1

        workbook.close()


