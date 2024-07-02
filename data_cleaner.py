import pandas as pd 
import spacy
import sys
import datetime as dt
from datetime import date

# read file
inFile = sys.argv[1]
dataset = pd.read_csv(inFile)

# today's date
today = date.today()

# Name recognizer
nlp = spacy.load("en_core_web_md")

def name_cleaning(names):
    # detects if the strings in a colunm are names (identified as PERSON)
    count = 0
    num_names = len(names)
    for i in range(num_names):
        name = nlp(names[i])
        for ent in name.ents:
            if ent.label_ == "PERSON":
                count += 1
    return count

def age_bracket_5yrs(age):
    # removes specific ages, cohorts of 5 years
    match age:
        case _ if age <= 20: return 'Under 20'
        case _ if 20 < age <= 25: return '21-25'
        case _ if 25 < age <= 30: return '26-30'
        case _ if 30 < age <= 35: return '31-35'
        case _ if 35 < age <= 40: return '36-40'
        case _ if 40 < age <= 45: return '41-45'
        case _ if 45 < age <= 50: return '46-50'
        case _ if 50 < age <= 55: return '51-55'
        case _ if 55 < age <= 60: return '56-60'
        case _ if 60 < age <= 65: return '61-65'
        case _ if 65 < age <= 70: return '66-70'
        case _ if 70 < age <= 75: return '71-75'
        case _ if 75 < age <= 80: return '76-80'
        case _ if 80 < age <= 85: return '81-85'
        case _ if 85 < age <= 90: return '86-90'
        case _ if 90 < age <= 95: return '91-95'
        case _ if 95 < age <= 100: return '96-100'
        case _ if 100 < age <= 105: return '101-105'
        case _ if 105 < age <= 110: return '106-110'
        case _ if 110 < age: return 'over 110'
        case _: return 'Unknown'

def age_bracket_10yrs(age):
    # removes specific ages, cohorts of 5 years
    match age:
        case _ if age <= 20: return 'Under 20'
        case _ if 20 < age <= 30: return '21-30'
        case _ if 30 < age <= 40: return '31-40'
        case _ if 40 < age <= 50: return '41-50'
        case _ if 50 < age <= 60: return '51-60'
        case _ if 60 < age <= 70: return '61-70'
        case _ if 70 < age <= 80: return '71-80'
        case _ if 80 < age <= 90: return '81-90'
        case _ if 90 < age <= 100: return '91-100'
        case _ if 100 < age <= 110: return '101-110'
        case _ if 110 < age: return 'over 110'
        case _: return 'Unknown'

def dob_to_ages(dob): 
    # converts dates to the years (or age) since that date based on current date
    date = dt.datetime.strptime(dob, '%Y-%m-%d').date()
    age = today.year - date.year - ((today.month, today.day) < (date.month, date.day))
    return age

def age_detected():
    # prompts the user on what to do if ages are detected in the dataset
    while True:
        print("\nWe have detected ages in your datset. How would you like to proceed?")
        choice = input("Please type 'r' for remove the column, 'p' to keep it, '5'  or '10' to bracket your ages in 5 or 10 year cohorts: ")
        if choice == "r" or choice == "5" or choice == "10":
            return choice

def zip_detected():
    # prompts the user on what to do if a zip code is detected in the dataset
    while True:
        print("\nWe have detected Zip Codes in your datset. How would you like to proceed?")
        choice = input("Please type 'y' if you would like to remove the column, and 'n' if not: ")
        if choice == "y" or choice == "n":
            return choice

def dob_detected(col_name):
    # prompts the user on what to do if a date of birth is detected in the dataset
    while True:
        print("\nWe have detected dates in your datset in the column named:", col_name, ". How would you like to proceed?")
        choice = input("Please type 'r' for remove the column, 'p' to keep it, '5'  or '10' to bracket your ages in 5 or 10 year cohorts: ")
        if choice == "r" or choice == "5" or choice == "10" or choice == 'p':
            return choice
    
def job_detected(col_name):
    # prompts the user on what to do if an occupation is detected in the dataset
    while True:
        print("\nWe have detected Job or Occupation in your datset in the column named:", col_name, ". How would you like to proceed?")
        choice = input("Please type 'y' if you would like to remove the column, and 'n' if not: ")
        if choice == "y" or choice == "n":
            return choice

def income_detected(col_name):
    # prompts the user on what to do if an income is detected in the dataset
    while True:
        print("\nWe have detected an income in your datset in the column named:", col_name, ". How would you like to proceed?")
        choice = input("Please type 'y' if you would like to remove the column, and 'n' if not: ")
        if choice == "y" or choice == "n":
            return choice

def nan_detected(num_nan, col_name, types):
    # prompts the user on what to do if an empty value is detected in the dataset
    while True:
        print("\nWe have detected", num_nan, "empty values in the column named:", col_name, ". How would you like to proceed?")
        if types == "int64" or types == "float64" : # can only replace values with 0 if the column is of type int or float
            choice = input("Please type 'r' if you would like to remove the rows, 'c' if you would like to remove the column, and 'p' if you would like to do nothing, 'o' if you would like to replace the values with 0: ")
            if choice == "r" or choice == "c" or choice == 'p' or choice == 'o':
                return choice
        else:
            choice = input("Please type 'r' if you would like to remove the rows, 'c' if you would like to remove the column, and 'p' if you would like to do nothing: ")
            if choice == "r" or choice == "c" or choice == 'p':
                return choice


