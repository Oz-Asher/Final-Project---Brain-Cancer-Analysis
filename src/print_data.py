"""
Prints the data after statistical analysis (Optional). No imports are required. 
"""

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