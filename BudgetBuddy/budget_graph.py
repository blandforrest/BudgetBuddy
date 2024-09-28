import pandas as pd
import logging
import re
from plotly import graph_objects as go

__all__ = ['BudgetGraph']

class BudgetGraph():

    def __init__(self, file_path : str) -> None:
        self.file_path = file_path
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def clean_str(text : str):
        ''' Remove symbols, numbers, common text from str '''
        clean_text = re.sub(r'[^a-zA-Z\s]', '', text) \
            .replace('TST', '').replace('SQ', '')
    
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()

        return clean_text

    def display_graph(self) -> None:
        parent, child, values = self.parse_data()
        self.generate_graph(parent, child, values)

    def parse_data(self) -> (list, list, list):
        ''' Massage data for graphing '''
        try:
            input_df = pd.read_csv(self.file_path)
        except FileNotFoundError as ex:
            self.logger.error(f"Exception while loading file {ex}")
            sys.exit(1)
    
        reduced_df = input_df[['Description', 'Category', 'Debit']]

        # Remove numbers and symbols from description
        reduced_df['Description'] = reduced_df['Description'].apply(self.clean_str)

        # Summarize costs by category
        category_sum_df = reduced_df.groupby('Category')['Debit'].sum().reset_index()
        description_sum_df = reduced_df.groupby(['Description', 'Category'], as_index=False)['Debit'].sum()
        total_cost = category_sum_df['Debit'].sum()

        # Create lists for graph
        total_cost_str = f'Total Cost: {total_cost}'
        parent = [total_cost_str] + category_sum_df['Category'].tolist() + description_sum_df['Description'].tolist()
        child = ["",] + ([total_cost_str] * len(category_sum_df.index)) + description_sum_df['Category'].tolist()
        values = [total_cost] + category_sum_df['Debit'].tolist() + description_sum_df['Debit'].tolist()

        self.logger.info("Successfully parsed data!")
        return parent, child, values

    def generate_graph(self, parent : list, child : list, values : list) -> None:
        ''' Display data in graph '''
        self.logger.info("Displaying graph!")
        fig = go.Figure(go.Sunburst(
        labels=parent,
        parents=child,
        values=values))
    
        fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
        fig.show()
