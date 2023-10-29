class BudgetCalculator:
    '''Return various calculations on the data'''

    def __init__(self, parser, file_name):
        self.parsed_budget    = parser.parse_budget_file_csv(file_name)
        self.expense_category = 0.00
        self.total_expense    = 0.00
        self.category_list    = self.create_category_list()

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

        for expense in self.parsed_budget:
            summary.setdefault(expense.category, 0.00)
            summary[expense.category] += expense.debit

        return summary

    def expense_reduction(self):
        '''For expenses within a category reduce and provide percentages'''
        summary = {}
        # For each category, obtain a list of expenses (Expenses per category)
        for expense in self.parsed_budget:
            # Remove store numbers (Hack format fix - will need to move to some other spot)
            description = expense.description

            summary.setdefault(expense.category, {})
            summary[expense.category].setdefault(description, 0.00)
            summary[expense.category][description] += expense.debit

        return summary