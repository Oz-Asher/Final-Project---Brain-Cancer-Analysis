from scipy.stats import f_oneway
import pandas as pd
import os
import numpy as np
import sys

"""
This code extract data from a CSV file (named csv_name) and  
uses statistical methods  to clean and modify the data. 
"""

# First function used in main.py
def import_data(csv_name):

    """
    This function imports the data from the excel file and creates a variable that contains it (df).

    Args:
        csv_name (str) - The name of the CSV file. 

    Return:
        df (DataFrame)- Consists of the raw data of the file. 
    """
    

    # The directory of the file in which our code is placed. 
    file_directory = os.getcwd()

    # The directory of the excel we were using.
    excel_directory = f"{file_directory}\{csv_name}.csv"
   
    # Load the CSV file.
    try:
        # Data of the excel file. 
        df = pd.read_csv(excel_directory)
        print("\nCSV file loaded successfully.")

        return df

    except FileNotFoundError: # If the excel file is not in the same directory as the code. 
        print(f"\nError: File {csv_name} not found. Ensure the file is in the correct directory.")

    except Exception as e: # General error. 
        print(f"\nAn error occurred while loading the CSV file: {e}")

    
# Second function used in main.py
def clean_data(df, critical_alpha = 0.01):

    """
    Uses statistical methods (ANOVA) to drop out all the expression values in df that 
    do not have a significant effect compared to the healthy tissue (used as control). 

    Args:
        df (DataFrame) - Consists of the raw data of the file.  

        critical_alpha (float) - Significance threshold for identifying significant alleles. 
                                 Can be somewhere between 0 and 1. 
                                 If the user has not inserted a value for it or an invalid one,
                                 baseline value shall be o.o1.

    Return:
        data (DataFrame) - Modified df as it contains solely the mean expression of each 
                           allele that had a significant effect over the normal tissue.

    """

    if df.empty: # If excel file is empty. 
        print('\nCSV file is empty. Please add info.')
        sys.exit()

    if type(critical_alpha) is not float or (critical_alpha >= 1 or critical_alpha <= 0): # In case critical alpha is not valid. 
        critical_alpha = 0.01
        print('\nInserted value of critical alpha is invalid. Baseline value (0.01) was used instead.')


    # A dictionary that stores alleles (in values) that have a significant effect for each tumor type (in keys).
    dict_alleles = {} # (Stores the mean values for each significant allele).

    # A list containing the types of each brain tumor. 
    cancer_type = list(df['type'].unique()) # unique() is used to refer to each tumor only once. 
    
    for tumor in cancer_type:

        # Get data for the current tumor type and normal type so we will be able to contrast them later in the ANOVA. 
        # Both lines of code extract allele expression using .values and skipping the first two columns of the excel.
        tumor_data = df[df['type'] == tumor].iloc[:, 2:].values 
        normal_data = df[df['type'] == 'normal'].iloc[:, 2:].values                                                      

        
        if len(tumor_data) > 1: # Making sure there is more than one sample for tumor for the ANOVA.

            # Calculating F and P value using ANOVA. Comparing the healthy and sick tissues (thus using normal_data as a control group).
            f_statistics, p_values = f_oneway(tumor_data, normal_data) 

        else:
            print(f'\nNot enough samples for {tumor}. Please insert more data into the excel file.')
            continue # Start over. 
        

        # Filter significant alleles based on critical alpha storing their index.
        indexes = np.where(p_values < critical_alpha)  


        # A list containing all the different alleles in the dataset. 
        alleles = df.columns[2:] # Skips the first two columns. 
  

        if tumor != 'normal': # If the tumor is not normal (i.e. the brain is not healthy).

            # Adding the unhealthy tumor expression values.
            dict_alleles[tumor] = {allele: # The name of the allele (as keys).
                                    df.loc[df['type'] == tumor, allele].mean() # Locating the mean value of 'allele' in 'tumor' (as values).
                                    for allele in alleles[indexes]} # Iterating 'allele' as through all the significant expressions.


        else: # If the tumor is normal (i.e. the brain is healthy).
            
            # Adding the normal expression values.
            dict_alleles[tumor] = {allele: # The name of the allele (as keys).
                                    df.loc[df['type'] == tumor, allele].mean() # Locating the mean value of 'allele' in 'tumor' (as values).
                                    for allele in alleles} # Iterating 'allele' as through all the possible expressions.
  
    # Converting dict_alleles into a dataframe.
    data = pd.DataFrame.from_dict(dict_alleles, orient='index') 
    
    return data


# Optional
def print_data(data):

    """
    This function prints the entire data from the excel after the statistical analysis.

    Args:
        data (DataFrame) - Contains the mean expression of each allele that 
                           had a significant effect over the normal tissue.
    """

    if data.empty:
        print('\nNo data recieved.')

    for tumor, row in data.iterrows():# Iterate over the DataFrame rows and print the formatted output.
        if tumor != 'normal':
            
            print(f"Tumor: {tumor}.")  # Print the tumor type.

            allele_num = len(row.dropna()) 
            print(f"Number of alleles having a significant play: {allele_num}")  # Print the total count of significant alleles.

            allele_list = ', '.join(f"'{allele}'" for allele in row.dropna().index)  # Get the list of alleles with non-NaN values.

            if allele_num > 0:
               print(f"Significant alleles: {allele_list}\n")  # Print the list of significant alleles.
            else:
                print()