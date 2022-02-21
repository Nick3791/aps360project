import csv


# Reads the RecipeNLG dataset and selects the first 1000 recipes
# Outputs a "cropped" version of that dataset as RecipeNLG_cropped.csv

output_filename = 'RecipeNLG_cropped.csv'

# Open the input and output files
in_file = open('RecipeNLG_dataset.csv', 'r')
out_file = open(output_filename, 'w', newline='')

# Setup the reader writer objects
csv_reader = csv.reader(in_file, delimiter=',')
csv_writer = csv.writer(out_file, delimiter=',')

# This represents the columns of the dataset
header = next(csv_reader)

# Write the header
csv_writer.writerow(header)

data = []
for i in range(0, 100):
    data.append(next(csv_reader))

csv_writer.writerows(data)

in_file.close()
out_file.close()
