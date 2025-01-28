Advanced Python for Neuroscience - Brain Cancer Gene Expression Analysis

Project Overview

This project focuses on analyzing gene expression in different types of brain cancer. 
The main research question is to identify which genes are involved in each type of brain 
tumor and the percentage of expression of a specific gene in each type of tumor when  
compared to healthy tissue. The project allows users to input either a gene or cancer data
type to get information about their expression levels and relevant tumor data.

The data used in this project is from the Brain_GSE50161 dataset, which includes gene 
expression levels for several types of brain cancers. The dataset is in CSV format,
containing gene expression percentages and other relevant information for four types of cancer.

Ensure that you have the Brain_GSE50161.csv file in the appropriate directory.


Key Functionalities:
- Gene and Cancer Type Analysis: Find dominant genes involved in specific types of brain cancer and their expression
                                 percentages in comparison to healthy tissue including other statistical info.

- User Interaction: The program allows the user to input a gene or cancer type and get detailed 
                    data about expression levels and dominant alleles in the cancer types.

- Data Visualization: The project can visualize the gene expression data using various plots.


Folder Structure

The project directory is structured as follows:

Project/
│
├── main.py                      # Main entry point of the project.
│                    
├── src/                         # Contains the core functionality modules.
│   ├── data_extraction.py       # Extracts data from the Brain_GSE50161 CSV file.
│   ├── print_data.py            # (Optional) Prints statistical analysis results of the data.
│   └── data_visualization.py    # Visualizes data using plots.
│
├── tests/                       # Contains test cases for all functionalities.
│   ├── test_data_extraction.py  # Tests the data extraction functionality.
│   ├── test_print_data.py       # Tests the print data functionality.
│   └── test_data_visualization.py # Tests the data visualization functionality.
│
├── Brain_GSE50161.csv           # Data file containing brain cancer gene expression levels.
├── pyproject.toml               # Project configuration file.
└── Project.code-workspace       # Visual Studio Code workspace file.





Usage

Run the project by executing main.py, which will process the data and output results based on the user's input. 

User Input:
- Enter a gene name to get details about the gene expression in different cancer types.
- Enter a cancer type to get information about the dominant alleles and their expression in the tumor.
