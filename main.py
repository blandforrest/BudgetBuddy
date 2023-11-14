import argparse
import logging
import os
import sys

from BudgetBuddy.Parser import CSVParser, QIFParser, QFXParser
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

    # Choose parser based on extension
    parser = None
    if file_path.lower().endswith('csv'):
        parser = CSVParser(file_path)
    elif file_path.lower().endswith('qif'):
        parser = QIFParser(file_path)
    elif file_path.lower().endswith('qfx'):
        parser = QFXParser(file_path)
    else:
        logging.fatal('UNSUPPORTED FILE TYPE %s! Exiting...', file_path) 


    # Create BudgetBuddy
    calculator = Calculator(parser)
    interface = Interface(calculator)
    interface.generate_sunburst_data()
