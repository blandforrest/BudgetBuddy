import logging
import csv
import re

from abc import ABC, abstractmethod

from .Defines import Types, Expense

class FileParser(ABC):
    ''' Abstract class for the File Parser '''
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
        '''Remove numbers, symbols, whitespace from description'''
        if in_str is None:
            return ''

        cleaned_str = re.sub(r'[0-9!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]', '', in_str)
        cleaned_str = re.sub(r'\s+', ' ', cleaned_str)
        return cleaned_str.strip()
    
    @abstractmethod
    def parse_budget_file(self, file_path : str) -> list[Expense]:
        '''Parse a file, return a list of expenses'''
        pass


class CSVParser(FileParser):
    '''Parser for CSV Files'''
    def parse_budget_file(self, file_path : str) -> list[Expense]:
        '''Parse a file, return a list of expenses'''
        with open(file_path, newline='', encoding="utf-8") as in_file:

            # Open the file and skip the header row
            reader = csv.reader(in_file, delimiter=',')
            next(reader)

            for row in reader:
                # Check if line is empty
                if not row:
                    continue

                description = FileParser.clean_description(str(row[Types.DESCRIPTION.value]))
                expense     = Expense(description,
                                      str(row[Types.CATEGORY.value]), 
                                      FileParser.str_to_float(row[Types.CREDIT.value]),
                                      FileParser.str_to_float(row[Types.DEBIT.value]))

                self.expense_list.append(expense)

        return self.expense_list

class QIFParser(FileParser):
    '''Parser for QIF Files'''
    def parse_budget_file(self, file_path : str) -> list[Expense]:
        '''Parse a file, return a list of expenses'''
        pass

class QFXParser(FileParser):
    '''Parser for QFX Files'''
    def parse_budget_file(self, file_path : str) -> list[Expense]:
        '''Parse a file, return a list of expenses'''
        pass