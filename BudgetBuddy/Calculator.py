import logging

class Calculator:
    '''Return various calculations on the data'''

    def __init__(self, parser):
        self.parsed_budget    = parser.expense_list
        self.expense_category = 0.00
        self.total_expense    = 0.00
        self.category_list    = self.create_category_list()
        self.logger           = logging.getLogger('BudgetBuddy.Calculator')

    def create_category_list(self) -> list:
        '''Iterate through the expenses, create a list of categories'''
        return sorted(set([expense.category for expense in self.parsed_budget]))

    def expenses_per_category(self,  category : str) -> list:
        '''Given a category, return a list of expenses'''
        return [(expense.description, expense.debit) 
                for expense in self.parsed_budget if expense.category == category]

    def category_reduction(self) -> map:
        '''Return a map that contains the summary of all expenses'''
        summary = {}

        try:
            for expense in self.parsed_budget:
                summary.setdefault(expense.category, 0.00)
                summary[expense.category] += expense.debit
        except KeyError as ex:
            self.logger.error('Failed during category reduction: %s', ex.with_traceback)
            return None

        self.logger.debug('Completed category reduction %s', summary)
        return summary

    def expense_reduction(self):
        '''For expenses within a category reduce and provide percentages'''
        summary = {}

        try:
            for expense in self.parsed_budget:
                description = expense.description
                summary.setdefault(expense.category, {})
                summary[expense.category].setdefault(description, 0.00)
                summary[expense.category][description] += expense.debit
        except KeyError as ex:
            self.logger.error('Failed during expense reduction: %s', ex.with_traceback)
            return None

        self.logger.debug('Completed expense reduction %s', summary)
        return summary