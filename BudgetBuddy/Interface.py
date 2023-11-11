import plotly.express as px
import polars as pl
from plotly import graph_objects as go
import logging

class Interface():
    '''Display component for the program'''
    def __init__(self, calculator):
        self.calculator = calculator
        self.logger     = logging.getLogger('BudgetBuddy.Interface')


    def generate_sunburst_data(self):
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

        self.logger.debug('Displaying Graph!')
        fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
        fig.show(renderer='iframe')


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