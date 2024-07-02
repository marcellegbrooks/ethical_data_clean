Automated Ethical Dataset Clean

Marcelle Brooks
May 2024

This program aims to automate some aspects of cleaning datasheets in hopes of 
making them as ethical as possible. Some ethical issues in datasheets that it 
addresses are: names, ages, date of births, locations (in multiple forms), 
incomes and occupations. 

To run this program, include a csv file in the command line.
    Example: python3 data_cleaner.py Artist_example.csv

Necessary libraries:
    - pandas==2.2.1
    - spacy==3.7.4
