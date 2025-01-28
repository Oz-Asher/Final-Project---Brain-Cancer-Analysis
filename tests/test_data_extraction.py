import sys
import os
import numpy as np
import pandas as pd

# Add the 'src' folder to the sys.path so Python can find the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_extraction import import_data, clean_data 



def test_data_exctraction():

    print('\n\\\\\\\\\\\\\\\\\\ import_data() Test')

    # Example of csv_name
    csv_name = None

    import_data(csv_name) # Test

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


test_data_exctraction()