import sys
import os
import numpy as np
import pandas as pd

# Add the 'src' folder to the sys.path so Python can find the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from print_data import print_data


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


test_print_data()