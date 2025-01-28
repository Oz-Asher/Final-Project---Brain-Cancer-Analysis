
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
import random

"""
This code uses the data of the allele's expression  
in each brain tumor and plots it to the user. 
"""

# First function being used. Recalled from main.py.
def data_visualization(data_, df_, num_for_plot_ = 5): 
    """
    This is the main function that takes all of the necessary variables from previous functions
    and makes them global so that all of the other functions in this code will be able to use them.
    It also creates new variables that will be used in the rest of the functions.
    Then it runs user_interface().

    Args: 
       data_ (DataFrame) - Modified df as it contains solely the mean expression of each 
                           allele that had a significant effect over the normal tissue

       df_ (DataFrame)- Consists of the raw data of the file.

       num_for_plot_ - The number of top alleles that we allow to be plotted for each tumor.
                       Can only be a natural number. If no value is used then basline is 5.

    """
     
    global data, df, alleles, cancer_type, num_for_plot, normal_means
    data, df, num_for_plot = data_, df_, num_for_plot_

    if type(num_for_plot) is not int or num_for_plot < 2:
        num_for_plot = 5
        print('\nInserted value of desired number of alleles to be plotted is invalid. Baseline value (5) was used instead.')

    # A list containing all the different alleles in the dataset. 
    alleles = df.columns[2:] # Skips the first two since in the excel file they do not contain names of alleles.

    # A list containing the types of each brain tumor. 
    cancer_type = list(df['type'].unique()) # unique() is used to refer to each tumor only once. 

    # Contains the mean expression (in values) for each allele (in keys) in the healthy tissue.
    normal_means = df[df['type'] == 'normal'][alleles].mean().to_dict() # Converts the variable into a dict.

  
    user_interface() # Run the interface with the user.
 

# Second function being used. Retrieved from data_visualization().
def user_interface():
    """
    Providing user interface for allele and tumor analysis.
    The program asks from the user to type either one of three options: 

    1. The name of the allele (which will execute analyze_allele_expression).
    2. The name of the tumor (which will execute analyze_tumor).
    3. 'Exit', which simply ends the program. 
    """

    while True: # The program will run perpetually until we tell it to stop (by typing 'exit').

       
        print("\nTissues available:", ", ".join(cancer_type))
        random_alleles = random.sample(list(alleles), num_for_plot)  # Randomly select num_for_plot alleles.
        print("Example of available genes:", ", ".join(random_alleles))

        # Get user's choice for analysis.
        allele_or_tumor = input("\nEnter allele, tumor type, or 'exit' to quit: ").strip().lower() # strip() is used to cut off spaces. 
                                                                                    # lower() is used in case the user uses uppercase letters.

        if allele_or_tumor in alleles: # If the user has inserted an allele to the program.
            analyze_allele_expression(allele_or_tumor)

        elif allele_or_tumor in cancer_type: # If the user has inserted a type of cancer to the program.
            analyze_tumor(allele_or_tumor)

        elif allele_or_tumor == 'exit': # If the user wants to end the program. 
            os.system('cls') # Clears the terminal. 
            sys.exit()  # Exit the program. *It was used instead of break since it breaks the whole program entierly, rather then a specific function.

        else: # If the user types something unfamiliar to the program.
            print("\nInvalid choice. Please try again.") 
            user_interface() # Running the program again to give the user another chance to type something relevant. 


# Reclled from user_interface() based on user's dicision.
def analyze_allele_expression(allele):
    
    """
    Analyzes a specific allele's expression levels across tumor types.
    This def function will print by how much this particular allele is expressed more or less in each type
    of cancer that had touted a significant expression for this allele compared to the healthy tissue. 
    Moreover it will print general data on the allele (like mean, std, min and max) and the distribution 
    of its expression level. 

    Args: 
        allele (str) - The name of the allele the user has inserted to the program.
    """

    os.system('cls') # Clears the terminal. 

    # Find tumor types where the allele expression is available (i.e., no values of NaN).
    tumors_with_allele = data[allele].dropna().index # dropna() is used to include only data without NaN. 
                                                    # index() is used in order to include only the names of the tumors.
                                                    # (which is the index in that case) and exclude the level of expression. 
    tumors_with_allele = tumors_with_allele[tumors_with_allele != 'normal'] # Exclude 'normal' type.

    # Check if the allele is present in any tumor types. If not, then it will call main() again and will start over.
    if tumors_with_allele.empty: # Either True or Flase. 
        print(f"Allele '{allele}' is not significant in any tumor types.")
        user_interface() # Call the main function if the allele is not found in any tumor.


    # Printing a subtitles for which alleles are we analysing. 
    print(f"Analysis for allele '{allele}':\n")  

    # Loop through each tumor type where the allele is present and analyze the expression level compared to the healthy tissue. 
    for tumor_type in tumors_with_allele:
        tumor_expression = data.loc[tumor_type, allele]  # Retrieve the tumor expression value for the allele from data. 

        # Calculate and print the difference in expression between the tumor and normal tissue.
        print(f"Tumor Type: {tumor_type}, Tumor Expression: {round(tumor_expression, 3)}, "
            f"It is different than the healthy tissue by: {round((tumor_expression / normal_means[allele]) * 100 , 3)}%.")

    # Describe the allele's data to get a statistical summary (mean, std, etc.).
    allele_data = df[allele]
    print(allele_data.describe())
    
    # Plotting the distribution of allele expression.
    plt.figure(figsize=(10, 5))
    sns.histplot(allele_data, kde=True, color='blue')  # Generate a histogram with a KDE curve.
    plt.title(f"Distribution of Expression Levels for allele: {allele}")  
    plt.xlabel("Expression Level")  
    plt.ylabel("Frequency")  
    plt.show()  


