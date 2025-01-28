#main.py: Entry point for the project

from src.data_extraction import import_data, clean_data
from src.print_data import print_data
from src.data_visualization import data_visualization


def main():

    '''
    This is the main function of the project. It first defines some essential variables  
    that'll be used later on throughout the code and then runs the functions. 
    '''

           # Initializing Important Variables: 

    csv_name = "Brain_GSE50161" # Name of the CSV file.

    # Significance threshold for identifying significant alleles.
    critical_alpha = 0.01 # Can be somewhere between 0 and 1.
    
    # The number of top alleles that we allow to be plotted for each tumor.
    num_for_plot = 5 # Can only be a natural number. 
    


                    # Running The Code:

    # Load data from CSV file.
    df = import_data(csv_name) #Ensure csv_name is in the correct directory.

    # Modified data after statistical analysis. 
    data = clean_data(df, critical_alpha)
    
    # print_data(data) # Optional. 

    # Visualising data of the excel using user interface. 
    data_visualization(data, df, num_for_plot)


if __name__ == "__main__":
    main()
