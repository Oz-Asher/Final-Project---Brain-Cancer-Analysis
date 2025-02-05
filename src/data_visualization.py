import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
import random

class DataVisualization:
    """
    This class uses the data of the allele's expression  
    in each brain tumor and plots it to the user. 
    """
    
    def __init__(self, data, df, num_for_plot = 5, corr_threshold = 0.7):
        """
        Initializes the class and prepares data for visualization.

        Args: 
           data (DataFrame) - Modified df as it contains solely the mean expression of each 
                              allele that had a significant effect over the normal tissue

           df (DataFrame)- Consists of the raw data of the file.

           num_for_plot (int) - The number of top alleles that we allow to be plotted for each tumor.
                                Can only be a natural number. If no value is used then baseline is 5.

           corr_threshold (float) - Threshold for determining significant correlations. If no value is 
                                    used then baseline value is 0.7.
        """

        self.data = data
        self.df = df
        self.num_for_plot = num_for_plot
        self.corr_threshold = corr_threshold
        
        # In case the programmer has inserted an invalid value for num_for_plot
        if type(self.num_for_plot) is not int or self.num_for_plot < 2:
            self.num_for_plot = 5
            print('\nInserted value of desired number of alleles to be plotted is invalid. Baseline value (5) was used instead.')


        # In case the programmer has inserted an invalid value for corr_threshold
        if type(self.corr_threshold) is not float or abs(self.corr_threshold) > 1:
            self.corr_threshold = 0.7
            print('\nInserted value of threshold for correlation was invalid. Baseline value (0.7) was used instead.')
        
        # A list containing all the different alleles in the dataset. 
        self.alleles = df.columns[2:]

        # A list containing the types of each brain tumor. 
        self.cancer_type = list(df['type'].unique())

        # Contains the mean expression (in values) for each allele (in keys) in the healthy tissue.
        self.normal_means = df[df['type'] == 'normal'][self.alleles].mean().to_dict() # Converts the variable into a dict.

        self.user_interface() # Run the interface with the user.


    def user_interface(self):
        """
        Providing user interface for allele and tumor analysis.
        The program asks the user to type either one of three options: 

        1. The name of the allele (which will execute analyze_allele_expression).
        2. The name of the tumor (which will execute analyze_tumor).
        3. 'Exit', which simply ends the program. 
        """
        while True:  # The program will run perpetually until we tell it to stop (by typing 'exit').

            print("\nTissues available:", ", ".join(self.cancer_type))
            random_alleles = random.sample(list(self.alleles), self.num_for_plot) # Randomly select num_for_plot alleles.
            print("Example of available genes:", ", ".join(random_alleles))

            # Get user's choice for analysis.
            allele_or_tumor = input("\nEnter allele, tumor type, or 'exit' to quit: ").strip().lower()

            if allele_or_tumor in self.alleles: # If the user has inserted an allele to the program.
                self.analyze_allele_expression(allele_or_tumor)

            elif allele_or_tumor in self.cancer_type: # If the user has inserted a type of cancer to the program.
                self.analyze_tumor(allele_or_tumor)

            elif allele_or_tumor == 'exit': # If the user wants to end the program. 
                os.system('cls') # Clears the terminal. 
                sys.exit() # Exit the program. 

            else: # If the user types something unfamiliar to the program.
                print("\nInvalid choice. Please try again.")
                self.user_interface() # Running the program again to give the user another chance to type something relevant. 


    # Reclled from user_interface() based on user's dicision.
    def analyze_allele_expression(self, allele):
        """
        Analyzes a specific allele's expression levels across tumor types.

        Args: 
            allele (str) - The name of the allele the user has inserted to the program.
        """

        os.system('cls') # Clears the terminal. 

        # Find tumor types where the allele expression is available (i.e., no values of NaN).
        tumors_with_allele = self.data[allele].dropna().index # dropna() is used to include only data without NaN. 
                                                            # index() is used in order to include only the names of the tumors.
                                                            # (which is the index in that case) and exclude the level of expression. 

        tumors_with_allele = tumors_with_allele[tumors_with_allele != 'normal'] # Exclude 'normal' type.

        # Check if the allele is present in any tumor types. If not, then it will call main() again and will start over.
        if tumors_with_allele.empty: 
            print(f"Allele '{allele}' is not significant in any tumor types.")
            self.user_interface() # Call the main function if the allele is not found in any tumor.


        # Printing a subtitle for which alleles are we analysing.
        print(f"Analysis for allele '{allele}':\n")

        # Loop through each tumor type where the allele is present and analyze the expression level compared to the healthy tissue. 
        for tumor_type in tumors_with_allele:
            tumor_expression = self.data.loc[tumor_type, allele] # Retrieve the tumor expression value for the allele from data. 

            # Calculate and print the difference in expression between the tumor and normal tissue.
            print(f"Tumor Type: {tumor_type}, Tumor Expression: {round(tumor_expression, 3)}, "
                  f"It is different than the healthy tissue by: {round((tumor_expression / self.normal_means[allele]) * 100 , 3)}%.")

        # Describe the allele's data to get a statistical summary (mean, std, etc.).
        allele_data = self.df[allele]
        print(allele_data.describe())

        # Plotting the distribution of allele expression.
        plt.figure(figsize=(10, 5))
        sns.histplot(allele_data, kde=True, color='blue') # Generate a histogram with a KDE curve.
        plt.title(f"Distribution of Expression Levels for allele: {allele}") 
        plt.xlabel("Expression Level")  
        plt.ylabel("Frequency")  
        plt.show()


    # Reclled from user_interface() based on user's dicision.
    def analyze_tumor(self, tumor_type):
        """
        Analyzes a specific tumor type and creates graphs for allele expression and correlation.
        Shows the top alleles with the most difference from their normal expression.

        Args: 
            tumor_type (str) - The name of the cancer the user has inserted to the program.
        """

        os.system('cls') # Clears the terminal. 
        
        # Retrieve the allele expression data for the specified tumor type (typed by the user).
        tumor_allele_data = self.data.loc[tumor_type].dropna() # Excludes all values of NaN.

         # Contains the absolute difference in expression between tumor and normal tissues.
        differences = {allele: abs(tumor_allele_data[allele] - self.normal_means[allele]) for allele in tumor_allele_data.index}

         # Get the top alleles with the largest expression differences. 
        top_alleles = sorted(differences, key=differences.get, reverse=True)[:self.num_for_plot]


              # Create a bar plot comparing tumor vs normal expression levels for the top alleles.
        
        expression_data = [] # List to store expression values.
        labels = [] # List to store allele labels.

        for allele in top_alleles:
            # Add tumor and normal expression values to the data for plotting.

            # In both expression_data and labels, extend is used in order to insert the data of the tumor and normal 
            # one after another. So for example if the expression data for the normal tissue is [1,2,3] and the sick 
            # tissue is [4,5,6], then the new list shall be: [1,4,2,5,3,6].
            expression_data.extend([tumor_allele_data[allele], self.normal_means[allele]])
            labels.extend([f'{allele}\nTumor', f'{allele}\nNormal'])
        
        if tumor_type != 'normal': # No need to plot results if the tissue is normal. 
            plt.figure(figsize=(10, 6))

            # Plot bars for tumor and normal expression levels.
            bars = plt.bar(range(len(expression_data)), expression_data) # First variable includes the range of how many different levels of expression we have (both normal and sick).
                                                                    # Second variable includes the data of the expression for both the sick and normal.
           
            # Coloring the bars according to whether they are sick or normal. 
            for i in range(0, len(bars), 2): # The jumps of 2 are necessary for only that way we will color a different bar each new iteration.

                bars[i].set_color('royalblue') # Set color for tumor bars.
                bars[i+1].set_color('lightgreen') # Set color for normal bars.
            
            # Plotting the results. 
            plt.xticks(range(len(labels)), labels, rotation=45) # Customize x-axis labels and rotating them 45 degrees.
            plt.title(f"Top {self.num_for_plot} Alleles with Most Difference in Expression for {tumor_type}")  
            plt.ylabel("Expression Level")  
            plt.tight_layout() # Adjust layout to prevent overlap for aesthetic reasons.
        

            # Create a heatmap to visualize correlations among the top alleles in the tumor type.

        correlation_data = self.df[self.df['type'] == tumor_type][top_alleles].corr() # Compute correlation matrix.

        if (len(top_alleles) >= 2 and # Must be at least two in order to show correlation between at least two alleles. 
             np.any(np.isfinite(correlation_data))):# Verifying whether there are correlation values at all.
                                                    #isfinite() checks for valid numeric values (excluding NaN or Inf).
            
            """
            Printing to the user the alleles who have a significant correlation 
            between one another in the formation of the tumor:
            """

            # Create a copy of the correlation matrix
            corr_lower = correlation_data.copy()

            # Apply a mask to keep only the lower triangle and remove the diagonal.
            corr_lower.values[np.triu_indices_from(corr_lower)] = np.nan

            # Extract components with correlation >= 0.4.
            significant_pairs = corr_lower[abs(corr_lower) >= self.corr_threshold].stack().index.tolist()

            # Get unique component names.
            list_corr = list(set([item for sublist in significant_pairs for item in sublist]))
            
            if len(list_corr) > 0 and tumor_type != 'normal':
                print(f"\nMost significant alleles that are highly correlated in the formation of {tumor_type}:\n")

                for allele in list_corr:
                    print(f"{allele} - Changed expression from normal by {round((tumor_allele_data[allele] / self.normal_means[allele])*100, 3)}%")
            
            elif tumor_type == 'normal':
                pass
            
            else:
                print("\nAlthough some alleles were found to be expressed significantly more or less compared to control,")
                print(f"no set of alleles were found to have a significantly correlated expression pattern in {tumor_type}.")



                 # Plotting the full (unfiltered) correlation results. 

            plt.figure(figsize=(8, 6))
            sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0) # Plot heatmap.
            plt.title(f"Allele Correlation Heatmap - {tumor_type}") # Set heatmap title.
            plt.tight_layout() # Adjust layout to prevent overlap for aesthetic reasons.

        else:
            print(f'\nNot enough data in excel file to show correlation between alleles in {tumor_type}.')
        
        plt.show()
        os.system('cls') # Clears the terminal. 