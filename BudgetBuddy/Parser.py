import logging
import csv
import re

from .Defines import Types, Expense

class Parser():
    '''Responsible for parsing budget files and returning structured data'''

    def __init__(self):
        self.expense_list = []
        self.logger       = logging.getLogger('BudgetBuddy.Parser')

    @staticmethod
    def str_to_float(num_str : str) -> float:
        '''Convert string to int, deal with whitespace'''
        if num_str.strip() == '':
            return 0.0
        try:
            return float(num_str)
        except (ValueError, TypeError) as ex:
            raise ValueError(f"Invalid input: {num_str} is not a float") from ex

    @staticmethod
    def clean_description(in_str) -> str:
        ''' Remove numbers, symbols, whitespace from description'''
        if in_str is None:
            return ''

        cleaned_str = re.sub(r'[0-9!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]', '', in_str)
        cleaned_str = re.sub(r'\s+', ' ', cleaned_str)
        return cleaned_str.strip()

    def parse_budget_file(self, file_path : str) -> list:
        '''Reads in the CSV, returns the category and cost If no category, mark as None'''
        with open(file_path, newline='', encoding="utf-8") as in_file:

            # Open the file and skip the header row
            reader = csv.reader(in_file, delimiter=',')
            next(reader)

            for row in reader:
                # Check if line is empty
                if not row:
                    continue

                description = Parser.clean_description(str(row[Types.DESCRIPTION.value]))
                expense = Expense(description,
                                  str(row[Types.CATEGORY.value]), 
                                  Parser.str_to_float(row[Types.CREDIT.value]),
                                  Parser.str_to_float(row[Types.DEBIT.value]))

                self.expense_list.append(expense)

        return self.expense_list

    def parse_file_set(self, directory_path : str):
        '''Take the path of a directory and parse all CSVs within'''
        pass