# Main function
def data_clean(dataset): 
    # List of columns to remove
    remove_list = []

    # List of actions
    actions = []

    for i in range(len(dataset.columns)):
        # Current column
        curr = dataset.columns[i]

        # Check empty column
        remove = 0
        num_nan = dataset[curr].isnull().sum()
        if num_nan == len(dataset[curr]):
            remove_list.append(curr)
            remove = 1
            actions.append("Removed empty column " + curr)
        
        # Check for Nan values
        if num_nan > 0 and remove == 0:
            choice = nan_detected(num_nan, curr, dataset.dtypes[curr])
            if choice == 'c': 
                remove_list.append(curr)
                actions.append("Remove column " + curr + " because of empty values")
            elif choice == 'r': 
                dataset.dropna(subset=[curr], inplace=True)
                actions.append("Removed rows from column " + curr + " because of empty values")
            elif choice == 'o':
                dataset[curr] = dataset[curr].fillna(0)
                actions.append("Replaced empty values with 0 in column " + curr)


        if dataset.dtypes[curr] == 'object':

            # check names
            if 'name' in curr.lower():
                remove_list.append(curr)
                actions.append("Removed column " + curr + " because of names")
            else:
                try:
                    names = dataset[curr]
                    count = name_cleaning(names[:500]) # to avoid a slow program
                    if count > 200:
                        remove_list.append(curr)
                        actions.append("Removed column " + curr + " because of names")
                except:
                    count = 0
            
            # check date of birth
            if 'dob' in curr.lower() or 'birth' in curr.lower():
                choice = dob_detected(curr)
                if choice == "r":
                    remove_list.append(curr)
                    actions.append("Removed column " + curr + " because of date of birth")
                elif choice == "5" or choice == "10":
                    dataset[curr] = dataset[curr].apply(dob_to_ages)
                    if choice == "5":
                        dataset[curr] = dataset[curr].apply(age_bracket_5yrs)
                        actions.append("Bracketed ages in column " + curr + " in 5 year cohorts")
                    elif choice == "10":
                        dataset[curr] = dataset[curr].apply(age_bracket_10yrs)
                        actions.append("Bracketed ages in column " + curr + " in 10 year cohorts")
            else:
                try:
                    date = dt.datetime.strptime(dataset[curr].iloc[1], '%Y-%m-%d').date()
                    choice = dob_detected(curr)
                    if choice == "r":
                        remove_list.append(curr)
                        actions.append("Removed column " + curr + " because of date of birth")
                    elif choice == "5" or choice == "10":
                        dataset[curr] = dataset[curr].apply(dob_to_ages)
                        if choice == "5":
                            dataset[curr] = dataset[curr].apply(age_bracket_5yrs)
                            actions.append("Bracketed ages in column " + curr + " in 5 year cohorts")
                        elif choice == "10":
                            dataset[curr] = dataset[curr].apply(age_bracket_10yrs)
                            actions.append("Bracketed ages in column " + curr + " in 10 year cohorts")
                except:
                    count = 0

            # Check occupation
            if 'occupation' in curr.lower() or 'job' in curr.lower():
                choice = job_detected(curr)
                if choice == "y":
                    remove_list.append(curr)
                    actions.append("Removed column " + curr + " because of occupation")

            # Check address and remove
            if 'address' in curr.lower():
                remove_list.append(curr)
                actions.append("Removed column " + curr + " because of date of address")
            
        
        if dataset.dtypes[curr] == 'int64' or 'float64':

            # check ages
            if 'age' in curr.lower():
                choice = age_detected()
                if choice == "r":
                    remove_list.append(curr)
                    actions.append("Removed column " + curr + " because of age")
                elif choice == "5":
                    dataset[curr] = dataset[curr].apply(age_bracket_5yrs)
                    actions.append("Bracketed ages in column " + curr + " in 5 year cohorts")
                elif choice == "10":
                    dataset[curr] = dataset[curr].apply(age_bracket_10yrs)
                    actions.append("Bracketed ages in column " + curr + " in 10 year cohorts")

            # Check Zip code
            if 'zip' in curr.lower():
                choice = zip_detected()
                if choice == "y":
                    remove_list.append(curr)
                    actions.append("Removed column " + curr + " because of Zip code")

            # Check income
            if 'income' in curr.lower() or 'dollar' in curr.lower() or 'euro' in curr.lower():
                choice = income_detected(curr)
                if choice == "y":
                    remove_list.append(curr)
                    actions.append("Removed column " + curr + " because of income")
            
            # Check longitude and latitude
            if 'longitude' in curr.lower():
                remove_list.append(curr)
                actions.append("Removed column " + curr + " because of longitude")
            if 'latitude' in curr.lower():
                remove_list.append(curr)
                actions.append("Removed column " + curr + " because of latitude")


    # drop columns
    dataset.drop(remove_list, axis=1, inplace=True)

    # Print summary of actions taken:
    if len(actions) == 0:
        print("\n No actions were taken to clean your dataset. Please know that while this may seem like a good thing, your data may still be unethical.")
    else:
        print("\nHere is the summary of the actions taken to clean your dataset:")
        for i in range(len(actions)):
            print("\t-", actions[i])
        print("Please not your data still be unethical in ways this program was unable to detect. Please proceed with caution. ")
    
    return dataset

# run function:
new_dataset = data_clean(dataset)

# save as new file
name_file = inFile.split(".")[0] + "_clean.csv"
new_dataset.to_csv(name_file)