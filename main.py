from src.BudgetParser import BudgetParser
from src.BudgetCalculator import BudgetCalculator
from src.BudgetInterface import BudgetInterface

if __name__ == '__main__':
    parser = BudgetParser()
    calculator = BudgetCalculator(parser, 'testFile.csv')
    interface = BudgetInterface(calculator)

    interface.generate_sunburst_data()
