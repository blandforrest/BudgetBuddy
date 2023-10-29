import csv
import re
from .BudgetDefines import Types, Expense

class BudgetParser():
    '''Responsible for parsing budget files and returning structured data'''

    def __init__(self):
        self.expense_list = []

    def str_to_float(self, num_str : str):
        '''Convert string to int, deal with whitespace'''
        if num_str == '':
            return 0.0
        else:
            return float(num_str)

    def clean_description(self, in_str):
        ''' Remove numbers and symbols from description'''
        pattern = r'[0-9!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]'
        cleaned_string = re.sub(pattern, '', in_str)
        return cleaned_string

    def parse_budget_file_csv(self, file_path : str) -> list:
        '''Reads in the CSV, returns the category and cost If no category, mark as None'''
        with open(file_path, newline='', encoding="utf-8") as in_file:
            
            # Open the file and skip the header row
            reader = csv.reader(in_file, delimiter=',')
            next(reader)

            for row in reader:

                # Strip the row and check if line is empty
                if not row[0] or row[0] == '\n':
                    continue
            
                description = self.clean_description(str(row[Types.DESCRIPTION.value]))
                expense = Expense(description,
                                  str(row[Types.CATEGORY.value]), 
                                  self.str_to_float(row[Types.CREDIT.value]),
                                  self.str_to_float(row[Types.DEBIT.value]))

                self.expense_list.append(expense)

        return self.expense_list

    def parse_file_set(self, directory_path : str):
        '''Take the path of a directory and parse all CSVs within'''
        pass