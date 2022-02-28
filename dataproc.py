# Imports
import numpy as np
import pandas as pd
import csv

def datasplit(startrow, endrow, output_filename):

    # Open the input and output files
    in_file = open('gdrive/MyDrive/APS360/RecipeNLG_dataset.csv', 'r') #replace with relevant file path
    out_file = open(output_filename+'.csv', 'w', newline='')

    # Setup the reader writer objects
    csv_reader = csv.reader(in_file, delimiter=',')
    csv_writer = csv.writer(out_file, delimiter=',')

    header = next(csv_reader)

    # Write the header
    csv_writer.writerow(header)

    vals = []

    # This represents the columns of the dataset
    for row, data in enumerate(csv_reader, start=startrow):
        if (row > endrow):
            break
        vals.append(data)

    csv_writer.writerows(vals)

    in_file.close()
    out_file.close()

# Training, test and validation splits: 70/15/15
# Training rows: 0.7*2231142 = 1561800
# Test rows: 0.15*2231142 = 334671
# Validation rows: 0.15*2231142 = 334671
datasplit(0,1561800,'train_set')
datasplit(1561800,1896471,'val_set')
datasplit(1896471,2231142,'test_set')