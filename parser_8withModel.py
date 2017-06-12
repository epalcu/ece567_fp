from concurrent.futures import ProcessPoolExecutor
import collections
import xlrd
import sys
import time

sys.stderr.write("\nOpening workbook..\n")

# Start taking time, bruh..
start = time.time()

# Open Excel file
workbook = xlrd.open_workbook("Vehicles2006-2011.xlsx")

sys.stderr.write("Opening sheet..\n")

# Specify sheet within file to open
sheet = workbook.sheet_by_name("all car fires 2006-2011")

# Dictionary of makes that we care about..
makes = { "Chevrolet": {}, "Dodge": {}, "Ford": {} }

origin = 21
make = 35
model = 36
year = 37

sys.stderr.write("Populating dictionaries..\n")

# Function for adding data to dictionary
def add_to_dict(n_make):
    try:
        model_val = str(sheet.cell(row, model).value)
        year_val = int(sheet.cell(row, year).value)
        origin_val = str(sheet.cell(row, origin).value)

        # Convert "undetermined" to 100
        if (origin_val == "UU"):
            origin_val = "100"

        # Make sure year and origin data exist
        if (year_val != xlrd.empty_cell.value and origin_val != xlrd.empty_cell.value and model_val != xlrd.empty_cell.value):
            # Only care about fires that occur within vehicle and not outside source
            if (origin_val[0] == "8"):
                # If model already exists, add year and origin data
                if (model_val in makes[n_make].keys()):
                    # Add model year to make key within dictionary of makes
                    makes[n_make][model_val]["year"].append(year_val)
                    # Add model origin to make key within dictionary of makes
                    makes[n_make][model_val]["origin"].append(int(float(origin_val)))
                # Otherwise, create it
                else:
                    makes[n_make][model_val] = { "year": [year_val], "origin": [int(float(origin_val))] }
    finally:
        return

# Traverse across rows
for row in range(1, sheet.nrows):
    # If make is a Chevrolet
    if (sheet.cell(row, make).value == "CH"):
        add_to_dict("Chevrolet")

    # If make is a Ford
    elif (sheet.cell(row, make).value == "DO"):
        add_to_dict("Dodge")

    # If make is a Ford
    elif (sheet.cell(row, make).value == "FO"):
        add_to_dict("Ford")

sys.stderr.write("Writing to files..\n")

models = {}

# write_dict makes dictionary to files:
# Contained in the "samples.csv" are "make, model, year"
# Contained in the "targets.csv" are the fire origins
def write_dict(m, cnt, label):
    for key in m.keys():

        # Create a number representation of models for machine learning
        if (key in models.keys()):
            k = models[key]
        else:
            models[key] = cnt
            k = models[key]
            cnt += 1

        for key2, value in m[key].items():
            for val in value:
                if (key2 == "year"):
                    open("ml/samples_8withModel.csv", 'a+').write("{0}, {1}, {2}\n".format(label, k, val))
                else:
                    open("ml/targets_8withModel.csv", 'a+').write("{0}\n".format(val))

# Parallelize the writing of the dictionary..one worker process per dictionary key
with ProcessPoolExecutor(max_workers=3) as e:
    e.submit(write_dict, makes["Chevrolet"], 200, 33333)
    e.submit(write_dict, makes["Dodge"], 10000, 44444)
    e.submit(write_dict, makes["Ford"], 20000, 55555)

# End the time
end = time.time() - start
sys.stderr.write("\nTotal elapsed time: {0}.\n\n".format(round(end, 2)))
exit()