# Reclled from user_interface() based on user's dicision.
def analyze_tumor(tumor_type):
    """
    Analyzes a specific tumor type and creates graphs for allele expression and correlation.
    Shows the top alleles with the most difference from their normal expression.

    Args: 
        tumor_type (str) - The name of the cancer the user has inserted to the program.
    """

    os.system('cls') # Clears the terminal. 
    
    # Retrieve the allele expression data for the specified tumor type (typed by the user).
    tumor_allele_data = data.loc[tumor_type].dropna()  # Excludes all values of NaN.
  
    differences = {} # Contains the absolute difference in expression between tumor and normal tissues.

    # Iterate through all the alleles in our selected tumor.
    for allele in tumor_allele_data.index: # index gets the names of the alleles rather than their level of expression. 

        # Inserting the absolute difference into the dict's values and the name of the allele as its keys. 
        differences[allele] = abs(tumor_allele_data[allele] - normal_means[allele]) 

    # Get the top alleles with the largest expression differences.
    top_alleles = sorted(differences, key=differences.get, reverse=True)[:num_for_plot]



        # Create a bar plot comparing tumor vs normal expression levels for the top alleles.

    expression_data = []  # List to store expression values.
    labels = []  # List to store allele labels.
    for allele in top_alleles:
        # Add tumor and normal expression values to the data for plotting.

        # In both expression_data and labels, extend is used in order to insert the data of the tumor and normal 
        # one after another. So for example if the expression data for the normal tissue is [1,2,3] and the sick 
        # tissue is [4,5,6], then the new list shall be: [1,4,2,5,3,6].
        expression_data.extend([tumor_allele_data[allele], normal_means[allele]])
        labels.extend([f'{allele}\nTumor', f'{allele}\nNormal']) 

    if tumor_type != 'normal': # No need to plot results if the tissue is normal. 

        plt.figure(figsize=(10, 6)) # Figuring the plot. 

        # Plot bars for tumor and normal expression levels.
        bars = plt.bar(range(len(expression_data)), expression_data) # First variable includes the range of how many different levels of expression we have (both normal and sick).
                                                                    # Second variable includes the data of the expression for both the sick and normal.

        # Coloring the bars according to whether they are sick or normal. 
        for i in range(0, len(bars), 2): # The jumps of 2 are necessary for only that way we will color a different bar each new iteration.

            bars[i].set_color('royalblue')  # Set color for tumor bars.
            bars[i+1].set_color('lightgreen')  # Set color for normal bars.

        # Plotting the results. 
        plt.xticks(range(len(labels)), labels, rotation=45) # Customize x-axis labels and rotating them 45 degrees.
        plt.title(f"Top {num_for_plot} Alleles with Most Difference in Expression for {tumor_type}")  
        plt.ylabel("Expression Level")  
        plt.tight_layout() # Adjust layout to prevent overlap for aesthetic reasons.
        

       # Create a heatmap to visualize correlations among the top alleles in the tumor type.

    correlation_data = df[df['type'] == tumor_type][top_alleles].corr() # Compute correlation matrix.
 
    if (len(top_alleles) >= 2 # Must be at least two in order to show correlation between at least two alleles. 
        and np.any(np.isfinite(correlation_data))): # Verifying whether there are correlation values at all.
                                                    #isfinite() checks for valid numeric values (excluding NaN or Inf).
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0)  # Plot heatmap.
        plt.title(f"Allele Correlation Heatmap - {tumor_type}")  # Set heatmap title.
        plt.tight_layout()  # Adjust layout to prevent overlap for aesthetic reasons.
         
    else:
        print(f'\nNot enough data in excel file to show correlation between alleles in {tumor_type}.')

    plt.show() 

