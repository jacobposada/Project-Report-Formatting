import pandas as pd 
import json 

# load the JSON file 
with open ('user_paths.json') as f: 
    user_data = json.load(f) 

# function to get input and output paths based on username 
def get_paths(username): 
    for user in user_data['users']: 
        if user['username'] == username: 
            return user['input_path'], user['output_path'] 
    return None, None # return None if username not found 

username = input("Enter username: ")

# get input and output paths 
input_path, output_path = get_paths(username) # how do i get the username without manually inserting it? 
print (input_path) 
print(output_path)


# specify Excel file formatted incorrectly 
file_name = "12215-2021-CG-SADEN-AOP-ficha_resumen_url_table_1"
excel_file = input_path + file_name + ".xlsx"


# read Excel file into pandas dataframe 
df = pd.read_excel(excel_file)


def parse_column_1(dataframe): 
## formats 'row' column and cleans up empty cells, works for all files 

    # create variable to store current phrase being evaluated 
    current_phrase = "" 

    # iterate through row column 
    for index, cell_value in df['row'].items(): 
       # fill empty rows with empty strings 
       df.fillna({'row': ''}, inplace=True)
       if cell_value.endswith(":"): 
            # add current cell ending with : to current_phrase 
            current_phrase += cell_value
           
            # update cell with full combined phrase 
            df.at[index, 'row'] = current_phrase 
            current_phrase = "" 
        
       elif cell_value != '':
            # add cell to current phrase until colon is found 
            current_phrase += cell_value + " "
            # replace incomplete rows with empty strings 
            df.at[index, 'row'] = "" 
       
    # brings non-empty rows to the top, maintaining their order 
    df['row'] = sorted(df['row'], key=lambda x: x == '')

    return df 


### FUNCTION FOR VALUE COLUMN 

def parse_column_2_format_1(dataframe): 
## formats 'value' column, works for file format 1 
    
    # fill empty value rows with empty strings 
    df.fillna({'value': ''}, inplace=True) 

    # turn all value columns to strings 
    df['value'] = df['value'].astype(str) 

    # manually corrects and cleans rows 
    df.iloc[2, 2] += " " + df.iloc[3, 2] + " " + df.iloc[4, 2] 
    df.iloc[3:5,2] = "" 
    df.iloc[7, 2] += " " + df.iloc[8, 2] + " " + df.iloc[9, 2] + " " + df.iloc[10, 2] + " " + df.iloc[11, 2] 
    df.iloc[8:12,2] = "" 
    df.iloc[15, 2] += " " + df.iloc[16, 2] 
    df.iloc[16,2] = "" 
    df.iloc[19, 2] += " " + df.iloc[20, 2] 
    df.iloc[20,2] = "" 

    # push empty rows to bottom 
    df['value'] = sorted(df['value'], key=lambda x: x == '')

    return df 


def parse_column_2_format_2(dataframe): 
## formats 'value' column, works for file format 2 
    
    # fill empty value rows with empty strings 
    df.fillna({'value': ''}, inplace=True) 

    # turn all value columns to strings 
    df['value'] = df['value'].astype(str) 

    # manually corrects and cleans rows 
    df.iloc[2,2] += " " + df.iloc[3, 2] + " " + df.iloc[4, 2] + " " + df.iloc[5, 2] + " " + df.iloc[6, 2] 
    df.iloc[3:7, 2] = "" 
    df.iloc[8,2] += " " + df.iloc[9, 2] 
    df.iloc[9,2] = ""

    # push empty rows to bottom 
    df['value'] = sorted(df['value'], key=lambda x: x == '') 

    return df 


def parse_column_2_format_3(dataframe): 
## formats 'value' column, works for file format 3 
    
    # fill empty value rows with empty strings 
    df.fillna({'value': ''}, inplace=True) 

    # turn all value columns to strings 
    df['value'] = df['value'].astype(str) 

    # manually corrects and cleans rows 
    df.iloc[1,2] += df.iloc[2,2]
    df.iloc[2,2] = "" 
    df.iloc[4,2] += df.iloc[5,2] 
    df.iloc[5,2] = "" 

    # push empty rows to bottom 
    df['value'] = sorted(df['value'], key=lambda x: x == '') 

    return df 


def parse_column_2_format_4(dataframe): 
## formats 'value' column, works for file format 3 
    
    # fill empty value rows with empty strings 
    df.fillna({'value': ''}, inplace=True) 

    # turn all value columns to strings 
    df['value'] = df['value'].astype(str) 

    # manually corrects and cleans rows 




# renumber indexing column in case numbers incorrect 
df.iloc[:, 0] = range(0, len(df)) 



df = parse_column_1(df) 
df = parse_column_2_format_2(df) 
print(df)

# write corrected dataframe back to an Excel sheet 
df.to_excel(output_path + file_name + "_parsed.xlsx", index=False) 