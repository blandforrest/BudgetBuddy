import csv
from enum import Enum  
import plotly.express as px
import polars as pl
import plotly.graph_objects as go

# Can have categories (Food, Mortgage, Car(Gas and expenses), Utilities, Entertainment)
# We can consider subcategories later on, 

# Something to consider is that the filename/filepath will come from the user. 

# Will have to consider the case where multiple files make up a monthly expense report
    # Most of the picture is in my credit card, but I will also have my checking account where electric and mortgage are pulled from
    # Can consider this after getting the rest working

# Subcategories will need to have more insight into each transaction
    # We have groceries and alcohol that appear under "merchandise"

# We should have multiple reduction functions that also provide percentages per category
    # Important data here will be total cost and percentage
    # Reductions from different levels
        # Level 1 -> General categories (Merchandise, Gas, Dining, Phone, Utilities
        # Level 2 -> Within Merchandise, how much did I spend on Publix? 
            # Maybe we don't need to get into subcategories.. The end user will know what each expense is once they get down to Level 2
            # The percentages are what matters - How much did we spend on Publix compared to ABC

# How can I determine if we are doing separate months vs multiple files in one month? 
    # File structure? 

class Types(Enum):
    '''Types to index CSV'''
    DESCRIPTION = 3
    CATEGORY    = 4
    DEBIT       = 5
    CREDIT      = 6

class Expense():
    '''Responsible for storing the data from the CSV'''
    class ExpenseType(Enum):
        '''Expense can either be debit or credit'''
        DEBIT  = 0
        CREDIT = 1

    def __init__(self, description, category, credit, debit):
        self.description = description
        self.category = category
        self.credit = credit
        self.debit = debit
        self.type = None

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

    def parse_budget_file_csv(self, file_path : str) -> list:
        '''Reads in the CSV, returns the category and cost If no category, mark as None'''
        with open(file_path, newline='', encoding="utf-8") as in_file:
            for row in csv.reader(in_file, delimiter=','):              

                expense = Expense(str(row[Types.DESCRIPTION.value]), 
                                  str(row[Types.CATEGORY.value]), 
                                  self.str_to_float(row[Types.CREDIT.value]),
                                  self.str_to_float(row[Types.DEBIT.value]))

                self.expense_list.append(expense)

        return self.expense_list

    def parse_file_set(self, directory_path : str):
        '''Take the path of a directory and parse all CSVs within'''
        pass


class BudgetCalculator():
    '''Return various calculations on the data'''

    def __init__(self):
        self.parser = BudgetParser()
        self.parsed_budget = self.parser.parse_budget_file_csv('testFile.csv')
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
            description = expense.description.replace('TST*', '').replace('SQ *', '').split()[0]

            summary.setdefault(expense.category, {})
            summary[expense.category].setdefault(description, 0.00)
            summary[expense.category][description] += expense.debit

        return summary

class UserInterface():
    '''Display component for the program'''
    def __init__(self):
        self.calculator = BudgetCalculator()

    def format_sunburst_data(self):
        '''Pull data from the calculator and format for sunburst'''

        summary = self.calculator.category_reduction()
        summary_expense = self.calculator.expense_reduction()
        total_cost = sum(summary.values())

        # Start of list
        parent = ["Total Cost",]
        child  = ["",]
        values = [total_cost]

        # Next, display categories with cost, parent is total cost
        for category, cost in summary.items():
            parent.append(category)
            child.append(parent[0])
            values.append(cost)

        # Finally, display expenses with category as parent
        for category, dic in summary_expense.items():
            for description, cost in dic.items():
                parent.append(description)
                child.append(category)
                values.append(cost)

        # Display the sun graph
        fig = go.Figure(go.Sunburst(
            labels=parent,
            parents=child,
            values=values,
        ))

        fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
        fig.show()

    def generate_pie(self):
        '''Given the categories and amounts, generate a pie graph'''

        summary = self.calculator.category_reduction()

        category_list = list(summary.keys())
        cost_list = list(summary.values())
        title = f'Statement Overview: {sum(summary.values())}'

        # Create the dataframe
        df = pl.DataFrame(
            {
                'Category' : category_list,
                'Cost'     : cost_list
            }
        )

        fig = px.pie(df, values='Cost', names='Category', title=title)
        fig.show()


if __name__ == '__main__':
    # Create UserInterface
    y = UserInterface()
    y.format_sunburst_data()

