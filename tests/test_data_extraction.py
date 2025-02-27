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

    try:
        result = import_data(csv_name)
        
        # Check if the function returned what we expect
        if result is None:
            print("\nTEST CONCLUSION: import_data correctly handled missing filename.")
        else:
            print("\nTEST CONCLUSION: Unexpected output from import_data.")

    except Exception as e:
        print(f"\nTEST CONCLUSION: import_data failed with error: {e}")


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
 
    try:
        data = clean_data(df)

        # Check if the function returned a DataFrame
        if isinstance(data, pd.DataFrame):
            print("\nTEST CONCLUSION: clean_data produced a valid DataFrame output.")
        else:
            print("\nTEST CONCLUSION: clean_data returned an empty or incorrect DataFrame.")

    except Exception as e:
        print(f"\nTEST CONCLUSION: clean_data failed with error: {e}")



    print('\n\\\\\\\\\\\\\\\\\\ clean_data() Test 2')

    # Example when df is empty:
    df = pd.DataFrame({})

    try:
        data = clean_data(df) 

        if data is None:
            print("\nTEST CONCLUSION: clean_data correctly handled an empty DataFrame.")
        else:
            print("\nTEST CONCLUSION: clean_data should return an empty DataFrame but didn't.")

    except Exception as e:
        print(f"\nTEST CONCLUSION: clean_data failed with error: {e}")


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


    try:
        print_data(data)
        print("\nTEST CONCLUSION: print_data ran successfully without errors.")

    except Exception as e:
        print(f"\nTEST CONCLUSION: print_data failed with error: {e}")



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

    try:
        print_data(data)
        print("\nTEST CONCLUSION: print_data ran successfully with varied data.")

    except Exception as e:
        print(f"\nTEST CONCLUSION: print_data failed with error: {e}")



    print('\n\\\\\\\\\\\\\\\\\\ print_data() Test 3')

    data = pd.DataFrame({})

    try:
        print_data(data)
        print("\nTEST CONCLUSION: print_data ran successfully on an empty DataFrame.")

    except Exception as e:
        print(f"\nTEST CONCLUSION: print_data failed with error: {e}")



test_import_data()
test_clean_data()
test_print_data()
