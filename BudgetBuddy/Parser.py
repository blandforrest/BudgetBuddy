from difflib import SequenceMatcher as SM
from .CategoryMap import CATEGORY_MAP, CITY_LIST_FL
import xml.etree.ElementTree as ET
import PyPDF2
import logging
import json
import csv
import re

from abc import ABC, abstractmethod

from .Defines import Types, Expense

class FileParser(ABC):
    ''' Abstract class for the File Parser '''
    def __init__(self, file_path):
        self.expense_list = []
        self.logger       = logging.getLogger('BudgetBuddy.Parser')
        self.parse_budget_file(file_path)

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


class FileCategoryParser(FileParser):
    '''Accounts for formats with no category data'''
    def __init__(self, file_path):
        self.category_map  = CATEGORY_MAP
        self.name_list = list(self.category_map.keys())
        super().__init__(file_path)

    def key_category_map(self, key : str) -> str:
        '''Check if the key is in the map, otherwise, fuzzy check and confirm with user'''
        if key in self.category_map:
            return self.category_map[key]
        else:
            # Iterate through the name list, return the most similar string (This is expensive ...)
            value = ''
            score = 0.0
            for name in self.name_list:
                tmpscore = SM(None, key.lower(), name).ratio()*100

                if tmpscore > score:
                    value = name
                    score = tmpscore

            if score < 70:
                return 'Unknown'

            if value != '':
                category = self.category_map[value]
                self.logger.debug("Match correct? %s vs. %s Category: %s Score: %f", key.lower(), value, category, score)
                return category
            return 'Unknown'


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

class QIFParser(FileCategoryParser):
    '''Parser for QIF Files'''
    def parse_budget_file(self, file_path : str) -> list[Expense]:
        '''Parse a file, return a list of expenses'''
        try:
            with open(file_path, 'r', encoding="UTF-8") as in_file:
                tmp_str = [] # List of strings
                for line in in_file:
                    line = line.rstrip()

                    # Remove Comments
                    if line[0] == '!':
                        continue

                    # Build string until carrot
                    tmp_str.append(line)

                    # Hit the end of entry
                    if '^' in line:
                        name = tmp_str[3].replace('P','', 1)
                        expense = Expense(name,
                                        self.key_category_map(name),
                                        0.0,
                                        abs(self.str_to_float(tmp_str[1].replace('T-','', 1))))

                        self.expense_list.append(expense)
                        tmp_str = []
        except FileNotFoundError as ex:
            raise FileNotFoundError('Unable to find QIF File') from ex


class QFXParser(FileCategoryParser):
    '''Parser for QFX, OFX, QBO Files'''
    def parse_budget_file(self, file_path : str) -> list[Expense]:
        '''Parse a file, return a list of expenses'''

        root = ET.parse(file_path).getroot()

        for transaction in root.iter('STMTTRN'):
            if transaction.find('TRNTYPE').text != 'DEBIT':
                continue

            name = self.clean_description(transaction.find('MEMO').text)
            expense = Expense(name,
                              self.key_category_map(name),
                              0.0,
                              abs(self.str_to_float(transaction.find('TRNAMT').text)))

            self.expense_list.append(expense)

class PDFParser(FileCategoryParser):
    '''Parser for PDF Files'''
    def remove_city_state_from_description(self, description : str):
        '''Remove cities/state using regex'''
        florida_cities_pattern = re.compile(r'((' + '|'.join(CITY_LIST_FL) + r')' + r'FL)', re.IGNORECASE)

        return florida_cities_pattern.sub('', description)

    def parse_budget_file(self, file_path : str) -> list[Expense]:
        with open(file_path, 'rb') as in_file:
            pdf_reader = PyPDF2.PdfReader(in_file)

            for page_num, page in enumerate(pdf_reader.pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()

                if page_num > 2:
                    # Use regular expressions to extract transaction details
                    date_pattern = r'(((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s([0-9]{1,2})\s){2}(.*)[0-9]*\.[0-9]{2})'

                    dates = re.findall(date_pattern, text)
                    
                    # Use the first matching group
                    for match in dates:
                        cleaned_str = re.sub(r'((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s([0-9]{1,2})\s){2}', ' ', match[0])

                        split_string = cleaned_str.split('$')

                        description = self.remove_city_state_from_description(self.clean_description(split_string[0]))
                        cost        = self.str_to_float(split_string[1])

                        expense = Expense(description,
                                          self.key_category_map(description),
                                          0.0,
                                          abs(cost))

                        self.expense_list.append(expense)
