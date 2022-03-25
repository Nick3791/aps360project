import csv


# Reads the RecipeNLG dataset and selects the first 1000 recipes
# Outputs a "cropped" version of that dataset as RecipeNLG_cropped.csv

output_filename = 'RecipeNLG_cropped.csv'

# Open the input and output files
in_file = open('RecipeNLG_dataset.csv', 'r', encoding='utf8')
out_file = open(output_filename, 'w', newline='')

# Setup the reader writer objects
csv_reader = csv.reader(in_file, delimiter=',')
csv_writer = csv.writer(out_file, delimiter=',')

header = next(csv_reader)

# Write the header
csv_writer.writerow(header)

vals = []
max = 0
max_str = ' '

# This represents the columns of the dataset
for row, data in enumerate(csv_reader):
    #if (row > 50000):
    #    break
    #new = (data[3]).encode("ascii", "ignore")
    #new = new.decode()
    #vals.append([row, new])
    if len(data[3]) > max:
        max = len(data[3])
        max_str = data[3]

print(max)
print(max_str)

csv_writer.writerows(vals)

in_file.close()
out_file.close()
