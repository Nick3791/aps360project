"""
This scripts cleans the RecipeNLG_dataset.csv file located in the same directory as this script.
To be specific it will:
1. Filter out any and all single step recipes.
2. a) Concatenate ingredients, recipe title, and recipe steps together.
2. b) Insert control tokens between the concatenated sections.
3. Filter out inputs that are too long.
It will currently output the first 1000 cleaned entries of the dataset into RecipeNLG_clean.csv
"""

import csv
import ast

# Change this to true to see various debugging messages printed
DEBUG = False

# Defines when we skip a recipe, this is the maximum number of words the model input can have in it
# Otherwise, the tokenizer would not work, I also picked a lower value than the true max for safety
MAX_WORDS = 1400

def clean(start_rows=0, num_rows = 2, output_filename = 'RecipeNLG_clean_cropped.csv'):
    """
    Cleans the up to 'num_rows' entries from the dataset as per the docstring at the top of the script.
    Input: 
        start_rows indicates which row to start reading from
        num_rows indicating how many rows to clean up to. '-1' indicates reading the entire dataset.
        output_filename indicates the output filename
    Output: 
        None, a file is created that follows the argument above
    """
    input_filename = 'RecipeNLG_dataset.csv'

    in_file = open(input_filename, 'r', encoding='utf8')
    out_file = open(output_filename, 'w', newline='', encoding='utf8')

    # Set up the csv reader and writer objects
    csv_reader = csv.reader(in_file, delimiter=',')
    csv_writer = csv.writer(out_file, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')

    # Read in the header, this contains the columns in the dataset
    header = next(csv_reader)

    # We will not write the header, there will be a different header for our cleaned dataset
    new_header = ['entries']
    #csv_writer.writerow(new_header)

    # Now we begin cleaning by moving through the dataset
    for row, data in enumerate(csv_reader):
        if (row < start_rows): continue
        if (DEBUG): print('\n')
        # Break out if we reach the max number of rows to read
        if (row > num_rows and num_rows != -1): break
        
        # First, check if its a single step recipe, if it is, skip it.
        if (len(ast.literal_eval(data[3])) <= 1): continue

        # Keeps track of how many words there are in the model input
        num_words = 0

        # Next it will setup the concatenated model input along with the control tokens
        # Starting with inputs
        cleaned_data = "<RECIPE_START>" + '<INPUT_START>'
        for input in ast.literal_eval(data[6]):
            cleaned_data = cleaned_data + input + '<NEXT_INPUT>'
            num_words += len(input.split(' '))

        # Now to remove the extra 'next_input' that got appended
        cleaned_data = cleaned_data.removesuffix('<NEXT_INPUT>')
        cleaned_data = cleaned_data + '<INPUT_END>' + '<INGR_START>'

        # Next up, we will concatenate the ingredients
        for input in ast.literal_eval(data[2]):
            cleaned_data = cleaned_data + input + '<NEXT_INGR>'
            num_words += len(input.split(' '))

        cleaned_data = cleaned_data.removesuffix('<NEXT_INGR>')
        cleaned_data = cleaned_data + '<INGR_END>' + '<TITLE_START>'

        # Add in the title right after the ingredients
        cleaned_data = cleaned_data + data[1] + '<TITLE_END>' + '<INSTR_START>'
        num_words += len(data[1].split(' '))

        # Now to process the actual recipes steps
        for input in ast.literal_eval(data[3]):
            cleaned_data = cleaned_data + input + '<NEXT_INSTR>'
            num_words += len(input.split(' '))

        cleaned_data = cleaned_data.removesuffix('<NEXT_INSTR>')
        cleaned_data = cleaned_data + '<INSTR_END>' + '<RECIPE_END>'

        # Now to check if the final model input is too long for the tokenizer or not
        if (num_words > MAX_WORDS): continue

        # Lastly, we can write the data into our output file
        # Bit of a hack to get 'writerow' to write the row properly
        cleaned_data = str(cleaned_data)

        cleaned_data_list = cleaned_data.split("93129")
        csv_writer.writerow(cleaned_data_list)

        if (DEBUG): print(cleaned_data_list)

    return

clean(0, 500000, 'RecipeNLG_clean_cropped_1.csv')
clean(500001, 1000000, 'RecipeNLG_clean_cropped_2.csv')
clean(1000001, 1500000, 'RecipeNLG_clean_cropped_3.csv')
clean(1500001, 2000000, 'RecipeNLG_clean_cropped_4.csv')
clean(2000000, -1, 'RecipeNLG_clean_cropped_5.csv')




