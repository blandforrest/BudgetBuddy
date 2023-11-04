import pytest
from BudgetBuddy.Parser import Parser

# Create a single instance of the parser
parser = Parser()

# Tests for str_to_float
def test_str_to_float_correct():
    '''Valid data in, verify output'''
    assert Parser.str_to_float('1.0') == 1.0

def test_str_to_float_negative_correct():
    '''Valid negative data in, verify output'''
    assert Parser.str_to_float('-46.0') == -46.0

def test_str_to_float_empty_string():
    '''Empty string data in, verify output'''
    assert Parser.str_to_float('') == 0.0

def test_str_to_float_string_input():
    '''Invalid string data in, verify exception'''
    with pytest.raises(ValueError):
        assert Parser.str_to_float('abc123')

def test_str_to_float_string_input2():
    '''Invalid string data in, verify exception'''
    with pytest.raises(ValueError):
        assert Parser.str_to_float('123abc')

# Tests for clean_description
def test_clean_description_good_input1():
    '''Valid string data, verify cleaned string'''
    assert Parser.clean_description('PUBLIX #1234') == 'PUBLIX'

def test_clean_description_good_input2():
    '''Valid string data, verify cleaned string'''
    assert Parser.clean_description('12356WINN DIXIE235') == 'WINN DIXIE'

def test_clean_description_good_input3():
    '''Valid string data, verify cleaned string'''
    assert Parser.clean_description('$PAPPA *JOHNS #1235') == 'PAPPA JOHNS'

def test_clean_description_input4():
    '''Valid string data, verify cleaned string'''
    assert Parser.clean_description('12356WINN DIXIE235') == 'WINN DIXIE'

def test_clean_description_empty_string():
    '''Empty string data, verify cleaned string'''
    assert Parser.clean_description('') == ''

def test_clean_description_none():
    '''None string data, verify cleaned string'''
    assert Parser.clean_description(None) == ''

def test_clean_description_bad_string():
    '''Odd string data, verify cleaned string'''
    assert Parser.clean_description('dfgaoduih436') == 'dfgaoduih'

def test_clean_description_bad_spaces():
    '''Spaced out string data, verify cleaned string'''
    assert Parser.clean_description('\t   dfgaoduih436   \t') == 'dfgaoduih'