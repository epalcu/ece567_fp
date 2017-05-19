from concurrent.futures import ProcessPoolExecutor
import collections
import xlrd
import sys
import time

'''
Description: Script reads in Excel file of all vehicle fires and extracts
              vehicle make, year, and origin of file. These are placed within
              their appropriate dictionaries and ultimately written out to two
              files for the machine learning process: samples.csv and targets.csv.
USAGE: python parser.py
'''

sys.stderr.write("\nOpening workbook..")

# Start taking time, bruh..
start = time.time()

# Open Excel file
workbook = xlrd.open_workbook("Vehicles2006-2011.xlsx")

sys.stderr.write("done.\n")

sys.stderr.write("Opening sheet..")

# Specify sheet within file to open
sheet = workbook.sheet_by_name("all car fires 2006-2011")

sys.stderr.write("done.\n")

# Dictionary of makes that we care about..
makes = {"Chevrolet": {"year": [], "origin": []},
         "Dodge": {"year": [], "origin": []},
         "Ford": {"year": [], "origin": []}
         }

num_rows = sheet.nrows

origin = 21
make = 35
year = 37

sys.stderr.write("Populating dictionaries..")

def add_to_dict(n_make):
    try:
        year_val = int(sheet.cell(row, year).value)
        origin_val = str(sheet.cell(row, origin).value)

        # Convert "undetermined" to 100
        if (origin_val == "UU"):
            origin_val = 100

        # Make sure year and origin data exist
        if (year_val != xlrd.empty_cell.value and origin_val != xlrd.empty_cell.value):
            # Add model year to "Ford" key within dictionary of makes
            makes[n_make]["year"].append(year_val)
            # Add model origin to "Ford" key within dictionary of makes
            makes[n_make]["origin"].append(int(float(origin_val)))
    finally:
        return

# Traverse across rows
for row in range(1, num_rows):
    # If make is a Chevrolet
    if (sheet.cell(row, make).value == "CH"):
        add_to_dict("Chevrolet")

    # If make is a Ford
    elif (sheet.cell(row, make).value == "DO"):
        add_to_dict("Dodge")

    # If make is a Ford
    elif (sheet.cell(row, make).value == "FO"):
        add_to_dict("Ford")

sys.stderr.write("done.\n")

sys.stderr.write("Writing to files..")

# Write makes dictionary to files:
# Contained in the "samples.csv" are "Make, year"
# Contained in the "targets.csv" are the fire origins
def write_dict(items, label):
    for key, value in items:
        for val in value:
            if (key == "year"):
                open("ml/samples.csv", 'a+').write("{0}, {1}\n".format(label, val))
            else:
                open("ml/targets.csv", 'a+').write("{0}\n".format(val))

# Parallelize the writing of the dictionary..one worker process per dictionary key
with ProcessPoolExecutor(max_workers=3) as e:
    e.submit(write_dict, makes["Chevrolet"].items(), 1000)
    e.submit(write_dict, makes["Dodge"].items(), 1001)
    e.submit(write_dict, makes["Ford"].items(), 1002)

sys.stderr.write("done.\n")

# End the time
end = time.time() - start
sys.stderr.write("\nTotal elapsed time: {0}.\n\n".format(round(end, 2)))
exit()
