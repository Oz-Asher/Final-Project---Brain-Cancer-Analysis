import sys
import os
import pandas as pd

# Add the 'src' folder to the sys.path so Python can find the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_visualization import DataVisualization 


def test_DataVisualization():

    print('\n\\\\\\\\\\\\\\\\\\ DataVisualization() Test')

    # Example of df
    df = {
    "samples": [  834,          835,          836,            837,                   838], 
    "type": ["ependymoma", "glioblastoma", "normal", "pilocytic_astrocytoma", "medulloblastoma"],
    "1007_s_at": [12,           15,          15,               9,                     10],
    "1053_at": [  5,            6,            7,               8,                     9],
    "117_at": [   10,           11,          12,               13,                    14],
    }


    # Example of data
    data = {
    'type': ["ependymoma", "glioblastoma", "normal", "pilocytic_astrocytoma", "medulloblastoma"],
    "1007_s_at": [None,       15,           15,               9,                    10],
    "1053_at": [  5,            6,            7,               None,                9],
    "117_at": [   10,           11,           12,               13,                None],
    }
    
    
    df = pd.DataFrame(df)
    data = pd.DataFrame(data)
    
    # Removes the title 'types' from data.
    data.columns.values[0] = ''
    data.set_index('', inplace=True)

    num_for_plot = 2
    

    # Ensure no errors during plotting
    DataVisualization(data, df, num_for_plot)


test_DataVisualization()
