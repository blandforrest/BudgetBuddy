import argparse
import logging
import os
import sys

from BudgetBuddy.Parser import Parser
from BudgetBuddy.Calculator import Calculator
from BudgetBuddy.Interface import Interface

if __name__ == '__main__':
    # Configure the logging system
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info('Current working directory: %s', os.getcwd())
    
    # Get the file path from arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('file_path', help='File path to statement')
    args = arg_parser.parse_args()
    file_path = args.file_path

    if not os.path.exists(file_path):
        logging.error('File does not exist %s', file_path)
        sys.exit('File does not exist %s', file_path)

    logging.info('Successfully loaded %s!', file_path)

    # Create BudgetBuddy
    parser = Parser()
    calculator = Calculator(parser, file_path)
    interface = Interface(calculator)
    interface.generate_sunburst_data()
