from enum import Enum  

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