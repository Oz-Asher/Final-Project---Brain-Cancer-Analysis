import sys
import os
import numpy as np
import pandas as pd

# Add the 'src' folder to the sys.path so Python can find the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_extraction import import_data, clean_data, print_data


def test_import_data():

    print('\n\\\\\\\\\\\\\\\\\\ import_data() Test')

    # Example of csv_name
    csv_name = None

    import_data(csv_name) # Test


def test_clean_data():

    print('\n\\\\\\\\\\\\\\\\\\ clean_data() Test 1')

    # Example of df
    df = {
    "samples": [  834,          835,          836,            837,                   838], 
    "type": ["ependymoma", "glioblastoma", "normal", "pilocytic_astrocytoma", "medulloblastoma"],
    "1007_s_at": [12,           15,          15,               9,                     10],
    "1053_at": [  5,            6,            7,               8,                     9],
    "117_at": [   10,           11,          12,               13,                    14],
    }

    df = pd.DataFrame(df)
   
    # Example of critical_alpha
    critical_alpha = 0.01

    data = clean_data(df, critical_alpha) # Test
    print('\n', data)


    print('\n\\\\\\\\\\\\\\\\\\ clean_data() Test 2')

    # Example when df is empty:
    df = {}
    df = pd.DataFrame(df)
    data = clean_data(df, critical_alpha) # Test
    print('\n', data)


def test_print_data():
    
    print('\n\\\\\\\\\\\\\\\\\\ print_data() Test 1')

    # Example of data
    data = {
    'type': ["ependymoma", "glioblastoma", "normal", "pilocytic_astrocytoma", "medulloblastoma"],
    "1007_s_at": [None,         None,           15,               None,                None],
    "1053_at": [  None,         None,            7,               None,                None],
    "117_at": [   None,         None,           12,               None,                None],
    }
    
    data = pd.DataFrame(data)
    
    # Removes the title 'types' from data.
    data.columns.values[0] = ''
    data.set_index('', inplace=True)


    print_data(data)


    print('\n\\\\\\\\\\\\\\\\\\ print_data() Test 2')

    # Example of data
    data = {
    'type': ["ependymoma", "glioblastoma", "normal", "pilocytic_astrocytoma", "medulloblastoma"],
    "1007_s_at": [1000,          4,           15,                4,                None],
    "1053_at": [  None,         None,            7,               30,                40],
    "117_at": [   23,         None,           12,               32,                None],
    }
    
    data = pd.DataFrame(data)
    
    # Removes the title 'types' from data.
    data.columns.values[0] = ''
    data.set_index('', inplace=True)


    print_data(data)


    print('\n\\\\\\\\\\\\\\\\\\ print_data() Test 3')

    data = pd.DataFrame({})
    print_data(data)


test_import_data()
test_print_data()
test_clean_data()
